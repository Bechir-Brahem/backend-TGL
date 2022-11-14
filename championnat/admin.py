from django.contrib import admin

from .models import Game, League, Player, Team, GameComment

admin.site.site_header = 'Tunisia Golden League Administration'
admin.site.site_title = 'Tunisia Golden League Administration'
admin.site.index_title = 'Tunisia Golden League Administration'

admin.site.register(League, list_display=['abbreviation', 'name'])


class PlayerInline(admin.TabularInline):
    model = Player


class GameCommentInline(admin.TabularInline):
    template = 'admin/championnat/game/edit_inline/tabular.html'
    model = GameComment
    extra = 1


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('league', 'homeTeam', 'awayTeam', 'homeTeamScore', 'awayTeamScore')
    inlines = [GameCommentInline]


class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = ['image_tag', 'name', 'points', 'league']
    inlines = [PlayerInline]
    change_form_template = 'admin/championnat/game/change_form.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['banana'] = 'aaa'
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


admin.site.register(Team, TeamAdmin)

#
# @admin.register(Game)
# class Model1Admin(admin.ModelAdmin):
#
#     def image_tag(self, obj):
#         return format_html('<img src="{}" />'.format(obj.image.url))
#
#     image_tag.short_description = 'Image'


# Register your models here.
