import json
from datetime import datetime, date
from .models import Stock, HistoricalStock
from rest_framework import viewsets, status
from rest_framework.response import Response
from .producer import publish
from .seriealizers import StockSerializer
from .seriealizers import HistoricalStockSerializer


class StockViewSet(viewsets.ViewSet):

    def get_all_stock(self, request):
        """
            GET /api/stock
        """
        stocks = Stock.objects.all()
        seriealizer = StockSerializer(stocks, many=True)
        return Response(seriealizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
            POST /api/stock
        """
        serializer = StockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_stock(self, request, code=None):
        """
            GET /api/stock/<str:id>
        """
        stock = Stock.objects.get(code=code)
        serializer = StockSerializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, code=None):
        """
            PUT /api/stock/<str:id>
        """
        stock = Stock.objects.get(code=code)
        serializer = StockSerializer(instance=stock, data=request.data, required=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, code=None):
        """
            DELETE /api/stock/<str:id>
        """
        stock = Stock.objects.get(code=code)
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HistoricalStockViewSet(viewsets.ViewSet):

    def get_all_historical_stock(self, request, code=None):
        """
            GET /api/HistoricalStock/<str:id>

            args:
                code(str) = code stock
        """
        stock_instance = Stock.objects.get(code=code)
        historical_stock_data = HistoricalStock.objects.filter(stock_pk=stock_instance)
        if historical_stock_data:
            seriealizer = HistoricalStockSerializer(historical_stock_data, many=True)
            return Response(seriealizer.data, status=status.HTTP_200_OK)
        else:
            return Response(f'There is no historical to {code}', status=status.HTTP_200_OK)


    def create_historical(self, request):
        """
            POST /api/HistoricalStock
        """
        serializer = HistoricalStockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_historical_stock_by_date(self, request, code=None, date=None):
        """
            GET /api/HistoricalStock/<str:id>/date/<str:date>

            args:
                code(str) = code stock
                date(str) = date day
        """

        stock_instance = Stock.objects.get(code=code)
        date = datetime.strftime(date, '%Y-%m-%d').date()
        if HistoricalStock.objects.get(stock_pk=stock_instance,date=date).exists():
            print("existe!")
            historical_stock_instance = HistoricalStock.objects.get(
                                        stock_pk=stock_instance,
                                        date=date)
            serializer = HistoricalStockSerializer(historical_stock_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(f'No found historical with date {date}', status=status.HTTP_404_NOT_FOUND)


    def update(self, request, code=None, date=None):
        """
             PUT /api/HistoricalStock/<str:id>/date/<str:date>
        """

        date = datetime.strftime(date, '%Y-%m-%d').date()

        if HistoricalStock.objects.get(code=code, date=date).exists():
            historical_stock_instance = HistoricalStock.objects.get(code=code, date=date)
            serializer = HistoricalStockSerializer(instance=historical_stock_instance,
                                                   data=request.data, required=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(f'No found historical with date {date}', status=status.HTTP_404_NOT_FOUND)

    def delete(self, code=None, date=None):
        """
         DELETE /api/HistoricalStock/<str:id>/date/<str:date>
        """
        historical_stock_instance = HistoricalStock.objects.get(code=code, date=date)
        historical_stock_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ScheduleGetHistorical(viewsets.ViewSet):
    def get_external_historical(self, request):
        data = request.data
        code_stock = data['code_stock']
        stock_instance = Stock.objects.get(code=code_stock)
        if stock_instance:
            data["data_source"] = stock_instance.data_source
        data = json.dumps(data)
        publish(data)
        return Response('Get extenal historical with success', status=status.HTTP_201_CREATED)


def load_data_historical(dict_data):
    print('Salvando dados')
    flag_debug = 0
    try:
        code_stock = dict_data['code_stock']
        stock_instance = Stock.objects.get(code=code_stock)
        for date, values in dict_data['data'].items():
            date = datetime.strptime(date, '%d-%m-%Y').date()
            open_value = values['open']
            close_value = values['close']
            low_value = values['low']
            high_value = values['high']
            volume_dialy = values['volume']

            if flag_debug == 1:
                print("stock_instance", stock_instance)
                print("Date:", date)
                print("Open", open_value)
                print("Close", close_value)
                print("Low", low_value)
                print("High", high_value)
                print("Volume", volume_dialy)
            # Se o historico do ativo já existe pela data informada, somente o atualiza.
            if HistoricalStock.objects.filter(stock_pk=stock_instance, date=date).exists():
                if flag_debug == 1:
                    print(f'Has historical by date: {date}')
                try:
                    historical_stock_instance = HistoricalStock.objects.get(
                        stock_pk=stock_instance,
                        date=date)
                    historical_stock_instance.open_value = open_value
                    historical_stock_instance.close_value = close_value
                    historical_stock_instance.low_value = low_value
                    historical_stock_instance.high_value = high_value
                    historical_stock_instance.volume_dialy = volume_dialy
                    historical_stock_instance.save()
                    if flag_debug == 1:
                        print("Registro do ativo %s atualizado com sucesso, data %s"
                              % (stock_instance.code, date))
                except Exception as e:
                    print(e)
                    print("Falha ao salvar atualizar registro do ativo %s, data %s" % (
                        stock_instance.code, date)
                          )
                    continue
            else:
                if flag_debug == 1:
                    print(f'Try save new historical by date: {date}')
                try:
                    object_temp = HistoricalStock(
                        stock_pk=stock_instance,
                        date=date,
                        open_value=open_value,
                        close_value=close_value,
                        low_value=low_value,
                        high_value=high_value,
                        volume_dialy=volume_dialy
                    )
                    if flag_debug == 1:
                        print("object_temp", object_temp.__dict__)
                    object_temp.save()
                    if flag_debug == 1:
                        print("Novo registro do %s salvo com sucesso, data %s" % (code_stock, date))
                except Exception as e:
                    print(e)
                    print("Falha ao salvar novo registro do ativo %s, data %s" % (code_stock, date))
                    continue
    except KeyError as e:
        print(f'Erro de chave no dicionário: {dict_data}, error:', e)
    except Exception as e:
        print(e)
        print("Falha ao processa dados enviados")
