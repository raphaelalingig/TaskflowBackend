from django.contrib import admin
from api.models import User,Profile, Task, Project, Group, GroupNprojectAssoc


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['user', 'full_name' ,'verified']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_name','start_date', 'due_date']

class TaskAdmin(admin.ModelAdmin):
    list_editable = ['assignee']
    list_display = ['task_name', 'start_date', 'due_date', 'assignee']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']

class GroupNprojectAssocAdmin(admin.ModelAdmin):
    list_display = ['group']

admin.site.register(User, UserAdmin)
admin.site.register( Profile,ProfileAdmin)
admin.site.register( Task, TaskAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupNprojectAssoc, GroupNprojectAssocAdmin)


