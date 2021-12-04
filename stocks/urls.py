from django.urls import path, re_path, include

from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'stocks'

urlpatterns = [

    path('stock', views.StockViewSet.as_view({
        'get': 'get_all_stock',
        'post': 'create'
    })),
    re_path('^stock/(?P<code>\w+)', views.StockViewSet.as_view({
        'get': 'get_stock',
        'put': 'update',
        'delete': 'delete'
    })),
    path('historicalstock', views.HistoricalStockViewSet.as_view({
        'post': 'create_historical'
    })),
    re_path('^historicalstock/(?P<code>\w+)$', views.HistoricalStockViewSet.as_view({
        'get': 'get_all_historical_stock',
    })),
    re_path('^historicalstock/(?P<code>\w+)/date/(?P<date>\d{4}-\d{2}-\d{2})', views.HistoricalStockViewSet.as_view({
            'get': 'get_historical_stock_by_date',
            'put': 'update',
            'delete': 'delete'
    })),
    re_path('^get_external_historical', views.ScheduleGetHistorical.as_view({
        'post': 'get_external_historical'
    }))
]