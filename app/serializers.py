from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, FriendRequest


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password2", "first_name", "last_name"]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"required": True},
            "password2": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match"
            )
        return attrs

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["email"].split("@")[0],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class RequestAcceptSerializer(serializers.Serializer):
    request_id = serializers.IntegerField(allow_null=False, required=True)


class RequestSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField(allow_null=False, required=True)



class ViewRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)
    status = serializers.CharField(required=False)
    sender = UserSerializer()
    receiver = UserSerializer()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
