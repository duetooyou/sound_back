from datetime import datetime, date
from django.db.models import Sum, Avg, Max, F
from django.db.models.functions import TruncDay
from rest_framework import (views,
                            response,
                            )
from ..models import Record


class OwnerMixin(views.APIView):
    def get_queryset(self):
        return Record.objects.filter(studio__company__owner=self.request.user)


class CompanyStatView(OwnerMixin):
    def get(self, request):
        company_stat = self.get_queryset().aggregate(total_amount=Sum('session_cost'),
                                                     max_cost=Max('cost'),
                                                     avg_cost=Avg('cost'),
                                                     duration=Max('duration'),
                                                     )
        return response.Response(company_stat)

    def get_view_name(self):
        return f'Статистика компании'


class StudioStatView(OwnerMixin):
    def get(self, request, pk):
        queryset = super().get_queryset().filter(studio_id=pk)
        cost_stat = queryset.aggregate(average_cost=Avg('cost'),
                                       max_cost=Max('cost'),
                                       max_duration=Max('duration'),
                                       total_cost=Sum('session_cost'))
        return response.Response(cost_stat)

    def get_view_name(self):
        return f'Статистика по студии'


class EachStudioAmount(OwnerMixin):

    def get(self, request):
        each_studio_amount = self.get_queryset().values(label=F('studio__name')).\
            annotate(summa=Sum('session_cost'))
        return response.Response(each_studio_amount)


class EachDayStatView(OwnerMixin):

    def get(self, request, pk):
        result = self.get_queryset().filter(studio_id=pk).\
            annotate(day=TruncDay('start_recording')).values('day').\
            aggregate(label=Sum('session_cost'))
        return response.Response(result)


class EachMonthStatView(OwnerMixin):
    def get(self, request): pass
