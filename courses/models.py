from django.db import models
from django.contrib import admin
from django.utils import timezone

class Step(models.Model):
    step_number = models.PositiveIntegerField(unique=True, verbose_name="Step Number")
    title = models.CharField(max_length=200, verbose_name="Step Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['step_number']
        verbose_name = "Step"
        verbose_name_plural = "Steps"
    
    def __str__(self):
        return f"Step {self.step_number}: {self.title}"
    
    def get_level_count(self):
        return self.levels.count()
    
    def get_question_count(self):
        return sum(level.questions.count() for level in self.levels.all())

class Level(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='levels')
    level_number = models.PositiveIntegerField(verbose_name="Level Number")
    title = models.CharField(max_length=200, verbose_name="Level Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['step__step_number', 'level_number']
        unique_together = [['step', 'level_number']]
        verbose_name = "Level"
        verbose_name_plural = "Levels"
    
    def __str__(self):
        return f"Step {self.step.step_number} > Level {self.level_number}: {self.title}"
    
    def get_question_count(self):
        return self.questions.count()

class Question(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='questions')
    question_number = models.PositiveIntegerField(verbose_name="Question Number")
    question_text = models.TextField(verbose_name="Question Text")
    answer = models.TextField(verbose_name="Answer")
    hint = models.TextField(blank=True, null=True, verbose_name="Hint")
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags for search")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['level__step__step_number', 'level__level_number', 'question_number']
        unique_together = [['level', 'question_number']]
        verbose_name = "Question"
        verbose_name_plural = "Questions"
    
    def __str__(self):
        return f"Q{self.question_number}: {self.question_text[:50]}..."
    
    def get_full_reference(self):
        return f"Step {self.level.step.step_number} > Level {self.level.level_number} > Question {self.question_number}"

class UserProgress(models.Model):
    user_id = models.CharField(max_length=100, db_index=True)
    step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    last_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    completed_questions = models.ManyToManyField(Question, related_name='completed_by', blank=True)
    last_active = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "User Progress"
        verbose_name_plural = "User Progress"
        unique_together = [['user_id', 'step', 'level']]
    
    def __str__(self):
        return f"User {self.user_id} - Step {self.step.step_number if self.step else 'None'}"
    
    def update_progress(self, question):
        """Update user progress with a completed question"""
        if not self.completed_questions.filter(id=question.id).exists():
            self.completed_questions.add(question)
        self.last_question = question
        self.last_active = timezone.now()
        self.save()

class BotLog(models.Model):
    ACTION_CHOICES = [
        ('QUERY', 'Query'),
        ('RESPONSE', 'Response'),
        ('ERROR', 'Error'),
        ('FEEDBACK', 'Feedback'),
    ]
    
    user_id = models.CharField(max_length=100, db_index=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    message = models.TextField()
    response = models.TextField(blank=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bot Log"
        verbose_name_plural = "Bot Logs"
    
    def __str__(self):
        return f"{self.created_at} - {self.user_id} - {self.action}"