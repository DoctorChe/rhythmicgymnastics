from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .choices import CATEGORY


class Competition(models.Model):
    title = models.CharField(verbose_name='наименование', max_length=256)
    slug = models.SlugField(max_length=256, unique=True)
    place = models.CharField(verbose_name='место проведения соревнований', max_length=256)
    start = models.DateField(verbose_name='дата начала соревнований', auto_now_add=False)
    end = models.DateField(verbose_name='дата окончания соревнований', auto_now_add=False)
    age_from = models.CharField(max_length=4, blank=True)
    age_to = models.CharField(max_length=4, blank=True)
    organizer = models.CharField(verbose_name='организатор соревнований',
                                 max_length=256, blank=True)
    judge = models.CharField(verbose_name='судьи', max_length=256, blank=True)
    sec = models.CharField(verbose_name='секретарь', max_length=256, blank=True)
    gymnasts_are_sorted = models.BooleanField(verbose_name='жеребьёвка гимнасток проведена',
                                              default=False)
    teams_are_sorted = models.BooleanField(verbose_name='жеребьёвка команд проведена',
                                           default=False)

    class Meta:
        ordering = ('start',)
        verbose_name = 'соревнование'
        verbose_name_plural = 'соревнования'

    def __str__(self):
        return self.title

    def make_fullname(self):
        return "%s %s" % (self.start, self.title)

    make_fullname.short_description = "Полное название соревнования"
    full_name = property(make_fullname)

    def make_rank_list(self, instance):
        if type(instance) is Team:
            all_items = self.teams.all()
        else:
            all_items = self.gymnasts.all()
        dct = {item.id: item.result for item in all_items if item.result}
        import operator
        sorted_dct = sorted(dct.items(), key=operator.itemgetter(1), reverse=True)
        # if sorted_dct:
        for i, item in enumerate(sorted_dct):
            all_items.filter(id=item[0]).update(rank=i+1)

    def sortition(self):
        if not self.gymnasts_are_sorted:
            gymnast_list = list(self.gymnasts.all())
            import random
            random.shuffle(gymnast_list, random.random)
            for i, g in enumerate(gymnast_list):
                gymnast = self.gymnasts.all().filter(name=g.name)
                gymnast.update(number=i+1)
            self.gymnasts_are_sorted = True
        if not self.teams_are_sorted:
            team_list = list(self.teams.all())
            import random
            random.shuffle(team_list, random.random)
            for i, item in enumerate(team_list):
                team = self.teams.all().filter(name=item.name)
                team.update(number=i+1)
            self.teams_are_sorted = True

    def unsortition_gymnast(self):
        self.gymnasts.all().update(number=None)
        self.gymnasts_are_sorted = False
        self.save()

    def unsortition_team(self):
        self.teams.all().update(number=None)
        self.teams_are_sorted = False
        self.save()


class CommonInfo(models.Model):
    competition = models.ForeignKey(Competition, verbose_name='соревнование',
                                    related_name='%(class)ss', on_delete=models.DO_NOTHING)
    name = models.CharField(verbose_name='имя', max_length=256)
    city = models.CharField(verbose_name='город', max_length=32, blank=True)
    coach = models.CharField(verbose_name='тренер', max_length=128, blank=True)
    result = models.DecimalField(verbose_name='итог',
                                 max_digits=5, decimal_places=3, default=0, blank=False)
    number = models.PositiveIntegerField(verbose_name='порядковый номер выступления',
                                         blank=True, null=True)
    rank = models.PositiveIntegerField(verbose_name='место в зачёте',
                                       blank=True, null=True)
    # Оценка D
    tv1d = models.DecimalField(verbose_name='окончательная оценка D',
                               max_digits=5, decimal_places=3, blank=True, null=True)
    tv2d = models.DecimalField(verbose_name='окончательная оценка D',
                               max_digits=5, decimal_places=3, blank=True, null=True)
    tv3d = models.DecimalField(verbose_name='окончательная оценка D',
                               max_digits=5, decimal_places=3, blank=True, null=True)
    tv4d = models.DecimalField(verbose_name='окончательная оценка D',
                               max_digits=5, decimal_places=3, blank=True, null=True)

    # Оценка E
    tv1e = models.DecimalField(verbose_name='окончательная оценка E',
                               max_digits=5, decimal_places=3, blank=True, null=True)
    tv2e = models.DecimalField(verbose_name='окончательная оценка E',
                               max_digits=5, decimal_places=3, blank=True, null=True)
    tv3e = models.DecimalField(verbose_name='окончательная оценка E',
                               max_digits=5, decimal_places=3, blank=True, null=True)
    tv4e = models.DecimalField(verbose_name='окончательная оценка E',
                               max_digits=5, decimal_places=3, blank=True, null=True)

    score1 = models.DecimalField(verbose_name='оценка',
                                 max_digits=5, decimal_places=3, blank=True, null=True)
    score2 = models.DecimalField(verbose_name='оценка',
                                 max_digits=5, decimal_places=3, blank=True, null=True)
    score3 = models.DecimalField(verbose_name='оценка',
                                 max_digits=5, decimal_places=3, blank=True, null=True)
    score4 = models.DecimalField(verbose_name='оценка',
                                 max_digits=5, decimal_places=3, blank=True, null=True)

    result1 = models.DecimalField(verbose_name='сумма',
                                  max_digits=5, decimal_places=3, blank=True, null=True)
    result2 = models.DecimalField(verbose_name='сумма',
                                  max_digits=5, decimal_places=3, blank=True, null=True)
    result3 = models.DecimalField(verbose_name='сумма',
                                  max_digits=5, decimal_places=3, blank=True, null=True)
    result4 = models.DecimalField(verbose_name='сумма',
                                  max_digits=5, decimal_places=3, blank=True, null=True)

    pv1k = models.FloatField(verbose_name='сбавка', blank=True, null=True)
    pv2k = models.FloatField(verbose_name='сбавка', blank=True, null=True)
    pv3k = models.FloatField(verbose_name='сбавка', blank=True, null=True)
    pv4k = models.FloatField(verbose_name='сбавка', blank=True, null=True)

    # Обруч
    v1d1 = models.FloatField(verbose_name='D1/D2', blank=True, null=True)
    v1d2 = models.FloatField(verbose_name='D3/D4', blank=True, null=True)
    v1d3 = models.FloatField(blank=True, null=True)
    v1d4 = models.FloatField(blank=True, null=True)

    v1e1 = models.FloatField(verbose_name='E1/E2', blank=True, null=True)
    v1e2 = models.FloatField(verbose_name='E3', blank=True, null=True)
    v1e3 = models.FloatField(verbose_name='E4', blank=True, null=True)
    v1e4 = models.FloatField(verbose_name='E5', blank=True, null=True)
    v1e5 = models.FloatField(verbose_name='E6', blank=True, null=True)

    # Мяч
    v2d1 = models.FloatField(verbose_name='D1/D2', blank=True, null=True)
    v2d2 = models.FloatField(verbose_name='D3/D4', blank=True, null=True)
    v2d3 = models.FloatField(blank=True, null=True)
    v2d4 = models.FloatField(blank=True, null=True)

    v2e1 = models.FloatField(verbose_name='E1/E2', blank=True, null=True)
    v2e2 = models.FloatField(verbose_name='E3', blank=True, null=True)
    v2e3 = models.FloatField(verbose_name='E4', blank=True, null=True)
    v2e4 = models.FloatField(verbose_name='E5', blank=True, null=True)
    v2e5 = models.FloatField(verbose_name='E6', blank=True, null=True)

    # Булава
    v3d1 = models.FloatField(verbose_name='D1/D2', blank=True, null=True)
    v3d2 = models.FloatField(verbose_name='D3/D4', blank=True, null=True)
    v3d3 = models.FloatField(blank=True, null=True)
    v3d4 = models.FloatField(blank=True, null=True)

    v3e1 = models.FloatField(verbose_name='E1/E2', blank=True, null=True)
    v3e2 = models.FloatField(verbose_name='E3', blank=True, null=True)
    v3e3 = models.FloatField(verbose_name='E4', blank=True, null=True)
    v3e4 = models.FloatField(verbose_name='E5', blank=True, null=True)
    v3e5 = models.FloatField(verbose_name='E6', blank=True, null=True)

    # Лента
    v4d1 = models.FloatField(verbose_name='D1/D2', blank=True, null=True)
    v4d2 = models.FloatField(verbose_name='D3/D4', blank=True, null=True)
    v4d3 = models.FloatField(blank=True, null=True)
    v4d4 = models.FloatField(blank=True, null=True)

    v4e1 = models.FloatField(verbose_name='E1/E2', blank=True, null=True)
    v4e2 = models.FloatField(verbose_name='E3', blank=True, null=True)
    v4e3 = models.FloatField(verbose_name='E4', blank=True, null=True)
    v4e4 = models.FloatField(verbose_name='E5', blank=True, null=True)
    v4e5 = models.FloatField(verbose_name='E6', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    # def calc_position(self):
    #     sorted_dct = self.competition.make_rank_list(self)
    #     if sorted_dct:
    #         for i, k in enumerate(sorted_dct):
    #             # if k[0] == self.name:
    #             if k[0] == self.id:
    #                 print(k)
    #                 return i+1
    #     return None
    #
    # calc_position.short_description = "место в зачёте"
    # rank_position = property(calc_position)

    def calc_result(self, *args):
        lst = [item for item in args if item]
        return sum(lst) if lst else None

    def make_tv_d(self, *args):
        lst = [item for item in args if item]
        return sum(lst) if lst else None

    # result_e = {
    #     0: lambda x: None,
    #     1: lambda x: sum(x),
    #     2: lambda x: sum(x) / 2,
    #     3: lambda x: sum(x) - (min(x) + max(x)),
    #     4: lambda x: (sum(x) - (min(x) + max(x))) / 2,
    #     5: lambda x: (sum(x) - (min(x) + max(x))) / 3
    # }
    #
    # def make_tv_e(self, *args):
    #     lst1 = []
    #     i = 0
    #     for item in args:
    #         if item:
    #             i = i + 1
    #             lst1.append(item)
    #     return self.result_e[i](lst1)

    def make_tv_e(self, *args):
        if list(filter(lambda x: x is not None, args)):
            lst = []
            for item in args:
                if item:
                    lst.append(item)
                else:
                    lst.append(0)
                    print(item)
            return 10 - (lst[0] + (sum(lst[1:]) - (min(lst[1:]) + max(lst[1:])))/2)
        else:
            return None

    def calc_total_score(self, *args):
        lst = [item for item in args if item]
        return sum(lst) if lst else None

    def calc_total_result(self, score, penalty):
        if score and penalty:
            res = score - penalty
        elif score and not penalty:
            res = score
        else:
            res = None
        return res


class Team(CommonInfo):

    class Meta:
        verbose_name = 'команда'
        verbose_name_plural = 'команды'


class TeamGymnast(models.Model):
    team = models.ForeignKey(Team, verbose_name='команда',
                             related_name='team_gymnasts', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя гимнастки', max_length=256)

    class Meta:
        verbose_name = 'гимнастка'
        verbose_name_plural = 'гимнастки'

    def __str__(self):
        return self.name


class Gymnast(CommonInfo):
    year_of_birth = models.PositiveIntegerField(verbose_name='год рождения',
                                                validators=[MinValueValidator(2000),
                                                            MaxValueValidator(2018)])
    category = models.CharField(max_length=5,
                                verbose_name='разряд',
                                choices=CATEGORY,
                                blank=True)

    class Meta:
        verbose_name = 'гимнастка'
        verbose_name_plural = 'гимнастки'

    # def was_ranked(self):
    #     return self.rank_position is not None
    #
    # was_ranked.admin_order_field = 'rank_position'
    # was_ranked.boolean = True
    # was_ranked.short_description = 'Посчитано место в зачёте?'

    # def get_category_display(self):
    #     for cat in CATEGORY:
    #         if cat[0] == self.category:
    #             return cat[1]
