from rest_framework import serializers
from .models import Stock, HistoricalStock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields= '__all__'

class HistoricalStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalStock
        fields= '__all__'