from django.shortcuts import render
from django.http import JsonResponse
from api.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import MyTokenObtainPairSerializer, RegisterSerializer, TaskSerializers, UserSerializer, GroupSerializer, GroupProject_Assoc_Serializers, ProjectTaskSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from rest_framework import viewsets
from .serializers import ProjectSerializers
from .models import Project, Task, Group, GroupNprojectAssoc


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['POST'])
def confirm_email(request):
    token = request.data.get('token')
    user = User.objects.filter(confirmation_token=token).first()

    if user:
        user.email_confirmed = True
        user.save()
        return Response({'message': 'Email confirmed successfully'}, status=200)
    else:
        return Response({'message': 'Invalid token'}, status=400)

# Get All Routes
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
        '/api/projects/'
        
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get("text")
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import User

@api_view(['POST'])
def send_confirmation_email(request):
    # Extract the user email and token from the request data
    email = request.data.get('email')
    token = request.data.get('token')

    # Retrieve the user with the provided email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Send the confirmation email
    subject = 'Confirm your email'
    message = render_to_string('confirmation_email.html', {'token': token})
    send_mail(subject, message, 'from@example.com', [email])

    return JsonResponse({'message': 'Confirmation email sent successfully'}, status=200)


class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers

class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupProject_Assoc_View(viewsets.ModelViewSet):
    queryset = GroupNprojectAssoc.objects.all()
    serializer_class = GroupProject_Assoc_Serializers

class ProjectTaskView(viewsets.ModelViewSet):
    serializer_class = ProjectTaskSerializer

    def get_queryset(self):
        project_name = self.kwargs['project_name']  # Fetch project name from URL kwargs
        return Task.objects.filter(project_name__project_name=project_name)  # Filter tasks by project name

    def perform_create(self, serializer):
        project_name = self.kwargs['project_name']  # Fetch project name from URL kwargs
        project = Project.objects.get(project_name=project_name)  # Fetch project instance
        serializer.save(project_name=project)  # Save task with project instance
