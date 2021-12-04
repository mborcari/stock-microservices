from datetime import date, timedelta

def get_validate_business_data(data):
    """
        Verify next business data consideing holydays

    Args:
        data ([data]): [date]

    Returns:
        [data]: [data after calcule business data]
    """

    lista_feriados = ( '25/01', '15/02','16/02', '02/04', '10/04',
                        '21/04','01/05', '03/06', '09/07', '07/09',
                        '12/10', '02/11', '15/11', '24/12', '25/12',
                        '31/12', '01/01')
    while True:
        if data.weekday() != 6 and data.weekday() != 5 and data.strftime('%d/%m') not in lista_feriados:
            return data
        data = data - timedelta(days=1)