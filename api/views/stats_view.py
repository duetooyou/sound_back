from django.db.models import Sum, Avg, Max, F, DateField, DurationField
from django.db.models.functions import TruncDay, Cast
from rest_framework import response
from .mixins import OwnerMixin
from ..models import Record


class CompanyStatView(OwnerMixin):

    def get(self, request):
        company_stat = self.get_queryset().aggregate(total_amount=Sum('session_cost'),
                                                     max_cost=Max('cost'),
                                                     avg_cost=Avg('cost'),
                                                     max_duration=Max('duration'),
                                                     avg_duration=Avg('duration'))
        company_stat['max_duration'] = str(company_stat['max_duration'])
        company_stat['avg_duration'] = str(company_stat['avg_duration'])
        return response.Response(company_stat)

    def get_view_name(self):
        return f'Статистика компании'


class StudioStatView(OwnerMixin):

    def get(self, request, pk):
        studio_stat = super().get_queryset().filter(studio_id=pk) \
            .aggregate(average_cost=Avg('cost'),
                       max_cost=Max('cost'),
                       max_duration=Max('duration', output_field=DurationField()),
                       total_cost=Sum('session_cost'))
        studio_stat['max_duration'] = str(studio_stat['max_duration'])
        studio_stat['avg_duration'] = str(studio_stat['avg_duration'])
        return response.Response(studio_stat)

    def get_view_name(self):
        return f'Статистика по студии'


class EachStudioAmount(OwnerMixin):

    def get(self, request):
        each_studio_amount = Record.objects.\
            values(label=F('studio__name')).annotate(value=Sum('session_cost'))
        print(self.request.user)
        return response.Response(each_studio_amount)

    def get_view_name(self):
        return f'Суммарный доход каждой студии за все время'


class SingleStudioEachDayStatView(OwnerMixin):

    def get(self, request, pk):
        each_day_amount = super().get_queryset().filter(studio_id=pk).\
            values(label=Cast(TruncDay('start_recording'), output_field=DateField())).\
            annotate(value=Sum('session_cost'))
        return response.Response(each_day_amount)

    def get_view_name(self):
        return f'Суммарный доход студии ежедневно'


class EachMonthStatView(OwnerMixin):

    def get(self, request): pass
