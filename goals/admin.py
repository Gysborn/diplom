from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user__username")


class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'status', 'priority')
    list_display_links = ('title',)
    search_fields = ('title', 'description')
    list_filter = ('status', 'priority')
    readonly_fields = ('created', 'updated',)


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text',)
    readonly_fields = ('created', 'updated',)


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_deleted',)
    readonly_fields = ('created', 'updated',)


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('board', 'user', 'role')
    readonly_fields = ('created', 'updated',)


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardParticipant, BoardParticipantAdmin)
