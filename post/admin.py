from django.contrib import admin

from .models import Post, Team, Contact, Services, Laws, ServiceCategory

from django.utils.html import format_html


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['status', 'publish']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'role']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_filter = ['Status']
    list_display = ['name', 'services', 'phone', 'created_at', 'status', '_']
    search_fields = ['name', 'services', 'Status']
    list_per_page = 6

    def _(self, obj):
        if obj.Status == 'Read':
            return True
        else:
            return False

    _.boolean = True

    def status(self, obj):
        if obj.Status == 'Read':
            color = '#80c904'
        else:
            color = 'red'
        return format_html('<strong><p style="color:{}>{}</p></strong>'.format(color, obj.Status))

    status.allow_tags = True


@admin.register(Services)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ServiceCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Laws)
class LawsAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}
