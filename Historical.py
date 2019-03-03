import requests
import os
class Historical:
    def __init__(self, init_date, end_date = None, res_path = 'Historical_data'):
        '''
        Esta clase te permite DESCARGAR EN TU COMPUTADORA los registros historicos de ECOBICI CDMX en formato .csv.
        Estos reportes se publican mensualmente, asi que las consultas solo necesitan año y mes. Usualmente estos reportes teinen un
        retraso de dos meses, por ejemplo, si estamos en Marzo 2019 el reporte mas actual es Enero 2019.

         Inputs
        -------
        init_date: str
            En formato YYYYMM, el mes en el que se quiere comenzar la descarga de informacion.
            Si solo quiere descargar los historicos de un mes, este es el unico parametro que necesita.
        end_date: str
            Ultimo mes a ser descargado.
        res_path: Ruta en donde se colocara cada uno de los reportes mensuales.

         Returns
        ---------
        None.
        Esta funcion no regresa nada. En su lugar crea los arhcivos en tu computadora.

        '''
        if end_date == None:
            end_date = init_date
        self.init_date = init_date
        self.end_date = end_date
        self.res_path = res_path
    def _make_url(self,data_point):
        '''
        Funcion para crear la url a la que se hara la consulta.
        '''
        yyyy = data_point[0]
        mm = '{:02d}'.format(data_point[1])
        url = f'https://www.ecobici.cdmx.gob.mx/sites/default/files/data/usages/{yyyy}-{mm}.csv'
        return url
    def _iterate_dates(self):
        '''
        Funcion para generar tuplas (año,mes) que pertenecen al periodo
        de descarga de informacion.
        '''
        curr_yr = int(self.init_date[:4])
        curr_mth = int(self.init_date[4:])
        end_yr = int(self.end_date[:4])
        end_mth = int(self.end_date[4:])
        assert (curr_yr, curr_mth) <= (end_yr,end_mth), "La fehcha de inicio es mayor a la de fin."
        while (curr_yr, curr_mth) <= (end_yr,end_mth):
            data_point = (curr_yr, curr_mth)
            yield data_point
            if curr_mth == 12:
                curr_yr +=1
                curr_mth = 1
            else:
                curr_mth +=1
    def get_historical_data(self):
        '''
        Consulta de informacion historica de cada mes que pertenezca al periodo de descarga.
        '''
        if self.res_path not in os.listdir():
            os.mkdir(self.res_path)
        for data_point in self._iterate_dates():
            url = self._make_url(data_point)
            print('Downloading: ', url, sep = '\n')
            page = requests.get(url)
            if page.status_code == 404:
                print('STATUS CODE 404')
                next
            else:
                filename = 'Ecobici_Historico_' + '-'.join(['{:02d}'.format(x) for x in data_point])+'.csv'
                final_path = '\\'.join((self.res_path, filename))
                with open(final_path, 'wb') as f:
                    f.write(page.content)
