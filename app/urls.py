from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.Register.as_view(), name="signup"),
    path("search-user/", views.SearchUsersView.as_view(), name="search_users"),
    path(
        "friend-request/send/",
        views.SendFriendRequestView.as_view(),
        name="send_friend_request",
    ),
    path(
        "friend-request/accept/",
        views.AcceptFriendRequestView.as_view(),
        name="accept_friend_request",
    ),
    path(
        "friend-request/reject/",
        views.RejectFriendRequestView.as_view(),
        name="reject_friend_request",
    ),
    path("friends/", views.ListFriendsView.as_view(), name="list_friends"),
    path(
        "friend-requests/pending/",
        views.ListPendingFriendRequestsView.as_view(),
        name="list_pending_friend_requests",
    ),
]
