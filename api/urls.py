from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'projects', views.ProjectView, 'projects' )
router.register(r'task', views.TaskView, 'task' )
router.register(r'user', views.UserView, 'user' )
router.register(r'group', views.GroupView, 'group' )
router.register(r'groupProject_assoc', views.GroupProject_Assoc_View, 'groupProject_assoc' )
router.register(r'projects/(?P<project_name>[^/.]+)/tasks', views.ProjectTaskView, basename='project-tasks')






urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    # path('projects/<str:project_name>/tasks/', views.ProjectTaskView.as_view(), name='project-tasks-view'),
    path('test/', views.testEndPoint, name='test'),
    path('send-confirmation-email/', views.send_confirmation_email, name='send_confirmation_email'),
    path('', views.getRoutes),
    path('', include(router.urls)),
]
