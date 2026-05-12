from rest_framework import serializers
from .models import Step, Level, Question, UserProgress, BotLog

class QuestionSerializer(serializers.ModelSerializer):
    full_reference = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'question_number', 'question_text', 'answer', 'hint', 'tags', 'full_reference']
    
    def get_full_reference(self, obj):
        return obj.get_full_reference()

class LevelSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    question_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Level
        fields = ['id', 'level_number', 'title', 'description', 'question_count', 'questions']
    
    def get_question_count(self, obj):
        return obj.get_question_count()

class StepSerializer(serializers.ModelSerializer):
    levels = LevelSerializer(many=True, read_only=True)
    level_count = serializers.SerializerMethodField()
    question_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Step
        fields = ['id', 'step_number', 'title', 'description', 'level_count', 'question_count', 'levels']
    
    def get_level_count(self, obj):
        return obj.get_level_count()
    
    def get_question_count(self, obj):
        return obj.get_question_count()

class UserProgressSerializer(serializers.ModelSerializer):
    step_title = serializers.CharField(source='step.title', read_only=True)
    level_title = serializers.CharField(source='level.title', read_only=True)
    completed_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProgress
        fields = [
            'id', 'user_id', 'step', 'step_title', 'level', 'level_title',
            'last_question', 'completed_questions', 'completed_count', 
            'last_active', 'created_at'
        ]
        read_only_fields = ['created_at', 'last_active']
    
    def get_completed_count(self, obj):
        return obj.completed_questions.count()

class BotLogSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    
    class Meta:
        model = BotLog
        fields = ['id', 'user_id', 'action', 'message', 'response', 'question', 'question_text', 'created_at']
        read_only_fields = ['created_at']