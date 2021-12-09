from rest_framework.views import APIView
from ..models import Record


class OwnerMixin(APIView):
    def get_queryset(self):
        return Record.objects.filter(studio__company__owner=self.request.user)
