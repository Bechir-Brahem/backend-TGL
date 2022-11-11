from django.contrib import admin
from .models import Game, Team,League

admin.site.register(Game)
admin.site.register(League)
admin.site.register(Team, list_display=['image_tag','get_name','get_points'])

#
# @admin.register(Game)
# class Model1Admin(admin.ModelAdmin):
#
#     def image_tag(self, obj):
#         return format_html('<img src="{}" />'.format(obj.image.url))
#
#     image_tag.short_description = 'Image'


# Register your models here.
