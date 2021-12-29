from datetime import datetime
from django.db.models import Sum, Avg, Max, F, DateField
from django.db.models.functions import (TruncDay,
                                        ExtractMonth,
                                        ExtractYear)
from rest_framework import response
from .mixins import OwnerMixin
from ..serializers import RecordMonthSerializer, RecordYearSerializer


class CompanyStatView(OwnerMixin):

    def get(self, request):
        company_stat = self.get_queryset().aggregate(total_amount=Sum('session_cost'),
                                                     max_cost=Max('cost'),
                                                     avg_cost=Avg('cost'),
                                                     avg_session_cost=Avg('session_cost'),
                                                     max_duration=Max('duration'),
                                                     avg_duration=Avg('duration'))
        company_stat['max_duration'] = str(company_stat['max_duration']).split('.')[0]
        company_stat['avg_duration'] = str(company_stat['avg_duration']).split('.')[0]
        return response.Response(company_stat)

    def get_view_name(self):
        return f'Статистика компании'


class StudioStatView(OwnerMixin):

    def get(self, request, pk):
        studio_stat = super().get_queryset().filter(studio_id=pk) \
            .aggregate(total_amount=Sum('session_cost'),
                       max_cost=Max('cost'),
                       avg_cost=Avg('cost'),
                       avg_session_cost = Avg('session_cost'),
                       max_duration=Max('duration'),
                       avg_duration=Avg('duration'))
        studio_stat['max_duration'] = str(studio_stat['max_duration']).split('.')[0]
        studio_stat['avg_duration'] = str(studio_stat['avg_duration']).split('.')[0]
        return response.Response(studio_stat)

    def get_view_name(self):
        return f'Статистика по студии'


class EachStudioAmountView(OwnerMixin):

    def get(self, request):
        each_studio_amount = self.get_queryset(). \
            values(label=F('studio__name')).annotate(value=Sum('session_cost'))
        return response.Response(each_studio_amount)

    def get_view_name(self):
        return f'Суммарный доход каждой студии за все время'


class SingleStudioEachDayStatView(OwnerMixin):

    def get(self, request, pk):
        each_day_amount = super().get_queryset().filter(studio_id=pk). \
            values(label=TruncDay('start_recording', output_field=DateField())).\
            annotate(value=Sum('session_cost'))
        return response.Response(each_day_amount)

    def get_view_name(self):
        return f'Суммарный доход студии ежедневно'


class EachMonthStatView(OwnerMixin):

    def get(self, request, pk):
        current = datetime.now().year
        each_month_amount = self.get_queryset().filter(studio_id=pk,
                                                       start_recording__year=current). \
            annotate(label=ExtractMonth('start_recording')). \
            values('label').annotate(value=Sum('session_cost'))
        serializer = RecordMonthSerializer(each_month_amount, many=True)
        return response.Response(serializer.data)

    def get_view_name(self):
        return f'Суммарный доход студии ежемесячно за текущий год'


class EachYearStatView(OwnerMixin):

    def get(self, request, pk):
        each_year_amount = self.get_queryset().filter(studio_id=pk). \
            annotate(label=ExtractYear('start_recording')). \
            values('label').annotate(value=Sum('session_cost'))
        serializer = RecordYearSerializer(each_year_amount, many=True)
        return response.Response(serializer.data)

    def get_view_name(self):
        return f'Суммарный доход студии ежегодно'
