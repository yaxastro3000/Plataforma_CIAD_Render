import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input,Output
import pandas as pd 
#base de datos de la Huasteca
ud = pd.read_csv('unidaddomestica_Huasteca.csv')
pc=pd.read_csv('productor_ciclo.csv')
s=pd.read_csv('productor_huasteca.csv')
al=pd.read_csv('alimentos_Huasteca.csv')
pg=pd.read_csv('Plaga_Huasteca.csv')

#base de datos del valle del mezquital 
md = pd.read_csv('unidaddomestica_Mezquital.csv')
p_valle=pd.read_csv('productoyvalle.csv') # Quital acatlan 2018
df_valle=pd.read_csv('productor_Mezquital.csv') #Quitar acatlan 2018
df_productores=pd.read_csv('Encuesta_productores2.csv') # 2019
df_productores2=pd.read_csv('Encuesta_productores3.csv') #Seleccionar el valle del mezquital con Municipio 2019
pg2=pd.read_csv('Plaga_Mezquital.csv')
al2=pd.read_csv('alimentos_Mezquital.csv')
#########################################
###### Test map df ##############3
######################################
map_valle = pd.read_csv('Valle_map.csv')
map_pc = pd.read_csv('Huasteca_map.csv')

#####################################
############Edit data base ##########
#####################################

map_valle['municipio'].unique()
map_pc['municipio'].unique()
#Valle=p_valle['municipio']
dt_valle = map_valle.groupby(['municipio']).agg({'edad': 'mean'}).reset_index()
dt_huas =  map_pc.groupby(['municipio']).agg({'edad': 'mean'}).reset_index()
dt_entidad = pd.concat([dt_valle,dt_huas])
dt_entidad

##### APP DASH ##########
#######################
app = dash.Dash(__name__)
server = app.server
###########################

app.layout = html.Div([
    
    html.Div(children=[
        html.H1(children='Dashboard de los resultados en las regiones de Hidalgo'),
                html.Img(src='assets/CIAD.png'),

        html.Div(children= "La siguiente seccion es recopilacion de los datos de la base de datos de la huasteca Hidalguense"),
    ], className = 'banner'),

    html.Div([
        html.Div([
            html.P('Selecciona la Region', className = 'fix_label', style={'color':'black', 'margin-top': '2px'}),
            dcc.RadioItems(id = 'radioitms', 
                            labelStyle = {'display': 'inline-block'},
                            options = [
                                {'label' : 'LA HUASTECA', 'value' : 'region'},
                                {'label' : 'VALLE DEL MEZQUITAL', 'value' : 'region2'},
                            ], value = 'region',
                            style = {'text-aling': 'justify', 'color':'black'}, className = 'dcc_compon'),
        ], className = 'create_container2 five columns', style = {'bottom': 'center'}),
    ], className = 'row flex-display'),

#1 fecha de cosecha vs alimentos
    html.Div([
        html.Div([
         html.H2('Edad y cantidades de Hectareas'),
        dcc.Graph(id = 'barra_graph', figure = {})
        ], className = 'create_container2 eight columns'),

#2 estructura familiar
        html.Div([
        html.H2('Estructura Familiar'),
        dcc.Graph(id = 'pie_graph', figure = {})
        ], className = 'create_container2 six columns')
    ], className = 'row flex-display'),

#3 produccion por H

html.Div([
        html.Div([
         html.H2('Produccion por Hectareas'),
        dcc.Graph(id = 'barra_graph2', figure = {})
        ], className = 'create_container2 eight columns'),

#4 Encuestados por municipio
        html.Div([
        html.H2('Genero de los productores'),
        dcc.Graph(id = 'pie_graph4', figure = {})
        ], className = 'create_container2 six columns')
    ], className = 'row flex-display'),


# 5 Consumos de alimentos  
 html.Div([
        html.Div([
        html.H2('Frecuencia de consumo de alimentos'),
        dcc.Graph(id = 'barra_graph3', figure = {})
        ], className = 'create_container2 eight columns'),

#6 plagas
        html.Div([
        html.H2('Plagas'),# className= 'fix_label'),
        dcc.Graph(id = 'pie_graph6', figure = {})
        ], className = 'create_container2 six columns')
    ], className = 'row flex-display'),

# 7 Estudio  
 html.Div([
        html.Div([
        html.H2('Nivel de Estudio'),
        dcc.Graph(id = 'pie_graph7', figure = {})
        ], className = 'create_container2 eight columns'),

#8 Migración
        html.Div([html.H2('Migración'),
        dcc.Graph(id = 'box', figure = {})
        ], className = 'create_container2 six columns')
    ], className = 'row flex-display'),
    

], id='mainContainer', style={'display':'flex', 'flex-direction':'column'})


#1 fecha de cosecha vs alimentos
@app.callback(
    Output('barra_graph', component_property='figure'),
    [Input('radioitms', component_property='value')])

def update_graph(value):

    if value == 'region':
        fig = px.bar(
            data_frame = s, #ca,
            x = 'edad',
            y = 'ext_num',labels={'edad':'Edad del productor',
                'ext_num': 'Extensión de Hectareas'},)
    else:
        fig = px.bar(
            data_frame= df_valle,# ca,
            x = 'edad',
            y = 'ext_num',labels={'edad':'Edad',
                'ext_num': 'Extensión de Hectareas'},)
    return fig

#2 estructura familiar
@app.callback(
    Output('pie_graph', component_property='figure'),
    [Input('radioitms', component_property='value')])

def update_graph_pie(value):

    if value == 'region':
        fig2 = px.pie(
            data_frame = ud,
            names = 'familiar_modif',
            values = 'id')
    else:
        fig2 = px.pie(
            data_frame = df_productores2,
            names = 'parentesco',
            values = '_index')
    return fig2
#3 produccion por H
@app.callback(
    Output('barra_graph2', component_property='figure'),
    [Input('radioitms', component_property='value')])

def display_color(value):

    if value == 'region':
        fig3 = px.bar(
            data_frame =pc,
            x = 'edad',
             y = 'prod_hect2',
        labels={'edad':'Edad',
                'prod_hect2': 'Ton/H'},)
    else:
        fig3 = px.bar(
            data_frame= p_valle,
            x = 'edad',
            y = 'prod_hec',
         labels={'edad':'Edad',
                'prod_hec': 'Ton/H'},)
    return fig3


#cuatro ya quedo 

#4 Encuestados por municipio     
@app.callback(
    Output('pie_graph4', component_property='figure'),
    [Input('radioitms', component_property='value')])
def update_graph_sunburst (value):
    if value == 'region':
        fig4 = px.sunburst(
            data_frame=s,
            path=['municipio', 'sexo', 'edad'], 
            values='idUsuario')

    else:
        fig4 = px.sunburst(
            data_frame=df_valle,
            path=['municipio', 'sexo', 'edad'], 
            values='idUsuario')
    return fig4



#5 Consumos de alimentos 
@app.callback(

Output('barra_graph3', component_property='figure'),
[Input('radioitms', component_property='value')])

def display_structure(value):

    if value == 'region':
        fig5 = px.bar(
            data_frame =al,
            x = 'articulos',
             y = 'Freq_anual', facet_col='compra_venta',
            labels={'articulos':'Alimentos',
                'Freq_anual': 'Frecuencia de consumo',
                   'compra-venta':'Uso del alimento'},)
    else:
        fig5 = px.bar(
            data_frame =al2,
            x = 'articulos',
             y = 'Freq_anual',facet_col='compra_venta',
            labels={'articulos':'Alimentos',
                'Freq_anual': 'Frecuencia de consumo',
                   'compra-venta':'Uso del alimento'},)
        #fig5 = px.bar(
        #    data_frame= df_productores,
        #    x = '¿Que edad tiene?',
        #     y = '¿Número de terrenos que utiliza la familia?')
    return fig5

#6 plagas
@app.callback(
    Output('pie_graph6', component_property='figure'),
    [Input('radioitms', component_property='value')])
def update_graph_sunburst (value):
    if value == 'region':
        fig6 = px.sunburst(
            title='Tipo de Plagas',
            data_frame = pg,
            path=['nombre_modif','combate_modif'], 
            values='CantidadPlaga', hover_name="nombre_modif")
        fig6.update_traces(hovertemplate='<b>Número Total de plaga:%{value}<b><br><b>Como lo Combate:%{label}<b>')        

    else:
        fig6 = px.sunburst(
            title='Tipo de Plagas',
            data_frame = pg2,
            path=['nombre_modif','combate_modif'], 
            values='CantidadPlaga', hover_name="nombre_modif")
        fig6.update_traces(hovertemplate='<b>Número Total de plaga:%{value}<b><br><b>Como lo Combate:%{label}<b>') 
        #fig6 = px.sunburst(
        #    title='Actividades realizadas en el espacio de vida, y productos generados ',
        #    data_frame = df_productores2,
        #    path=['Nombre del espacio de vida','¿Cuantos productos obtiene de la actividad?'],
        #    names='Nombre del espacio de vida',
        #    values='¿Cuantas actividades realiza en el espacio de vida?', hover_name="Nombre del espacio de vida",
        #    hover_data={'Nombre del espacio de vida':False})
        #fig6.update_traces(hovertemplate='<b>Número de personas que realizan la actividad:%{value}<b><br><b>Numero de actividades Realizadas:%{label}<b>')        
    return fig6

#7 Estudio
@app.callback(
    Output('pie_graph7', component_property='figure'),
    [Input('radioitms', component_property='value')])

def update_graph_sunburst (value):
    if value == 'region':
        fig7 = px.sunburst(
            data_frame=ud,
            path=['sexo','estudio_modif', 'familiar_modif'], 
            values='est_i')
        fig7.update_traces(hovertemplate='<b>Número de personas que realizan la actividad:%{value}<b>')        


    else:
        fig7 = px.sunburst(
            data_frame=md,
            path=['sexo','estudio_modif', 'familiar_modif'], 
            values='est_i')
#            path=['Estudio','Edad'], 
#            values='Edad', hover_name="Estudio")
    return fig7

#8 Barra
@app.callback(
    Output('box', component_property='figure'),
    [Input('radioitms', component_property='value')])

def update_graph_box (value):
    if value == 'region':
        fig8 = px.box(
            data_frame=ud,
            title='Edad vs migración',
            y='edad',
            x='migracion_modif',)
    else:
        fig8 = px.box(
            data_frame=df_productores,
            title='Actividades vs edad',
            y='¿Que edad tiene?',
            x='¿Cuantas actividades realiza en el espacio de vida?',)
    return fig8


if __name__ == ('__main__'):
    app.run_server(debug=False)#,host="0.0.0.0", port=8080, use_reloader=False)
