from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth import authenticate, get_user_model

from .serializers import *
from .models import *

# Create your views here.


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "payload": serializer.errors,
                    "status": 400,
                    "message": "Something went Wrong",
                }
            )
        serializer.save()
        user = User.objects.get(email=serializer.data["email"])
        Userserializer = UserSerializer(user)
        return Response(
            {
                "payload": Userserializer.data,
                "status": 201,
                "message": "User is Register Successfully",
            }
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "code": 400, "errors": serializer.errors})
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        print("sds", email, password)
        user = authenticate(request, username=email, password=password)
        print("user", user)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "status": True,
                    "code": 200,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response({"status": False, "code": 401, "errors": "Invalid credentials"})


class SearchUsersView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        try:
            search_string = request.GET.get("search", "")
            if "@" in search_string:
                print("search_string", search_string)
                users = User.objects.filter(email__iexact=search_string)
                serializer = UserSerializer(users[0])
            else:
                users = User.objects.filter(username__icontains=search_string)
                serializer = UserSerializer(users, many=True)

            return Response(
                {
                    "payload": serializer.data,
                    "status": 200,
                    "message": "User fetched successfully",
                }
            )

        except BaseException as err:
            print(err)
            return Response({"status": False, "code": 500, "message": str(err)})


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = "app"

    def post(self, request):
        try:
            serializer = RequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"status": False, "code": 400, "errors": serializer.errors}
                )

            receiver = User.objects.get(id=serializer.validated_data["receiver_id"])
            friend_request, created = FriendRequest.objects.get_or_create(
                sender=request.user, receiver=receiver
            )
            if created:
                serializer = ViewRequestSerializer(friend_request)

                return Response(
                    {
                        "payload": serializer.data,
                        "status": 201,
                        "message": "Request sent",
                    }
                )
            return Response(
                {
                    "status": 400,
                    "message": "Request already exists",
                }
            )
        except BaseException as err:
            print(err.__traceback__.tb_lineno)
            return Response({"status": False, "code": 500, "message": str(err)})


class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = RequestAcceptSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"status": False, "code": 400, "errors": serializer.errors}
                )
            friend_request = FriendRequest.objects.get(
                id=serializer.validated_data["request_id"], receiver=request.user
            )
            friend_request.status = "accepted"
            friend_request.save()
            serializer = ViewRequestSerializer(friend_request)
            return Response(
                {
                    "payload": serializer.data,
                    "status": 200,
                    "message": "Request accepted",
                }
            )

        except BaseException as err:
            return Response({"status": False, "code": 500, "message": str(err)})


class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = RequestAcceptSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"status": False, "code": 400, "errors": serializer.errors}
                )
            friend_request = FriendRequest.objects.get(
                id=serializer.validated_data["request_id"], receiver=request.user
            )
            friend_request.status = "rejected"
            friend_request.save()
            serializer = ViewRequestSerializer(friend_request)
            return Response(
                {
                    "payload": serializer.data,
                    "status": 200,
                    "message": "Request rejected",
                }
            )
        except BaseException as err:
            return Response({"status": False, "code": 500, "message": str(err)})


class ListFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            friends = FriendRequest.objects.filter(
                sender=user, status="accepted"
            ).values_list("receiver", flat=True)
            users = User.objects.filter(id__in=friends)
            if len(users) > 0:
                serializer = UserSerializer(users, many=True)

                return Response(
                    {
                        "payload": serializer.data,
                        "status": 200,
                        "message": "All User fetched successfully who have accepted friend request",
                    }
                )
            return Response(
                {
                    "status": 200,
                    "message": "No User found with this User",
                }
            )

        except BaseException as err:
            return Response({"status": False, "code": 500, "message": str(err)})


class ListPendingFriendRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            friends = FriendRequest.objects.filter(receiver=user, status="pending")

            if len(friends) > 0:
                serializer = ViewRequestSerializer(friends, many=True)

                return Response(
                    {
                        "payload": serializer.data,
                        "status": 200,
                        "message": "All received friend request fetched successfully",
                    }
                )
            return Response(
                {
                    "status": 200,
                    "message": "No friend request found with this User",
                }
            )

        except BaseException as err:
            return Response({"status": False, "code": 500, "message": str(err)})
