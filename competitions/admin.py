from django.contrib import admin
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.forms import TextInput, NumberInput

from .models import Competition, Gymnast, Team, TeamGymnast


class TeamGymnastInline(admin.StackedInline):
    model = TeamGymnast
    extra = 0


# @receiver(pre_save, sender=Competition)
# def sortition(sender, instance, **kwargs):
#     instance.sortition()


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'full_name', 'place', 'gymnasts_are_sorted', 'teams_are_sorted']
    list_filter = ['place', ]
    search_fields = ['title', 'place']
    fieldsets = [
        (None, {'fields': [('title', 'slug'), 'full_name']}),
        (None, {'fields': [('place', ),
                           ('start', 'end', ),
                           # ('age_from', 'age_to',),
                           ('organizer', 'sec', ),
                           # 'judge',
                           ]}),
        ('Дополнительная информация', {
            'fields': [
                'gymnasts_are_sorted',
                'teams_are_sorted',
                ],
        }),
    ]
    prepopulated_fields = {'slug': ('title',)}
    save_as = True  # Включить возможность “сохранять как” на странице редактирования объекта (сохранит с новым ID)
    readonly_fields = ('full_name',
                       'gymnasts_are_sorted',
                       'teams_are_sorted'
                       )
    date_hierarchy = 'start'  # Отображение дат

    def make_sorted(self, request, queryset):
        for obj in queryset:
            obj.sortition()
            obj.save()
    make_sorted.short_description = "Провести жеребьёвку"

    actions = [make_sorted]


@receiver(post_save, sender=Gymnast)
def make_rank_list_gymnast(sender, instance, created, **kwargs):
    instance.competition.make_rank_list(instance)


@receiver(post_save, sender=Gymnast)
def make_non_sorted_gymnasts_add(sender, instance, created, **kwargs):
    if created:
        instance.competition.unsortition_gymnast()


@receiver(post_delete, sender=Gymnast)
def make_non_sorted_gymnasts_delete(sender, instance, **kwargs):
    instance.competition.unsortition_gymnast()


@receiver(pre_save, sender=Gymnast)
def calc_gymnast_results(sender, instance, **kwargs):
    if (instance.v1d1 or instance.v1d2 or
            instance.v1e1 or instance.v1e2 or instance.v1e3 or
            instance.v1e4 or instance.v1e5 or
            instance.v2d1 or instance.v2d2 or
            instance.v2e1 or instance.v2e2 or instance.v2e3 or
            instance.v2e4 or instance.v2e5 or
            instance.v3d1 or instance.v3d2 or
            instance.v3e1 or instance.v3e2 or instance.v3e3 or
            instance.v3e4 or instance.v3e5 or
            instance.v4d1 or instance.v4d2 or
            instance.v4e1 or instance.v4e2 or instance.v4e3 or
            instance.v4e4 or instance.v4e5):
        instance.tv1d = instance.make_tv_d(instance.v1d1,
                                           instance.v1d2)
        instance.tv1e = instance.make_tv_e(instance.v1e1,
                                           instance.v1e2,
                                           instance.v1e3,
                                           instance.v1e4,
                                           instance.v1e5)
        instance.tv2d = instance.make_tv_d(instance.v2d1,
                                           instance.v2d2)
        instance.tv2e = instance.make_tv_e(instance.v2e1,
                                           instance.v2e2,
                                           instance.v2e3,
                                           instance.v2e4,
                                           instance.v2e5)
        instance.tv3d = instance.make_tv_d(instance.v3d1,
                                           instance.v3d2)
        instance.tv3e = instance.make_tv_e(instance.v3e1,
                                           instance.v3e2,
                                           instance.v3e3,
                                           instance.v3e4,
                                           instance.v3e5)
        instance.tv4d = instance.make_tv_d(instance.v4d1,
                                           instance.v4d2)
        instance.tv4e = instance.make_tv_e(instance.v4e1,
                                           instance.v4e2,
                                           instance.v4e3,
                                           instance.v4e4,
                                           instance.v4e5)
        instance.score1 = instance.calc_total_score(instance.tv1d,
                                                    instance.tv1e)
        instance.score2 = instance.calc_total_score(instance.tv2d,
                                                    instance.tv2e)
        instance.score3 = instance.calc_total_score(instance.tv3d,
                                                    instance.tv3e)
        instance.score4 = instance.calc_total_score(instance.tv4d,
                                                    instance.tv4e)
        instance.result1 = instance.calc_total_result(instance.score1,
                                                      instance.pv1k)
        instance.result2 = instance.calc_total_result(instance.score2,
                                                      instance.pv2k)
        instance.result3 = instance.calc_total_result(instance.score3,
                                                      instance.pv3k)
        instance.result4 = instance.calc_total_result(instance.score4,
                                                      instance.pv4k)
        instance.result = instance.calc_result(instance.result1,
                                               instance.result2,
                                               instance.result3,
                                               instance.result4)


@admin.register(Gymnast)
class GymnastAdmin(admin.ModelAdmin):
    list_display = ['competition',
                    'name', 'year_of_birth', 'category', 'city', 'coach',
                    'number',
                    'rank',
                    ]
    list_display_links = ('name',)
    list_filter = ['competition', 'number', 'category', 'city', ]
    search_fields = ['name', ]
    fieldsets = [
        (None, {'fields': ['competition', ]}),
        (None, {'fields': [('name', 'category', 'year_of_birth',),
                           ('city', 'coach',),
                           ]}),
        ('Дополнительная информация', {
            'fields': [(
                'number',
                'result',
                # 'rank_position',
                'rank',
            )],
        }),
        ('Результаты', {
            'fields': [],
            # 'classes': ('wide', 'extrapretty'),
             }),
        ('Обруч', {
            'classes': ('collapse',),
            'fields': [
                ('v1d1', 'v1d2',),
                ('v1e1', 'v1e2', 'v1e3', 'v1e4', 'v1e5',),
                ('tv1d', 'tv1e', 'score1',),
                ('pv1k', 'result1',),
                ]}),
        ('Мяч', {
            'classes': ('collapse',),
            'fields': [
                ('v2d1', 'v2d2',),
                ('v2e1', 'v2e2', 'v2e3', 'v2e4', 'v2e5',),
                ('tv2d', 'tv2e', 'score2',),
                ('pv2k', 'result2',),
                ]}),
        ('Булава', {
            'classes': ('collapse',),
            'fields': [
                ('v3d1', 'v3d2',),
                ('v3e1', 'v3e2', 'v3e3', 'v3e4', 'v3e5',),
                ('tv3d', 'tv3e', 'score3',),
                ('pv3k', 'result3',),
                ]}),
        ('Лента', {
            'classes': ('collapse',),
            'fields': [
                ('v4d1', 'v4d2',),
                ('v4e1', 'v4e2', 'v4e3', 'v4e4', 'v4e5',),
                ('tv4d', 'tv4e', 'score4',),
                ('pv4k', 'result4',),
                ]}),
    ]
    formfield_overrides = {
        models.FloatField: {'widget': NumberInput(attrs={'size': '5', 'min': '0', 'max': '10', 'step': '0.1'})},
        models.CharField: {'widget': TextInput(attrs={'size': '15'})},
    }
    readonly_fields = (
        'tv1d', 'tv1e',
        'tv2d', 'tv2e',
        'tv3d', 'tv3e',
        'tv4d', 'tv4e',
        'score1', 'score2', 'score3', 'score4',
        'result1', 'result2', 'result3', 'result4',
        'result',
        # 'rank_position',
        'rank',
        'number',
    )


@receiver(post_save, sender=Team)
def make_rank_list_team(sender, instance, created, **kwargs):
    instance.competition.make_rank_list(instance)


@receiver(post_save, sender=Team)
def make_non_sorted_teams_add(sender, instance, created, **kwargs):
    if created:
        instance.competition.unsortition_team()


@receiver(post_delete, sender=Team)
def make_non_sorted_teams_delete(sender, instance, **kwargs):
    instance.competition.unsortition_team()


@receiver(pre_save, sender=Team)
def calc_team_results(sender, instance, **kwargs):
    if (instance.v1d1 or instance.v1d2 or
            instance.v1e1 or instance.v1e2 or instance.v1e3 or
            instance.v1e4 or instance.v1e5 or
            instance.v2d1 or instance.v2d2 or
            instance.v2e1 or instance.v2e2 or instance.v2e3 or
            instance.v2e4 or instance.v2e5):
        instance.tv1d = instance.make_tv_d(instance.v1d1,
                                           instance.v1d2)
        instance.tv1e = instance.make_tv_e(instance.v1e1,
                                           instance.v1e2,
                                           instance.v1e3,
                                           instance.v1e4,
                                           instance.v1e5)
        instance.tv2d = instance.make_tv_d(instance.v2d1,
                                           instance.v2d2)
        instance.tv2e = instance.make_tv_e(instance.v2e1,
                                           instance.v2e2,
                                           instance.v2e3,
                                           instance.v2e4,
                                           instance.v2e5)
        instance.score1 = instance.calc_total_score(instance.tv1d,
                                                    instance.tv1e)
        instance.score2 = instance.calc_total_score(instance.tv2d,
                                                    instance.tv2e)
        instance.result1 = instance.calc_total_result(instance.score1,
                                                      instance.pv1k)
        instance.result2 = instance.calc_total_result(instance.score2,
                                                      instance.pv2k)
        instance.result = instance.calc_result(instance.result1,
                                               instance.result2)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['competition',
                    'name', 'city', 'coach',
                    'number',
                    'rank',
                    ]
    list_display_links = ('name',)
    list_filter = ['competition', 'number', 'city', ]
    search_fields = ['name', ]
    fieldsets = [
        (None, {'fields': ['competition', ]}),
        (None, {'fields': [('name', 'city', 'coach',), ]}),
        ('Дополнительная информация', {
            'fields': [(
                'number',
                'result',
                # 'rank_position',
                'rank',
            )],
        }),
        ('Результаты', {
            'fields': [],
            # 'classes': ('wide', 'extrapretty'),
             }),
        ('1 вид', {
            'classes': ('collapse',),
            'fields': [
                ('v1d1', 'v1d2',),
                ('v1e1', 'v1e2', 'v1e3', 'v1e4', 'v1e5',),
                ('tv1d', 'tv1e', 'score1',),
                ('pv1k', 'result1',),
                ]}),
        ('2 вид', {
            'classes': ('collapse',),
            'fields': [
                ('v2d1', 'v2d2',),
                ('v2e1', 'v2e2', 'v2e3', 'v2e4', 'v2e5',),
                ('tv2d', 'tv2e', 'score2',),
                ('pv2k', 'result2',),
                ]}),
    ]
    formfield_overrides = {
        models.FloatField: {'widget': NumberInput(attrs={'size': '5', 'min': '0', 'max': '10', 'step': '0.1'})},
        models.CharField: {'widget': TextInput(attrs={'size': '15'})},
        # models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    readonly_fields = (
        'tv1d', 'tv1e',
        'tv2d', 'tv2e',
        'score1', 'score2',
        'result1', 'result2',
        'result',
        # 'rank_position',
        'rank',
        'number',
    )
    # ordering = ('rank', )
    inlines = [TeamGymnastInline, ]
