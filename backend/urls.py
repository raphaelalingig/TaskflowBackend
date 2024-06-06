from django.contrib import admin
from django.urls import path, include
from api.views import confirm_email
from rest_framework import routers
from api import views
router = routers.DefaultRouter()
router.register(r'projects', views.ProjectView, 'projects' )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
    path('confirm-email/', confirm_email, name='confirm_email'),
]
