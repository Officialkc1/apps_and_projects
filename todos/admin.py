from django.contrib import admin

from todos.models import Todo
from .models import Todo

# Register your models here.
# admin.site.register(Todo)
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id','title','body']
    search_field = ['title', 'id']

