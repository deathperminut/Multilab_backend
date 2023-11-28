import pymysql
from flask import Flask,request
import pandas as pd
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Configuración de la conexión a la base de datos
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root2'
app.config['MYSQL_PASSWORD'] = 'Carrito_1'
app.config['MYSQL_DB'] = 'multilab'

# Creación de la conexión a la base de datos
connection = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)
rangos_elementos = {
    "ph": [4.5, 5, 5.5, 6.001],
    "n": [0.2, 0.3, 0.4, 0.5001],
    "mo": [5, 10, 15, 20.001],
    "k": [0.2, 0.4, 0.6, 0.8001],
    "ca": [1.5, 3, 5, 6.001],
    "mg": [0.6, 1.2, 1.8, 2.4001],
    "na": [0.02, 0.04, 0.06, 0.08001],
    "al": [0.4, 0.8, 1.2, 1.60001],
    "cic": [10, 15, 20, 25.0001],
    "p": [7, 14, 21, 28.0001],
    "fe": [70, 140, 210, 280.0001],
    "mn": [20, 40, 60, 80.0001],
    "zn": [3, 6, 9, 12.0001],
    "cu": [3, 6, 9, 12.0005],
    "s": [5, 10, 15, 20.001],
    "b": [0.15, 0.3, 0.45, 0.6001],
    "ar": [7, 14, 21, 28.001],
    "l": [20, 25, 30, 35.001],
    "a": [30, 40, 50, 60.0001]
}
####### RANGOS ########
rangos_elementos_cafe = {
    "ph": [4.6, 5, 5.4, 5.8],
    "n": [0.2, 0.3, 0.4, 0.5],
    "mo": [4, 7, 10, 13],
    "k": [0.12, 0.24, 0.36, 0.48],
    "ca": [1, 3, 5, 9],
    "mg": [0.3, 0.8, 1.3, 2.3],
    "na": [0.02, 0.04, 0.06, 0.08],
    "al": [0.4, 0.8, 1.2, 2],
    "cic": [15, 19, 23, 27],
    "p": [3, 6, 12, 24],
    "fe": [150, 200, 250, 300],
    "mn": [12, 24, 36, 60],
    "zn": [1.8, 3.6, 5.4, 7.2],
    "cu": [1.8, 3.6, 5.4, 7.2],
    "s": [4, 8, 12, 20],
    "b": [0.15, 0.3, 0.45, 0.6],
    "ar": [20, 26, 32, 38],
    "l": [21, 25, 29, 33],
    "a": [35, 42, 49, 56]
}

rangos_elementos_citricos = {
    "ph": [4.6, 5, 5.4, 5.8],
    "n": [0.2, 0.25, 0.3, 0.35],
    "mo": [4, 5, 6, 8],
    "k": [0.2, 0.4, 0.6, 0.8],
    "ca": [3, 4.5, 6, 7.5],
    "mg": [0.8, 1.6, 2.4, 4],
    "na": [0.02, 0.04, 0.06, 0.1],
    "al": [0.2, 0.5, 0.8, 1.4],
    "cic": [15, 18, 21, 24],
    "p": [5, 10, 20, 40],
    "fe": [200, 250, 300, 400],
    "mn": [30, 45, 60, 90],
    "zn": [4, 6, 8, 10],
    "cu": [4, 6, 8, 10],
    "s": [5, 10, 20, 40],
    "b": [0.3, 0.4, 0.5, 0.7],
    "ar": [22, 28, 34, 40],
    "l": [22, 25, 28, 31],
    "a": [38, 43, 48, 53]
}

rangos_elementos_aguacate = {
    "ph": [5, 5.2, 5.4, 5.6],
    "n": [0.2, 0.3, 0.4, 0.5],
    "mo": [6, 8, 10, 14],
    "k": [0.15, 0.25, 0.35, 0.45],
    "ca": [1, 2, 3, 5],
    "mg": [0.3, 0.6, 0.9, 1.5],
    "na": [0.02, 0.03, 0.04, 0.6],
    "al": [0.25, 0.5, 0.75, 1],
    "cic": [18, 22, 26, 30],
    "p": [2, 6, 10, 18],
    "fe": [140, 180, 220, 300],
    "mn": [10, 20, 30, 50],
    "zn": [3, 5, 7, 9],
    "cu": [2, 4, 6, 8],
    "s": [4, 8, 12, 20],
    "b": [0.15, 0.3, 0.45, 0.6],
    "ar": [16, 21, 26, 31],
    "l": [24, 27, 30, 33],
    "a": [43, 48, 53, 58]
}
round_elementos = {
    "ph": 1,
    "n": 2,
    "mo": 1,
    "k": 2,
    "ca": 2,
    "mg": 2,
    "na": 2,
    "al": 1,
    "cic": 0,
    "p": 0,
    "fe": 0,
    "mn": 0,
    "zn": 1,
    "cu": 1,
    "s": 1,
    "b": 2,
    "ar": 0,
    "l": 0,
    "a": 0,
}
### RANGOS PASTO
rangos_elementos_pasto = {
    "ph": [5.3, 5.5, 5.7, 5.9],
    "n": [0.2, 0.3, 0.4, 0.5],
    "mo": [5, 7, 9, 13],
    "k": [0.2, 0.3, 0.4, 0.6],
    "ca": [2, 4, 6, 8],
    "mg": [0.7, 1.3, 1.9, 3.1],
    "na": [0.04, 0.06, 0.08, 0.12],
    "al": [0.25, 0.5, 0.75, 1],
    "cic": [18, 22, 26, 30],
    "p": [2, 6, 10, 18],
    "fe": [140, 180, 220, 300],
    "mn": [10, 20, 30, 50],
    "zn": [3, 5, 7, 9],
    "cu": [2, 4, 6, 8],
    "s": [4, 8, 12, 20],
    "b": [0.15, 0.3, 0.45, 0.6],
    "ar": [16, 21, 26, 31],
    "l": [24, 27, 30, 33],
    "a": [43, 48, 53, 58]
}



# Cerrar la conexión al finalizar el programa o cuando ya no se necesite
def cerrar_conexion():
    connection.close()

# Puedes registrar una función para cerrar la conexión cuando la aplicación se detenga
@app.teardown_appcontext
def cerrar_conexion_teardown(exception):
    cerrar_conexion()
# Ejemplo de consulta SQL
@app.route('/departaments_data',methods=['POST'])
def index():
    ##################################
    #############
    ############# variable ['ph','n','mo','k','ca','mg','al','cic','p','fe','mn','zn','cu','s','b','ar','l','a']
    ############# año      ['pH','N','MO','K','Ca','Mg','Al','CIC','P','Fe','Mn','Zn','Cu','S','B','Ar','L','A']     
    ############# tipo de cultivo ['CITRICOS','cafe', 'aguacate'] ## solo esos 3 rangos
    data = request.json
    dictionary_ranges = {
        'General':rangos_elementos,
        'Café':rangos_elementos_cafe,
        'Citricos':rangos_elementos_citricos,
        'Aguacates':rangos_elementos_aguacate,
        'Pasto':rangos_elementos_pasto
    }
    year = data['year']
    if len(year) == 0:
        year = [{'value':'2010'},{'value':'2011'},{'value':'2012'},{'value':'2013'},{'value':'2014'},{'value':'2015'},{'value':'2016'},{'value':'2017'},{'value':'2018'},{'value':'2019'},{'value':'2020'},{'value':'2021'},{'value':'2022'},{'value':'2023'}]
    variable = data['variable']
    tipo_cultivo = data['tipo_cultivo'] ## 'General', 'Café' , 'Citricos' , 'Aguacates' , 'Pasto'
    cursor = connection.cursor()### conectamos el cursor
    #############################################################################
    ###### OBTENEMOS EN UN DATAFRAME TODOS LOS AÑOS SELECCIONADOS ###############
    #############################################################################
    cursor.execute('SELECT * FROM departamentos')
    dataframe_all_data = pd.DataFrame()
    
    for ye in year:
        y = ye['value']
        ### iteramos por cada año seleccionado
        consulta = f'SELECT multilab.muestra_{y}.{variable} ,multilab.departamentos.codigo FROM multilab.muestra_{y} INNER JOIN multilab.orden_{y} ON multilab.muestra_{y}.orden = multilab.orden_{y}.codigo INNER JOIN multilab.finca ON multilab.orden_{y}.codigo_finca = multilab.finca.codigo INNER JOIN multilab.departamentos ON multilab.finca.departamento = multilab.departamentos.codigo;'
        cursor.execute(consulta)
        results_muestras = cursor.fetchall()
        ### obtenemos cada una de las muestras correspondientes de dicho departamento en un dataframe
        df_muestras_1 = pd.DataFrame(results_muestras, columns=[desc[0] for desc in cursor.description])
        ### concatenamos los dataframes
        dataframe_all_data = pd.concat([dataframe_all_data, df_muestras_1])
    ### obtenemos en un solo dataframe la información de todos los años seleccionados con todos los departamentos
    ##### nos traemos los departamentos y filtramos el dataframe por dicho año
    cursor.execute('SELECT * FROM departamentos')
    results_departaments = cursor.fetchall()
    df = pd.DataFrame(results_departaments, columns=[desc[0] for desc in cursor.description])
    list_departaments = []
    
    for row in df.iterrows():
        dictionary_row = {'value':'','media':'','Bajo':'','Mod. bajo':'','Medio':'','Mod. alto':'','Alto':'','name':row[1]['nombre'],'cantidad registros':'','Rango_media':'','id':str(row[1]['codigo'])}
        #dictionary[row[1]['nombre']]
        ### iteramos por cada fila para ejecutar la query
        df_muestras = dataframe_all_data[dataframe_all_data['codigo'] == row[1]['codigo'] ]
        
        dictionary_row['cantidad registros'] = df_muestras.shape[0]
        ### obtenemos la media de los datos sin tener encuenta los nulos
        # Eliminar filas con valores de columna vacíos en 'Columna1'
        # Eliminar filas donde los valores de 'Columna1' sean strings vacíos
        df_muestras = df_muestras[df_muestras[variable] != '']
        df_muestras[variable] = df_muestras[variable].str.replace(',', '.')
        df_muestras[variable] = df_muestras[variable].astype('float').fillna(0)
        media = df_muestras[variable].mean(skipna=True)
        ### OBTENEMOS EL RANGO SEGUN LA MEDIDA MANDADA
        RANGOS = dictionary_ranges[tipo_cultivo]
        if(np.isnan(media)):
            dictionary_row['media'] = 'No hay datos'
            dictionary_row['Rango_media'] = 'No hay datos'
            dictionary_row['value'] = 'No hay datos'
        else:
            dictionary_row['media'] = round(media,round_elementos[variable])
            if(media < RANGOS[variable][0]):
                dictionary_row['Rango_media'] = 'Bajo'
                dictionary_row['value'] = min(1,(media - 0) / (RANGOS[variable][1]))
            elif (media >= RANGOS[variable][0] and  media < RANGOS[variable][1]):
                dictionary_row['Rango_media'] = 'Mod. bajo'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][0]) / (RANGOS[variable][1] - media))
            elif (media >= RANGOS[variable][1] and  media < RANGOS[variable][2]):
                dictionary_row['Rango_media'] = 'Medio'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][1]) / (RANGOS[variable][2] - media))
            elif (media >= RANGOS[variable][2] and  media < RANGOS[variable][3]):
                dictionary_row['Rango_media'] = 'Mod. alto'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][2]) / (RANGOS[variable][3] - media))
            elif (media >= RANGOS[variable][3]):
                dictionary_row['Rango_media'] = 'Alto'
                dictionary_row['value'] = 1
        ### Miramos los valores por rango
        ###Bajo
        ###
        

        ### miramos candidad en cada rango
        count_bajo = df_muestras[(df_muestras[variable] < RANGOS[variable][0])].shape[0]
        count_M_bajo = df_muestras[(df_muestras[variable] >= RANGOS[variable][0]) & (df_muestras[variable] < RANGOS[variable][1])].shape[0]
        count_Medio = df_muestras[(df_muestras[variable] >= RANGOS[variable][1]) & (df_muestras[variable] < RANGOS[variable][2])].shape[0]
        count_M_alto = df_muestras[(df_muestras[variable] >= RANGOS[variable][2]) & (df_muestras[variable] < RANGOS[variable][3])].shape[0]
        count_alto = df_muestras[(df_muestras[variable] > RANGOS[variable][3])].shape[0]
        ### introducimos los resultados al diccionario del departamento
        dictionary_row['Bajo'] = count_bajo
        dictionary_row['Mod. bajo'] = count_M_bajo
        dictionary_row["Medio"] = count_Medio
        dictionary_row['Mod. alto'] = count_M_alto
        dictionary_row['Alto'] = count_alto

        
        list_departaments.append(dictionary_row)

    #### funciono :D
    cursor.close()
    return  list_departaments


@app.route('/departaments',methods=['GET'])
def departaments():
    cursor = connection.cursor()
    ####OBTENEMOS CADA UNO DE LOS DEPARTAMENTOS
    cursor.execute('SELECT * FROM multilab.departamentos')
    results_departaments = cursor.fetchall()
    data = []
    for element in results_departaments:
        data.append({'name':element[1],'id':element[0]})
    
    cursor.close()
    return data


# Ejemplo de consulta SQL
@app.route('/municipios',methods=['POST'])
def municipios():
    data = request.json
    departament_id = data ['id_departament']
    cursor = connection.cursor()
    ####OBTENEMOS CADA UNO DE LOS DEPARTAMENTOS
    cursor.execute('SELECT * FROM multilab.municipios WHERE codigo_depto =%s',(departament_id,))
    results_departaments = cursor.fetchall()
    data = []
    for element in results_departaments:
        data.append({'name':element[2],'id':element[0],'id_departament':element[1]})
    cursor.close()
    return data



# Ejemplo de consulta SQL
@app.route('/municipios_data',methods=['POST'])
def municipios_data():
    ##################################
    #############
    ############# variable ['ph','n','mo','k','ca','mg','al','cic','p','fe','mn','zn','cu','s','b','ar','l','a']
    ############# año      ['pH','N','MO','K','Ca','Mg','Al','CIC','P','Fe','Mn','Zn','Cu','S','B','Ar','L','A']     
    ############# tipo de cultivo ['CITRICOS','cafe', 'aguacate'] ## solo esos 3 rangos
    data = request.json
    dictionary_ranges = {
        'General':rangos_elementos,
        'Café':rangos_elementos_cafe,
        'Citricos':rangos_elementos_citricos,
        'Aguacates':rangos_elementos_aguacate,
        'Pasto':rangos_elementos_pasto
    }
    year = data['year']
    if len(year) == 0:
        year = [{'value':'2010'},{'value':'2011'},{'value':'2012'},{'value':'2013'},{'value':'2014'},{'value':'2015'},{'value':'2016'},{'value':'2017'},{'value':'2018'},{'value':'2019'},{'value':'2020'},{'value':'2021'},{'value':'2022'},{'value':'2023'}]
    variable = data['variable']
    tipo_cultivo = data['tipo_cultivo'] ## 'General', 'Café' , 'Citricos' , 'Aguacates' , 'Pasto'
    departament =data ['id_departament']
    cursor = connection.cursor()
    ####### OBTENEMOS TODA LA BASE DE DATOS POR CADA AÑO#####################
    dataframe_all_data = pd.DataFrame()
    for ye in year:
            y = ye['value']
            ### iteramos por cada fila para ejecutar la query
            consulta = f'SELECT multilab.muestra_{y}.{variable},multilab.municipios.codigo_municipio FROM multilab.muestra_{y} INNER JOIN multilab.orden_{y} ON multilab.muestra_{y}.orden = multilab.orden_{y}.codigo INNER JOIN multilab.finca ON multilab.orden_{y}.codigo_finca = multilab.finca.codigo INNER JOIN multilab.municipios ON multilab.finca.municipio = multilab.municipios.codigo_municipio'
            cursor.execute(consulta)
            results_muestras = cursor.fetchall()
            ### obtenemos cada una de las muestras correspondientes de dicho departamento en un dataframe
            df_muestras_1 = pd.DataFrame(results_muestras, columns=[desc[0] for desc in cursor.description])
            ### concatenamos los dataframes
            dataframe_all_data = pd.concat([dataframe_all_data, df_muestras_1])
    ####OBTENEMOS CADA UNO DE LOS DEPARTAMENTOS
    cursor.execute('SELECT * FROM multilab.municipios WHERE codigo_depto =%s',(departament,))
    results_departaments = cursor.fetchall()
    df = pd.DataFrame(results_departaments, columns=[desc[0] for desc in cursor.description])
    list_departaments = []
    
    for row in df.iterrows():
        dictionary_row = {'value':'','media':'','Bajo':'','Mod. bajo':'','Medio':'','Mod. alto':'','Alto':'','name':row[1]['nombre'],'cantidad registros':'','Rango_media':''}
        df_muestras = dataframe_all_data[dataframe_all_data['codigo_municipio'] == row[1]['codigo_municipio']]
        dictionary_row['cantidad registros'] = df_muestras.shape[0]
        ### obtenemos la media de los datos sin tener encuenta los nulos
        df_muestras = df_muestras[df_muestras[variable] != '']
        df_muestras[variable] = df_muestras[variable].str.replace(',', '.')
        df_muestras[variable] = df_muestras[variable].astype('float').fillna(0)


        media = df_muestras[variable].mean(skipna=True)
        ### OBTENEMOS EL RANGO SEGUN LA MEDIDA MANDADA
        RANGOS = dictionary_ranges[tipo_cultivo]
        if(np.isnan(media)):
            dictionary_row['media'] = 'No hay datos'
            dictionary_row['Rango_media'] = 'No hay datos'
        else:
            dictionary_row['media'] = round(media,round_elementos[variable])
            if(media < RANGOS[variable][0]):
                dictionary_row['Rango_media'] = 'Bajo'
                dictionary_row['value'] = min(1,(media - 0) / (RANGOS[variable][1]))
            elif (media >= RANGOS[variable][0] and  media < RANGOS[variable][1]):
                dictionary_row['Rango_media'] = 'Mod. bajo'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][0]) / (RANGOS[variable][1] - media))
            elif (media >= RANGOS[variable][1] and  media < RANGOS[variable][2]):
                dictionary_row['Rango_media'] = 'Medio'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][1]) / (RANGOS[variable][2] - media))
            elif (media >= RANGOS[variable][2] and  media < RANGOS[variable][3]):
                dictionary_row['Rango_media'] = 'Mod. alto'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][2]) / (RANGOS[variable][3] - media))
            elif (media >= RANGOS[variable][3]):
                dictionary_row['Rango_media'] = 'Alto'
                dictionary_row['value'] = 1

        ### miramos candidad en cada rango
        count_bajo = df_muestras[(df_muestras[variable] < RANGOS[variable][0])].shape[0]
        count_M_bajo = df_muestras[(df_muestras[variable] >= RANGOS[variable][0]) & (df_muestras[variable] < RANGOS[variable][1])].shape[0]
        count_Medio = df_muestras[(df_muestras[variable] >= RANGOS[variable][1]) & (df_muestras[variable] < RANGOS[variable][2])].shape[0]
        count_M_alto = df_muestras[(df_muestras[variable] >= RANGOS[variable][2]) & (df_muestras[variable] < RANGOS[variable][3])].shape[0]
        count_alto = df_muestras[(df_muestras[variable] > RANGOS[variable][3])].shape[0]
        ### introducimos los resultados al diccionario del departamento
        dictionary_row['Bajo'] = count_bajo
        dictionary_row['Mod. bajo'] = count_M_bajo
        dictionary_row["Medio"] = count_Medio
        dictionary_row['Mod. alto'] = count_M_alto
        dictionary_row['Alto'] = count_alto
        list_departaments.append(dictionary_row)

    
    
    #### funciono :D
    cursor.close()
    return  list_departaments

####SERVICIO PARA VER EL HISTORIAL DE UN CLIENTE DE UNA FINCA.
# Ejemplo de consulta SQL
@app.route('/cliente_historial',methods=['POST'])
def cliente_historial():
    data = request.json
    dictionary_ranges = {
        'General':rangos_elementos,
        'Café':rangos_elementos_cafe,
        'Citricos':rangos_elementos_citricos,
        'Aguacates':rangos_elementos_aguacate,
        'Pasto':rangos_elementos_pasto
    }
    cliente = data['cliente']#'1172232'
    variable = data['variable']#'ph'
    tipo_cultivo = data['tipo_cultivo']#'Café'
    list_year = ['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023']
    let_list_data = [] ## arreglo donde voy a guardar todos los servicios
    cursor = connection.cursor()
    count = 0
    for year in list_year:
        ### iteramos por cada año para obtener el historico de dicho año y determinar cuales
        ### estan en cada rango
        ### en caso de que no haya registro retornamos un valor de cero como referencia
        results = {'media':'','Bajo':'','Mod. bajo':'','Medio':'','Mod. alto':'','Alto':'','year':year,'cantidad registros':''}
        
        ### iteramos por cada fila para ejecutar la query
        consulta = f'SELECT multilab.muestra_{year}.{variable} FROM multilab.muestra_{year} INNER JOIN multilab.orden_{year} ON multilab.muestra_{year}.orden = multilab.orden_{year}.codigo INNER JOIN multilab.finca ON multilab.orden_{year}.codigo_finca = multilab.finca.codigo INNER JOIN multilab.cliente ON multilab.finca.propietario = multilab.cliente.codigo WHERE multilab.cliente.nombre = %s'
        cursor.execute(consulta, (cliente,))
        results_muestras = cursor.fetchall()
        if(len(results_muestras) == 0):
                let_list_data.append({'media':'No hay datos','Bajo':0,'Mod. bajo':0,'Medio':0,'Mod. alto':0,'Alto':0,'year':year,'cantidad registros':0})
        else:
            count = 1
            ### obtenemos cada una de las muestras correspondientes de dicho departamento en un dataframe
            df_muestras = pd.DataFrame(results_muestras, columns=[desc[0] for desc in cursor.description])
            results['cantidad registros'] = df_muestras.shape[0]
            ### obtenemos la media de los datos sin tener encuenta los nulos
            df_muestras[variable] = df_muestras[variable].str.replace(',', '.')
            df_muestras[variable] = df_muestras[variable].astype('float').fillna(0)
            media = df_muestras[variable].mean(skipna=True)
            
            if(np.isnan(media)):
                results['media'] = 'No hay datos'
            else:
                results['media'] =  media
            ### Miramos los valores por rango
            ###Bajo
            ###
            ### OBTENEMOS EL RANGO SEGUN LA MEDIDA MANDADA
            RANGOS = dictionary_ranges[tipo_cultivo]

            ### miramos candidad en cada rango
            count_bajo = df_muestras[(df_muestras[variable] < RANGOS[variable][0])].shape[0]
            count_M_bajo = df_muestras[(df_muestras[variable] >= RANGOS[variable][0]) & (df_muestras[variable] < RANGOS[variable][1])].shape[0]
            count_Medio = df_muestras[(df_muestras[variable] >= RANGOS[variable][1]) & (df_muestras[variable] < RANGOS[variable][2])].shape[0]
            count_M_alto = df_muestras[(df_muestras[variable] >= RANGOS[variable][2]) & (df_muestras[variable] < RANGOS[variable][3])].shape[0]
            count_alto = df_muestras[(df_muestras[variable] > RANGOS[variable][3])].shape[0]
            ### introducimos los resultados al diccionario del departamento
            results['Bajo'] = count_bajo
            results['Mod. bajo'] = count_M_bajo
            results["Medio"] = count_Medio
            results['Mod. alto'] = count_M_alto
            results['Alto'] = count_alto

            let_list_data.append(results)
    
    if(count == 0):
        cursor.close()
        return []
    else:
        cursor.close()
        return let_list_data
    

### TERMINAMOS PROYECTO DE BACKEND
@app.route('/inferencia',methods=['POST'])
def inferencia_resultados():
    data = request.json
    dictionary_ranges = {
        'General':rangos_elementos,
        'Café':rangos_elementos_cafe,
        'Citricos':rangos_elementos_citricos,
        'Aguacates':rangos_elementos_aguacate,
        'Pasto':rangos_elementos_pasto
    }
    variable = data['variable']#'ph'
    magnitud = float(data['magnitud'])#4.8
    tipo_cultivo = data['tipo_cultivo'] #'Café'
    RANGOS  = dictionary_ranges[tipo_cultivo]

    if(magnitud < RANGOS[variable][0]):

        return {'Answer':'Bajo'}
    elif (magnitud >= RANGOS[variable][0] and  magnitud < RANGOS[variable][1]):
        return {'Answer':'Mod. bajo'}
    elif (magnitud >= RANGOS[variable][1] and  magnitud < RANGOS[variable][2]):
        return {'Answer':'Medio'}
    elif (magnitud >= RANGOS[variable][2] and  magnitud < RANGOS[variable][3]):
        return {'Answer':'Mod. alto'}
    elif (magnitud >= RANGOS[variable][3]):
        return {'Answer':'Alto'}

### TERMINAMOS PROYECTO DE BACKEND
@app.route('/inferencia_2',methods=['POST'])
def inferencia_resultados_2():
    data = request.json
    dictionary_ranges = {
        'General':rangos_elementos,
        'Café':rangos_elementos_cafe,
        'Citricos':rangos_elementos_citricos,
        'Aguacates':rangos_elementos_aguacate,
        'Pasto':rangos_elementos_pasto
    }

    variable = data['variable']#'ph'
    magnitud = float(data['magnitud'])#4.8
    tipo_cultivo = data['tipo_cultivo'] #'Café'
    departament = data['departament'] # 'departament'
    Municipio = data['Municipio'] # 'departament'
    
    #### CALCULAMOS EL RANGO DEL VALOR SIMINISTRADO
    RANGOS  = dictionary_ranges[tipo_cultivo]
    Data = {'Answer':'','Answer_city':''}
    if(magnitud < RANGOS[variable][0]):
        Data['Answer'] = 'Bajo'
    elif (magnitud >= RANGOS[variable][0] and  magnitud < RANGOS[variable][1]):
        Data['Answer'] = 'Mod. bajo'
    elif (magnitud >= RANGOS[variable][1] and  magnitud < RANGOS[variable][2]):
        Data['Answer'] = 'Medio'
    elif (magnitud >= RANGOS[variable][2] and  magnitud < RANGOS[variable][3]):
        Data['Answer'] = 'Mod. alto'
    elif (magnitud >= RANGOS[variable][3]):
        Data['Answer'] = 'Alto'
    #### CALCULAMOS EL VALOR DEL PROMEDIO EN EL CUAL SE UBICA EL DEPARTAMENTO ####
    ### LEEMOS BAJO QUE AÑOS QUIERO HACER LA COMPARATIVA
    year = data['year']
    if len(year) == 0:
        year = [{'value':'2010'},{'value':'2011'},{'value':'2012'},{'value':'2013'},{'value':'2014'},{'value':'2015'},{'value':'2016'},{'value':'2017'},{'value':'2018'},{'value':'2019'},{'value':'2020'},{'value':'2021'},{'value':'2022'},{'value':'2023'}]
    
    if(Municipio != ''):
        dataframe_all_data = pd.DataFrame()
        cursor = connection.cursor()
        for ye in year:
            y = ye['value']
            ### iteramos por cada año seleccionado
            consulta = f'SELECT multilab.muestra_{y}.{variable} ,multilab.municipios.codigo_municipio FROM multilab.muestra_{y} INNER JOIN multilab.orden_{y} ON multilab.muestra_{y}.orden = multilab.orden_{y}.codigo INNER JOIN multilab.finca ON multilab.orden_{y}.codigo_finca = multilab.finca.codigo INNER JOIN multilab.municipios ON multilab.finca.municipio = multilab.municipios.codigo_municipio WHERE multilab.municipios.codigo_municipio =%s'
            cursor.execute(consulta, (Municipio,))
            results_muestras = cursor.fetchall()
            ### obtenemos cada una de las muestras correspondientes de dicho departamento en un dataframe
            df_muestras_1 = pd.DataFrame(results_muestras, columns=[desc[0] for desc in cursor.description])
            ### concatenamos los dataframes
            dataframe_all_data = pd.concat([dataframe_all_data, df_muestras_1])

        #### una vez con toda la base de datos  midamos la media que necesito y cuantos estan en cada rango:
        
        dictionary_row = {'value':'','media':'','Bajo':'','Mod. bajo':'','Medio':'','Mod. alto':'','Alto':'','cantidad registros':'','Rango_media':''}
        #dictionary[row[1]['nombre']]
        ### iteramos por cada fila para ejecutar la query
        df_muestras = dataframe_all_data
        dictionary_row['cantidad registros'] = df_muestras.shape[0]
        ### obtenemos la media de los datos sin tener encuenta los nulos
        # Eliminar filas con valores de columna vacíos en 'Columna1'
        # Eliminar filas donde los valores de 'Columna1' sean strings vacíos
        df_muestras = df_muestras[df_muestras[variable] != '']
        df_muestras[variable] = df_muestras[variable].str.replace(',', '.')
        df_muestras[variable] = df_muestras[variable].astype('float').fillna(0)
        media = df_muestras[variable].mean(skipna=True)
        ### OBTENEMOS EL RANGO SEGUN LA MEDIDA MANDADA
        RANGOS = dictionary_ranges[tipo_cultivo]
        if(np.isnan(media)):
            dictionary_row['media'] = 'No hay datos'
            dictionary_row['Rango_media'] = 'No hay datos'
            dictionary_row['value'] = 'No hay datos'
        else:
            dictionary_row['media'] = round(media,round_elementos[variable])
            if(media < RANGOS[variable][0]):
                dictionary_row['Rango_media'] = 'Bajo'
                dictionary_row['value'] = min(1,(media - 0) / (RANGOS[variable][1]))
            elif (media >= RANGOS[variable][0] and  media < RANGOS[variable][1]):
                dictionary_row['Rango_media'] = 'Mod. bajo'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][0]) / (RANGOS[variable][1] - media))
            elif (media >= RANGOS[variable][1] and  media < RANGOS[variable][2]):
                dictionary_row['Rango_media'] = 'Medio'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][1]) / (RANGOS[variable][2] - media))
            elif (media >= RANGOS[variable][2] and  media < RANGOS[variable][3]):
                dictionary_row['Rango_media'] = 'Mod. alto'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][2]) / (RANGOS[variable][3] - media))
            elif (media >= RANGOS[variable][3]):
                dictionary_row['Rango_media'] = 'Alto'
                dictionary_row['value'] = 1
        ### Miramos los valores por rango
        ###Bajo
        ###
        

        ### miramos candidad en cada rango
        count_bajo = df_muestras[(df_muestras[variable] < RANGOS[variable][0])].shape[0]
        count_M_bajo = df_muestras[(df_muestras[variable] >= RANGOS[variable][0]) & (df_muestras[variable] < RANGOS[variable][1])].shape[0]
        count_Medio = df_muestras[(df_muestras[variable] >= RANGOS[variable][1]) & (df_muestras[variable] < RANGOS[variable][2])].shape[0]
        count_M_alto = df_muestras[(df_muestras[variable] >= RANGOS[variable][2]) & (df_muestras[variable] < RANGOS[variable][3])].shape[0]
        count_alto = df_muestras[(df_muestras[variable] > RANGOS[variable][3])].shape[0]
        ### introducimos los resultados al diccionario del departamento
        dictionary_row['Bajo'] = count_bajo
        dictionary_row['Mod. bajo'] = count_M_bajo
        dictionary_row["Medio"] = count_Medio
        dictionary_row['Mod. alto'] = count_M_alto
        dictionary_row['Alto'] = count_alto
        Data['Answer_city']=dictionary_row
        cursor.close()
        return Data
    
    elif(departament !=''):
        dataframe_all_data = pd.DataFrame()
        cursor = connection.cursor()
        for ye in year:
            y = ye['value']
            ### iteramos por cada año seleccionado
            consulta = f'SELECT multilab.muestra_{y}.{variable} ,multilab.departamentos.codigo FROM multilab.muestra_{y} INNER JOIN multilab.orden_{y} ON multilab.muestra_{y}.orden = multilab.orden_{y}.codigo INNER JOIN multilab.finca ON multilab.orden_{y}.codigo_finca = multilab.finca.codigo INNER JOIN multilab.departamentos ON multilab.finca.departamento = multilab.departamentos.codigo WHERE multilab.departamentos.codigo = %s'
            cursor.execute(consulta, (departament,))
            results_muestras = cursor.fetchall()
            ### obtenemos cada una de las muestras correspondientes de dicho departamento en un dataframe
            df_muestras_1 = pd.DataFrame(results_muestras, columns=[desc[0] for desc in cursor.description])
            ### concatenamos los dataframes
            dataframe_all_data = pd.concat([dataframe_all_data, df_muestras_1])

        #### una vez con toda la base de datos  midamos la media que necesito y cuantos estan en cada rango:
        
        dictionary_row = {'value':'','media':'','Bajo':'','Mod. bajo':'','Medio':'','Mod. alto':'','Alto':'','cantidad registros':'','Rango_media':''}
        #dictionary[row[1]['nombre']]
        ### iteramos por cada fila para ejecutar la query
        df_muestras = dataframe_all_data
        dictionary_row['cantidad registros'] = df_muestras.shape[0]
        ### obtenemos la media de los datos sin tener encuenta los nulos
        # Eliminar filas con valores de columna vacíos en 'Columna1'
        # Eliminar filas donde los valores de 'Columna1' sean strings vacíos
        df_muestras = df_muestras[df_muestras[variable] != '']
        df_muestras[variable] = df_muestras[variable].str.replace(',', '.')
        df_muestras[variable] = df_muestras[variable].astype('float').fillna(0)
        media = df_muestras[variable].mean(skipna=True)
        ### OBTENEMOS EL RANGO SEGUN LA MEDIDA MANDADA
        RANGOS = dictionary_ranges[tipo_cultivo]
        if(np.isnan(media)):
            dictionary_row['media'] = 'No hay datos'
            dictionary_row['Rango_media'] = 'No hay datos'
            dictionary_row['value'] = 'No hay datos'
        else:
            dictionary_row['media'] = round(media,round_elementos[variable])
            if(media < RANGOS[variable][0]):
                dictionary_row['Rango_media'] = 'Bajo'
                dictionary_row['value'] = min(1,(media - 0) / (RANGOS[variable][1]))
            elif (media >= RANGOS[variable][0] and  media < RANGOS[variable][1]):
                dictionary_row['Rango_media'] = 'Mod. bajo'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][0]) / (RANGOS[variable][1] - media))
            elif (media >= RANGOS[variable][1] and  media < RANGOS[variable][2]):
                dictionary_row['Rango_media'] = 'Medio'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][1]) / (RANGOS[variable][2] - media))
            elif (media >= RANGOS[variable][2] and  media < RANGOS[variable][3]):
                dictionary_row['Rango_media'] = 'Mod. alto'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][2]) / (RANGOS[variable][3] - media))
            elif (media >= RANGOS[variable][3]):
                dictionary_row['Rango_media'] = 'Alto'
                dictionary_row['value'] = 1
        ### Miramos los valores por rango
        ###Bajo
        ###
        

        ### miramos candidad en cada rango
        count_bajo = df_muestras[(df_muestras[variable] < RANGOS[variable][0])].shape[0]
        count_M_bajo = df_muestras[(df_muestras[variable] >= RANGOS[variable][0]) & (df_muestras[variable] < RANGOS[variable][1])].shape[0]
        count_Medio = df_muestras[(df_muestras[variable] >= RANGOS[variable][1]) & (df_muestras[variable] < RANGOS[variable][2])].shape[0]
        count_M_alto = df_muestras[(df_muestras[variable] >= RANGOS[variable][2]) & (df_muestras[variable] < RANGOS[variable][3])].shape[0]
        count_alto = df_muestras[(df_muestras[variable] > RANGOS[variable][3])].shape[0]
        ### introducimos los resultados al diccionario del departamento
        dictionary_row['Bajo'] = count_bajo
        dictionary_row['Mod. bajo'] = count_M_bajo
        dictionary_row["Medio"] = count_Medio
        dictionary_row['Mod. alto'] = count_M_alto
        dictionary_row['Alto'] = count_alto
        Data['Answer_city']=dictionary_row
        cursor.close()
        return Data
    else:
        dataframe_all_data = pd.DataFrame()
        ### EN CASO DE QUE NO TENGA SELECCIONADO NINGUNO MIRAMOS CON RESPECTO A LA MEDIA NACIONAL
        cursor = connection.cursor()
        for ye in year:
            y = ye['value']
            ### iteramos por cada año seleccionado
            consulta = f'SELECT multilab.muestra_{y}.{variable} FROM multilab.muestra_{y} '
            cursor.execute(consulta)
            results_muestras = cursor.fetchall()
            ### obtenemos cada una de las muestras correspondientes de dicho departamento en un dataframe
            df_muestras_1 = pd.DataFrame(results_muestras, columns=[desc[0] for desc in cursor.description])
            ### concatenamos los dataframes
            dataframe_all_data = pd.concat([dataframe_all_data, df_muestras_1])

        #### una vez con toda la base de datos  midamos la media que necesito y cuantos estan en cada rango:
        
        dictionary_row = {'value':'','media':'','Bajo':'','Mod. bajo':'','Medio':'','Mod. alto':'','Alto':'','cantidad registros':'','Rango_media':''}
        #dictionary[row[1]['nombre']]
        ### iteramos por cada fila para ejecutar la query
        df_muestras = dataframe_all_data
        dictionary_row['cantidad registros'] = df_muestras.shape[0]
        ### obtenemos la media de los datos sin tener encuenta los nulos
        # Eliminar filas con valores de columna vacíos en 'Columna1'
        # Eliminar filas donde los valores de 'Columna1' sean strings vacíos
        df_muestras = df_muestras[df_muestras[variable] != '']
        df_muestras[variable] = df_muestras[variable].str.replace(',', '.')
        df_muestras[variable] = df_muestras[variable].astype('float').fillna(0)
        media = df_muestras[variable].mean(skipna=True)
        ### OBTENEMOS EL RANGO SEGUN LA MEDIDA MANDADA
        RANGOS = dictionary_ranges[tipo_cultivo]
        if(np.isnan(media)):
            dictionary_row['media'] = 'No hay datos'
            dictionary_row['Rango_media'] = 'No hay datos'
            dictionary_row['value'] = 'No hay datos'
        else:
            dictionary_row['media'] = round(media,round_elementos[variable])
            if(media < RANGOS[variable][0]):
                dictionary_row['Rango_media'] = 'Bajo'
                dictionary_row['value'] = min(1,(media - 0) / (RANGOS[variable][1]))
            elif (media >= RANGOS[variable][0] and  media < RANGOS[variable][1]):
                dictionary_row['Rango_media'] = 'Mod. bajo'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][0]) / (RANGOS[variable][1] - media))
            elif (media >= RANGOS[variable][1] and  media < RANGOS[variable][2]):
                dictionary_row['Rango_media'] = 'Medio'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][1]) / (RANGOS[variable][2] - media))
            elif (media >= RANGOS[variable][2] and  media < RANGOS[variable][3]):
                dictionary_row['Rango_media'] = 'Mod. alto'
                dictionary_row['value'] = min(1,(media - RANGOS[variable][2]) / (RANGOS[variable][3] - media))
            elif (media >= RANGOS[variable][3]):
                dictionary_row['Rango_media'] = 'Alto'
                dictionary_row['value'] = 1
        ### Miramos los valores por rango
        ###Bajo
        ###
        

        ### miramos candidad en cada rango
        count_bajo = df_muestras[(df_muestras[variable] < RANGOS[variable][0])].shape[0]
        count_M_bajo = df_muestras[(df_muestras[variable] >= RANGOS[variable][0]) & (df_muestras[variable] < RANGOS[variable][1])].shape[0]
        count_Medio = df_muestras[(df_muestras[variable] >= RANGOS[variable][1]) & (df_muestras[variable] < RANGOS[variable][2])].shape[0]
        count_M_alto = df_muestras[(df_muestras[variable] >= RANGOS[variable][2]) & (df_muestras[variable] < RANGOS[variable][3])].shape[0]
        count_alto = df_muestras[(df_muestras[variable] > RANGOS[variable][3])].shape[0]
        ### introducimos los resultados al diccionario del departamento
        dictionary_row['Bajo'] = count_bajo
        dictionary_row['Mod. bajo'] = count_M_bajo
        dictionary_row["Medio"] = count_Medio
        dictionary_row['Mod. alto'] = count_M_alto
        dictionary_row['Alto'] = count_alto
        Data['Answer_city']=dictionary_row
        cursor.close()
        return Data
#SELECT DISTINCT nombre FROM multilab.cliente

# Ejemplo de consulta SQL
@app.route('/clientes',methods=['GET'])
def getClientes():
    cursor = connection.cursor()
    ####OBTENEMOS CADA UNO DE LOS DEPARTAMENTOS
    cursor.execute('SELECT DISTINCT nombre FROM multilab.cliente')
    results_departaments = cursor.fetchall()
    data = []
    for element in results_departaments:
        data.append({'value':element[0],'label':element[0]})
    cursor.close()
    return data
#### TERMINAMOS ENDPOINTS DE LA PLATAFORMA




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)