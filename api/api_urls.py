from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.base_views import (CompanyView,
                               StudioView,
                               RecordStudioView,
                               UserSignUPView, )
from .views.stats_view import (StudioStatView,
                               CompanyStatView,
                               SingleStudioEachDayStatView,
                               EachStudioAmountView,
                               EachMonthStatView,
                               EachYearStatView
                               )

router = DefaultRouter()
router.register('companies', CompanyView, basename='companies')
router.register('studios', StudioView, basename='studios')
router.register('records', RecordStudioView, basename='records')

urlpatterns = [
    path('', include(router.urls)),
    path('sign-up/', UserSignUPView.as_view()),
    path('tokens/', TokenObtainPairView.as_view()),
    path('tokens/refresh/', TokenRefreshView.as_view()),
    path('company/stat/', CompanyStatView.as_view()),
    path('studios/<int:pk>/stat/', StudioStatView.as_view()),
    path('studios/<int:pk>/daystat/', SingleStudioEachDayStatView.as_view()),
    path('studios/<int:pk>/monthstat/', EachMonthStatView.as_view()),
    path('studios/<int:pk>/yearstat/', EachYearStatView.as_view()),
    path('studio/amount/', EachStudioAmountView.as_view()),
]
