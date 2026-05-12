from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Step, Level, Question, UserProgress, BotLog

class LevelInline(admin.TabularInline):
    model = Level
    extra = 1
    show_change_link = True

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ['step_number', 'title', 'get_levels_count', 'get_questions_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    inlines = [LevelInline]
    
    def get_levels_count(self, obj):
        return obj.get_level_count()
    get_levels_count.short_description = "Levels"
    
    def get_questions_count(self, obj):
        return obj.get_question_count()
    get_questions_count.short_description = "Questions"

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['get_step', 'level_number', 'title', 'get_questions_count', 'created_at']
    list_filter = ['step', 'created_at']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]
    raw_id_fields = ['step']
    
    def get_step(self, obj):
        return format_html('<a href="{}">Step {}</a>', 
                          reverse('admin:courses_step_change', args=[obj.step.id]),
                          obj.step.step_number)
    get_step.short_description = "Step"
    
    def get_questions_count(self, obj):
        return obj.get_question_count()
    get_questions_count.short_description = "Questions"

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['get_full_ref', 'question_text_short', 'answer_preview', 'has_hint', 'created_at']
    list_filter = ['level__step', 'level', 'created_at']
    search_fields = ['question_text', 'answer', 'tags']
    raw_id_fields = ['level']
    
    def get_full_ref(self, obj):
        return obj.get_full_reference()
    get_full_ref.short_description = "Location"
    
    def question_text_short(self, obj):
        return obj.question_text[:100] + '...' if len(obj.question_text) > 100 else obj.question_text
    question_text_short.short_description = "Question"
    
    def answer_preview(self, obj):
        return obj.answer[:100] + '...' if len(obj.answer) > 100 else obj.answer
    answer_preview.short_description = "Answer Preview"
    
    def has_hint(self, obj):
        return bool(obj.hint)
    has_hint.boolean = True
    has_hint.short_description = "Has Hint"
    
    fieldsets = (
        ('Location', {
            'fields': ('level', 'question_number')
        }),
        ('Content', {
            'fields': ('question_text', 'answer', 'hint', 'tags')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'step', 'level', 'completed_questions_count', 'last_active']
    list_filter = ['step', 'level', 'last_active']
    search_fields = ['user_id']
    raw_id_fields = ['step', 'level', 'last_question']
    filter_horizontal = ['completed_questions']
    
    def completed_questions_count(self, obj):
        return obj.completed_questions.count()
    completed_questions_count.short_description = "Completed Questions"

@admin.register(BotLog)
class BotLogAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'user_id', 'action', 'message_preview']
    list_filter = ['action', 'created_at']
    search_fields = ['user_id', 'message', 'response']
    readonly_fields = ['created_at']
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = "Message"