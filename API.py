import requests
import json

class API:
    '''
    Por medio de esta clase se pueden hacer las dos consultas posibles a la API de Ecobici:
            1. Informacion de las cicloestaciones (id, ubicacion geografica, estaciones cercanas.)
            2. Disponibilidad de bicicletas: Permite conocer la cantidad de bicicletas disponibles en cada
                cicloestacion en tiempo real.
    '''
    def __init__(self, client_secret, client_id):
        '''
        Inputs
        --------
        Inicializar la clase para hacer consultas.
            client_secret, str
                Codigo secreto obtenido a traves de la pagina de ecobici.cdmx
            client_id str
                id secreto obtenido a traves de la pagina de ecobici.cdmx
        '''
        self.cl_se = client_secret
        self.cl_id = client_id
        self.access_token = None
        self.refresh_token = None
    def _get_token(self):
        '''
        Para hacer consultas necesitamos de un token que se consigue por medio de una url.
        Esta funcion consulta y almacena los siguientes tokens:
            1. access_token: Token necesario para realizar consultas a ecobici.
            2. refresh token: Token necesario para obtener el access_token una vez que ha caducado.
        '''
        url = 'https://pubsbapi.smartbike.com/oauth/v2/token?'
        params = {
           'client_id':self.cl_id,
            'client_secret': self.cl_se,
            'grant_type': 'client_credentials'
        }
        if self.refresh_token:
            params['grand_type'] = 'refresh_token'
            params['refresh_token'] = self.refresh_token
        page = requests.get(url, params = params)
        if page.status_code == 200:
            res = json.loads(page.content)
            self.access_token = res['access_token']
            self.refresh_token =  res['refresh_token']
        else:
            print('Bad Request')

    def consultar_cicloestaciones(self):
        '''
        Obtener listado de cicloestaciones registradas con la siguiente informacion:
        id, name, adress, adressnumber, zipcode, districtCode, districtName, nearby stations,
            location, stationType.
         Inputs
        -------
            No se necesita un Input adicional
         Returns
        --------
            stations: Dict
                Diccionario que contiene la informacion de las cicloestaciones.
        '''
        if not self.access_token:
            print('Consultando token')
            self._get_token()
        url = f'https://pubsbapi.smartbike.com/api/v1/stations.json?'
        params = {
            "access_token":self.access_token
        }
        page = requests.get(url, params = params)
        if page.status_code == 200:
            stations = json.loads(page.content)
        return stations
    def consultar_disponibilidad_estaciones(self):
        '''
        Obtener disponibilidad de estaciones con la siguiente informacion:
            id, status, availability.
         Inputs
        --------
         No se necesitan inputs adicionales

         Returns
        ----------
            disponibilidad: Dict
                Diccionario con la informacion de la disponibilidad de las estaciones.
        '''
        if not self.access_token:
            print('Consultando token')
            self._get_token()
        url = 'https://pubsbapi.smartbike.com/api/v1/stations/status.json?'
        params = {
            "access_token":self.access_token
        }
        page = requests.get(url, params = params)
        if page.status_code == 200:
            disponibilidad = json.loads(page.content)
        return disponibilidad
