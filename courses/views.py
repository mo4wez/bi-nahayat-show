from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Step, Level, Question, UserProgress, BotLog
from .serializers import (
    StepSerializer, LevelSerializer, QuestionSerializer, 
    UserProgressSerializer, BotLogSerializer
)

class StepViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Step.objects.all().prefetch_related('levels__questions')
    serializer_class = StepSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

class LevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Level.objects.all().prefetch_related('questions')
    serializer_class = LevelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        level = self.get_object()
        questions = level.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all().select_related('level__step')
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['question_text', 'answer', 'tags']
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            questions = Question.objects.filter(
                Q(question_text__icontains=query) |
                Q(answer__icontains=query) |
                Q(tags__icontains=query)
            ).select_related('level__step')[:10]
            serializer = self.get_serializer(questions, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=True, methods=['post'])
    def track_view(self, request, pk=None):
        question = self.get_object()
        user_id = request.data.get('user_id')
        if user_id:
            progress, created = UserProgress.objects.get_or_create(
                user_id=user_id,
                step=question.level.step,
                level=question.level
            )
            progress.update_progress(question)
        return Response({'status': 'tracked'})

class UserProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserProgressSerializer
    
    def get_queryset(self):
        """Dynamically return queryset based on user_id parameter"""
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return UserProgress.objects.filter(user_id=user_id)
        # Return empty queryset if no user_id specified
        return UserProgress.objects.none()
    
    def list(self, request, *args, **kwargs):
        """Override list to require user_id parameter"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {"error": "user_id parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().list(request, *args, **kwargs)

class BotLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing bot logs (admin only)"""
    queryset = BotLog.objects.all().select_related('question')
    serializer_class = BotLogSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user_id', 'message', 'response']
    ordering_fields = ['created_at']
    ordering = ['-created_at']