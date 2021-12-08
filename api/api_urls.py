from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.base_views import (CompanyView,
                               StudioView,
                               RecordStudioView,
                               UserSignUPView, )
from .views.stats_view import (StudioStatView,
                               CompanyStatView,
                               EachDayStatView,
                               EachStudioAmount
                               )

router = DefaultRouter()
router.register('companies', CompanyView, basename='companies')
router.register('studios', StudioView, basename='studios')
router.register('records', RecordStudioView, basename='records')

urlpatterns = [
    path('', include(router.urls)),
    path('sign_up/', UserSignUPView.as_view()),
    path('company/stat/', CompanyStatView.as_view()),
    path('studios/<int:pk>/stat/', StudioStatView.as_view()),
    path('studios/<int:pk>/daystat/', EachDayStatView.as_view()),
    path('studio/amount/', EachStudioAmount.as_view())
]
