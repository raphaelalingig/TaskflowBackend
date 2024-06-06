from api.models import User, Project, Group, Task, GroupNprojectAssoc
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # These are claims, you can add custom claims
        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio
        token['image'] = str(user.profile.image)
        token['verified'] = user.profile.verified
        # ...
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id','email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']

        )

        user.set_password(validated_data['password'])
        user.save()

        return user



class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task_name','project_name', 'start_date', 'due_date', 'assignee', 'description', 'get_project_name', 'get_user_name')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'members', 'projects', 'get_member_names')

class ProjectSerializers(serializers.ModelSerializer):
    group = GroupSerializer(many=True)  # Use the nested serializer

    class Meta:
        model = Project
        fields = ('id','project_name', 'start_date', 'due_date', 'description', 'group')


class GroupProject_Assoc_Serializers(serializers.ModelSerializer):
    project = ProjectSerializers(many=True)

    class Meta:
        model = GroupNprojectAssoc
        fields = ('id', 'group', 'project', 'members')


class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task_name', 'start_date', 'due_date', 'description', 'project_name', 'assignee', 'get_project_name', 'get_user_name')

