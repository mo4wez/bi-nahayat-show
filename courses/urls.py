from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'steps', views.StepViewSet)
router.register(r'levels', views.LevelViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'progress', views.UserProgressViewSet, basename='userprogress')
router.register(r'logs', views.BotLogViewSet, basename='botlog')

urlpatterns = [
    path('api/', include(router.urls)),
]