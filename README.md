
# Ecobici

EcoBici es un sistema de bicicletas compartidas en la Ciudad de México que sigue una política de datos abiertos y por lo tanto, cuenta con la infraestructura para compartir su información con todo el público.
De manera muy concreta, Ecobici comparte dos tipos de información:
1. Información Histórica:  
Ecobici te permite descargar los arhcivos históricos de los viajes en bicicleta con detalles como edad, sexo, Cicloestación de inicio y fin, Hora de inicio y fin entre otros.
2. Consultas por medio de su API:  
También cuentan con una API con la que puedes consultar la información de todas las cicloestaciones registradas así como la disponibilidad de bicicletas en tiempo real.  

Es importante mencionar que para realizar consultas por medio de la API es necesario crearse un perfil de desarrollador en [esta liga](https://www.ecobici.cdmx.gob.mx/es/informacion-del-servicio/open-data)

Para mayor información acerca de estos servicios pueden consultar en:  
https://www.ecobici.cdmx.gob.mx/es/informacion-del-servicio/open-data

Esta librería te permite explotar las tres fuentes de información mencionadas anteriormente de manera sencilla y rápida.

## Datos Históricos

Por medio de `Ecobici.Historical` es posible descargar información histórica de viajes Ecobici. Tu sólo elige dos fechas y en tu computadora se descargaran los archivos históricos de cada mes.


```python
import Ecobici.Historical as EH

## Las fechas se escriben en formato YYYYMM
init_month = '201712'
end_month = '201802'

sess = EH.Historical(init_month, end_month)
sess.get_historical_data()
```

    Downloading: 
    https://www.ecobici.cdmx.gob.mx/sites/default/files/data/usages/2017-12.csv
    Downloading: 
    https://www.ecobici.cdmx.gob.mx/sites/default/files/data/usages/2018-01.csv
    Downloading: 
    https://www.ecobici.cdmx.gob.mx/sites/default/files/data/usages/2018-02.csv
    

Con esto obtendras un nuevo directorio llamado `Historical_data` en donde se encuentran los historicos en formato .csv

## Consultas a la API

Antes que nada debes crearte un perfil de desarrollador y recibirás dos correos de Ecobici con dos códigos:
1. Client_id
2. Client_secret 

Con estos dos códigos podrás realizar las consultas de la siguiente manera


```python
import Ecobici.API as EA
```


```python
client_secret = "YOUR CLIENT SECRET"
client_id = "YOUR CLIENT ID"
```


```python
sess = EA.API(client_secret=client_secret, client_id= client_id)
```


```python
# En info_cicloestaciones se guarda un dict() con toda la informacion.
info_cicloestaciones = sess.consultar_cicloestaciones()
```

    Consultando token
    


```python
len(info_cicloestaciones['stations'])
```




    480




```python
info_cicloestaciones['stations'][0]
```




    {'id': 448,
     'name': '448 DR. ANDRADE - ARCOS DE BELÉN',
     'address': 'DR. ANDRADE ARCOS DE BELÉN',
     'addressNumber': 'S/N',
     'zipCode': None,
     'districtCode': None,
     'districtName': None,
     'altitude': None,
     'nearbyStations': [448],
     'location': {'lat': 19.426611, 'lon': -99.14447},
     'stationType': 'BIKE,TPV'}



### Disponibilidad en tiempo real


```python
disponibilidad = sess.consultar_disponibilidad_estaciones()
```


```python
disponibilidad['stationsStatus'][:5]
```




    [{'id': 1, 'status': 'OPN', 'availability': {'bikes': 5, 'slots': 20}},
     {'id': 2, 'status': 'OPN', 'availability': {'bikes': 3, 'slots': 9}},
     {'id': 3, 'status': 'OPN', 'availability': {'bikes': 30, 'slots': 6}},
     {'id': 4, 'status': 'CLS', 'availability': {'bikes': 0, 'slots': 15}},
     {'id': 5, 'status': 'OPN', 'availability': {'bikes': 5, 'slots': 7}}]


