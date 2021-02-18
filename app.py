import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import pandas as pd
import numpy as np


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
##external_stylesheets_2 = [dbc.themes.BOOTSTRAP]

#########################
#loading data
#########################
#path_general = '/Users/guillou/Documents/FLORENCE/FORMATION/FORMATIONS/OPEN-CLASSROOMS-DATA-SCIENTIST/7-IMPLEMENTATION_MODELE_SCORING/NOTEBOOK_JUPYTER/ressources_dash/'
#path_general = '/'
#path_reference = path_general + "valeurs_references_code.csv"
path_reference = "valeurs_references_code.csv"
#path_predInfo = path_general + "pred_infos_1000.csv"
path_predInfo = "pred_infos_1000.csv"

#mean values for all clients, defaut and non default clients, similar clients
reference3 = pd.read_csv(path_reference, index_col=0)
#general informations, probabilities and predictions
predInfo = pd.read_csv(path_predInfo, index_col = 0)

list_infoCredit = ['SK_ID_CURR','AMT_CREDIT','AMT_ANNUITY','CREDIT_DURATION','AMT_INCOME_TOTAL','DEBT_RATIO']
list_label_infoCredit = ['ID','MONTANT DU CREDIT','ANNUITES','DUREE DU CREDIT','REVENUS ANNUELS', "TAUX D'ENDETTEMENT"]
#selection de données pour table
predInfoCredit = predInfo[list_infoCredit][0:10]
predInfoCredit.rename(columns={'SK_ID_CURR': "ID", 'AMT_CREDIT': "MONTANT DU CREDIT", 'AMT_ANNUITY': "ANNUITES",
                             'CREDIT_DURATION':"DUREE DU CREDIT", 'AMT_INCOME_TOTAL':"REVENUS ANNUELS", 'DEBT_RATIO':"TAUX D'ENDETTEMENT"}, inplace= True)

#########################
#valeurs test
#########################

#valeur test pour table
#y = predInfoCredit[predInfoCredit['ID'] == 100002].to_dict('records')

#valeurs test pour Gauge
#x = round(predInfo['proba'][predInfo['SK_ID_CURR'] == 100008].values[0], 2)


###########################
#functions
###########################

#fonction pour tracer les barplots de caractéristiques générales et clients similaires
predInfo['code'] = predInfo['DAYS_BIRTHcategories'].astype(str) + predInfo['AMT_INCOME_TOTALcategories'].astype(str) + predInfo['DAYS_EMPLOYEDcategories'].astype(str)

def trace_bar_ligne(code):    
  fig3 = make_subplots(rows=1, cols=5)

  fig3.add_trace(go.Bar(y= reference3['DAYS_BIRTH_YEAR'][['mean_total', str(code)]],
                      x=['moyen', str(code)],
                      marker_color='#66AA00',
                       name = 'AGE'),
                row=1, col=1)
  fig3.add_trace(go.Bar(y= reference3['DAYS_EMPLOYED_YEAR'][['mean_total', str(code)]],
                       x=['moyen', str(code)],
                       marker_color = '#FF9900',
                      name = 'POSTE OCCUPE '), 
                row=1, col=3)
  fig3.add_trace(go.Bar(y= reference3['AMT_INCOME_TOTAL'][['mean_total', str(code)]],
                       x=['moyen', str(code)],
                       marker_color = '#FF7F0E',
                      name = 'REVENUS'),
                row=1, col=2)
  fig3.add_trace(go.Bar(y= reference3['CNT_CHILDREN'][['mean_total', str(code)]],
                       x=['moyen', str(code)],
                       marker_color = '#DC3912',
                      name = 'ENFANTS'),
                row=1, col=4)
  fig3.add_trace(go.Bar(y= reference3['FLAG_OWN_REALTY'][['mean_total', str(code)]],
                     x=['moyen', str(code)],
                     marker_color = '#B82E2E',
                    name = 'PROPRIETE'),
              row=1, col=5)
  #fig3.add_trace(go.Bar(y= reference3['TARGET'][['mean_total', str(simil)]],
  #                 x=['moyen', str(simil)],
  #                 marker_color = '#8C564B',
  #                name = 'TARGET'),
  fig3.update_layout( margin=dict(l=5, r=5, t=5, b=100))
  return fig3

def gauge_indicators(ID):
  fig5 = go.Figure()

  fig5.add_trace(go.Indicator(
    mode = "number+gauge+delta", value = round(predInfo['CREDIT_TERM'][predInfo['SK_ID_CURR'] == ID].values[0], 2),
    domain = {'x': [0.25, 1], 'y': [0.08, 0.24]},
    title = {'text' :"Credit term"},
    delta = {'reference': round(predInfo['CREDIT_TERM'].mean(), 2)},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, round(predInfo['CREDIT_TERM'].max(), 2)]},
        'threshold': {
            'line': {'color': "red", 'width': 2},
            'thickness': 0.75,
            'value':  round(predInfo['CREDIT_TERM'].mean(), 2)},
        'steps': [
            {'range': [0, round(predInfo['CREDIT_TERM'].mean(), 2)], 'color': "lightgray"},
            {'range': [round(predInfo['CREDIT_TERM'].mean(), 2), round(predInfo['CREDIT_TERM'].max(), 2)], 'color': "gray"}]
            }))

  fig5.add_trace(go.Indicator(
    mode = "number+gauge+delta", value = round(predInfo['AMT_GOODS_PRICE'][predInfo['SK_ID_CURR'] == ID].values[0], 2),
    domain = {'x': [0.25, 1], 'y': [0.265, 0.425]},
    title = {'text' :"Montant bien"},
    delta = {'reference': round(predInfo['AMT_GOODS_PRICE'].mean(), 2)},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, round(predInfo['AMT_GOODS_PRICE'].max(), 2)]},
        'threshold': {
            'line': {'color': "red", 'width': 2},
            'thickness': 0.75,
            'value': round(predInfo['AMT_GOODS_PRICE'].mean(), 2)},
        'steps': [
            {'range': [0, round(predInfo['AMT_GOODS_PRICE'].mean(), 2)], 'color': "lightgray"},
            {'range': [round(predInfo['AMT_GOODS_PRICE'].mean(), 2), round(predInfo['AMT_GOODS_PRICE'].max(), 2)], 'color': "gray"}]}))

  fig5.add_trace(go.Indicator(
    mode = "number+gauge+delta", value = round(predInfo['EXT_SOURCE_3'][predInfo['SK_ID_CURR'] == ID].values[0], 2),
    domain = {'x': [0.25, 1], 'y': [0.45, 0.61]},
    title = {'text' :"indicateur 3"},
    delta = {'reference': round(predInfo['EXT_SOURCE_3'].mean(), 2)},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 1]},
        'threshold': {
            'line': {'color': "red", 'width': 2},
            'thickness': 0.75,
            'value': round(predInfo['EXT_SOURCE_3'].mean(), 2)},
        'steps': [
            {'range': [0, round(predInfo['EXT_SOURCE_3'].mean(), 2)], 'color': "lightgray"},
            {'range': [round(predInfo['EXT_SOURCE_3'].mean(), 2), 1], 'color': "gray"}]}))

  fig5.add_trace(go.Indicator(
    mode = "number+gauge+delta", value = round(predInfo['EXT_SOURCE_2'][predInfo['SK_ID_CURR'] == ID].values[0], 2),
    domain = {'x': [0.25, 1], 'y': [0.635, 0.795]},
    title = {'text' :"indicateur 2"},
    delta = {'reference': round(predInfo['EXT_SOURCE_2'].mean(), 2)},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 1]},
        'threshold': {
            'line': {'color': "red", 'width': 2},
            'thickness': 0.75,
            'value': round(predInfo['EXT_SOURCE_2'].mean(), 2)},
        'steps': [
            {'range': [0, round(predInfo['EXT_SOURCE_2'].mean(), 2)], 'color': "lightgray"},
            {'range': [round(predInfo['EXT_SOURCE_2'].mean(), 2), 1], 'color': "gray"}]}))

  fig5.add_trace(go.Indicator(
    mode = "number+gauge+delta", value = round(predInfo['EXT_SOURCE_1'][predInfo['SK_ID_CURR'] == ID].values[0], 2),
    domain = {'x': [0.25, 1], 'y': [0.82, 0.98]},
    title = {'text' :"indicateur 1"},
    delta = {'reference': round(predInfo['EXT_SOURCE_1'].mean(), 2)},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 1]},
        'threshold': {
            'line': {'color': "red", 'width': 2},
            'thickness': 0.75,
            'value': round(predInfo['EXT_SOURCE_1'].mean(), 2)},
        'steps': [
            {'range': [0, round(predInfo['EXT_SOURCE_1'].mean(), 2)], 'color': "lightgray"},
            {'range': [round(predInfo['EXT_SOURCE_1'].mean(), 2), 1], 'color': "gray"}]}))
  #fig5.update_layout(height = 300 , margin = {'t':0, 'b':0, 'l':0})

  fig5.update_layout(
    #autosize=False,
    width=570,
    height=400,
    margin=dict(
        l=0,
        r=0,
        b=5,
        t=20,
        pad=4))

  return fig5

def var_graph_tx(ID):
    """plots the variation in the debt ratio as a function of the duration of the loan,
    the minimum loan term with a maximum debt ratio set at 33%"""
    
    #data formatting
    tx_act = predInfo['DEBT_RATIO'][predInfo['SK_ID_CURR'] == ID].values[0]
    duree_act = predInfo['CREDIT_DURATION'][predInfo['SK_ID_CURR'] == ID].values[0]
    cred = predInfo['AMT_CREDIT'][predInfo['SK_ID_CURR'] == ID].values[0]
    rev = predInfo['AMT_INCOME_TOTAL'][predInfo['SK_ID_CURR'] == ID].values[0]
    duree_min = round(cred/(0.33*rev),1)
    
    duration = []
    tx = []
    for i in range(10, 31, 5):
        x = round(cred/(i*rev), 2)
        duration.append(i)
        tx.append(x)
    
    duration.append(duree_act)
    duration.append(duree_min)
    duration = sorted(duration)
    
    tx.append(tx_act/100)
    tx.append(0.33)
    tx = sorted(tx, reverse = True)
    
    #graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=duration,
        y=tx,
        line_color="green"
    ))

    fig.update_layout(
        title="Endettement en fonction de la durée du prêt",
        xaxis_title="durée du prêt (années)",
        yaxis_title="taux d'endettement",
        autosize=False,
        width=430,
        height=400,
        margin=dict(
            l=50,
            r=0,
            b=50,
            t=50,
            pad=4
        ),
        #paper_bgcolor="lightgray",
    )
    #fig.show()        
    return fig

df2 = pd.DataFrame(predInfo['NAME_FAMILY_STATUS'].value_counts())
fig6 = px.bar(df2, y="NAME_FAMILY_STATUS", orientation = 'v')
fig6.update_traces(marker_color='gray')
fig6.update_layout( margin=dict(l=5, r=50, t=5, b=5))

df7 = pd.DataFrame(predInfo['NAME_INCOME_TYPE'].value_counts())
fig7 = px.bar(df7, y="NAME_INCOME_TYPE", orientation = 'v', range_color= '#8C564B')
fig7.update_traces(marker_color='gray')
fig7.update_layout( margin=dict(l=0, r=0, t=5, b=5))

#########################
#initialize app
#########################
app = dash.Dash(__name__, external_stylesheets= external_stylesheets)


app.layout = html.Div([
    #row1
    html.Div([
      html.H2(
        children='Evaluation du risque de défaut de paiement',
        style={'textAlign': 'center', 'backgroundColor': 'lightgray'}
        )
    ], className = 'row'),

    #row2
    html.Div([
        html.H4(children="Veuillez saisir l'identifiant :",
                style={'textAlign': 'left'}),
        dcc.Input(id='input-1-state', type='text', value=100003, style={'width' : '220px'}),

        dbc.Button(id='submit-button-state', n_clicks=0, children='Submit', style={'width' : '220px'})#,   

        #html.Div(id='output-state', style={'textAlign': 'left'})
      ], className = 'row'),
#######################################
#§zone de saisie et affichage du risque
#######################################
    #row3
    html.Div([      
 #     html.Div([
        #left col
        html.Div([
    ########################################   
    #§infos descriptives relatives au client
    ########################################
            html.H3(children="Informations client",
                    style={'textAlign': 'center'}),
            dcc.Dropdown(
                id = "dropdown0",
                options = [
                    {'label' : 'Age', 'value' : 'BIRTH'},
                    {'label' : 'Durée contrat de travail (années)', 'value' : 'EMPLOYED'},
                    {'label' : 'Salaire annuel (dollars)', 'value' : 'INCOME'},
                    {'label' : 'Situation familiale', 'value' : 'STATUS'},
                    {'label' : 'Situation logement' , 'value' : 'REALTY'},
                    {'label' : 'Enfants', 'value': 'CHILDREN'},
                    {'label' : 'Source de revenus', 'value' : 'SOURCE'}], 
                style={'textAlign': 'center'},                
                value = 'BIRTH'),
            html.H3(
                id='text_value', 
                style={'textAlign' : 'center',
                       'color' : 'green'}),
            #dcc.Graph(id='gauge_chart2')

          ], className = 'four columns'),

        #right col       
        html.Div([
            html.H3("Eléments d'interprétation du risque", style={'textAlign': 'center'}),

            html.Div(
              style = {'marginLeft' : '0.5%', 'marginRight' : '0.5%', 'marginBottom' : '.5%'},
              children = [
              html.Div(
                style = {'width':'19.0%', 'backgroundColor': 'lightgray', 'display': 'inline-block', 'marginRight':'.8%'},
                children = [html.P(style = {'textAlign' : 'center',
                                            'fontWeight' : 'bold', 'color' : 'gray', 'padding' : '1rem'},
                                  children = "Montant du crédit"),
                            html.H3(style={'textAlign' : 'center', 
                                          'color' : 'green'},
                                    id = 'montantCredit')]),
                                    
              html.Div(
                style = {'width':'19.0%', 'backgroundColor': 'lightgray', 'display': 'inline-block', 'marginRight':'.8%'},
                children = [html.P(style = {'textAlign' : 'center',
                                            'fontWeight' : 'bold', 'color' : 'gray', 'padding' : '1rem'},
                                  children = "Durée du crédit"),
                            html.H3(style={'textAlign' : 'center',
                                          'color' : 'green'},
                                    id = 'dureeCredit')]),
              html.Div(
                style = {'width':'19.0%', 'backgroundColor': 'lightgray', 'display': 'inline-block', 'marginRight':'.8%'},
                children = [html.P(style = {'textAlign' : 'center',
                                            'fontWeight' : 'bold', 'color' : 'gray', 'padding' : '1rem'},
                                  children = "Annuités"),
                            html.H3(style={'textAlign' : 'center',
                                          'color' : 'green'},
                                    id = 'annuites')]),
              html.Div(
                style = {'width':'19.0%', 'backgroundColor': 'lightgray', 'display': 'inline-block', 'marginRight':'.8%'},
                children = [html.P(style = {'textAlign' : 'center',
                                            'fontWeight' : 'bold', 'color' : 'gray', 'padding' : '1rem'},
                                  children = "Revenus annuels"),
                            html.H3(style={'textAlign' : 'center',
                                          'color' : 'green'},
                                    id = 'revAnn')]),
              html.Div(
                style = {'width':'19.0%', 'backgroundColor': 'lightgray', 'display': 'inline-block', 'marginRight':'.8%'},
                children = [html.P(style = {'textAlign' : 'center',
                                            'fontWeight' : 'bold', 'color' : 'gray', 'padding' : '1rem'},
                                  children = "Taux d'endettement"),
                            html.H3(style={'textAlign' : 'center',
                                          'color' : 'green'},
                                    id = 'txEndet')]),  
              ], className = 'eight columns'),

    ],className = 'row'),
      

#####################################
#§éléments d'interprétation du risque
#####################################
    #row4
    html.Div([
        html.Div([
          dcc.Graph(id='gauge_chart2')
          #html.H5(
           # id='output-state', 
            #style={'textAlign': 'center'})
          ],className = 'four columns'), 
        html.Div([
          dcc.Graph(id = 'gauge_ind')
          ],className = 'four columns'),
        html.Div([
          dcc.Graph(id = 'tx_endet')
          ], className = 'four columns')

      ], className = 'row'),

    html.Div([
        #left col
        html.Div([

          ], className = 'five columns'),
        #middle col
        html.Div([
          ])
          ], className = 'three columns'),
        #right col
        html.Div([
          #
          ], className = 'four columns')
    ], className = 'row'),


############################
#§infos générales clientèle
############################
    #row5
    html.Div([
      html.Div([
        html.H3('Situation familiale', style={'textAlign' : 'center'}),
        dcc.Graph(figure = fig6)
        ], className = 'three columns'),
      html.Div([
        html.H3('Situation professionnelle', style={'textAlign' : 'center'}),
        dcc.Graph(figure = fig7)
        ], className = 'three columns'),
      html.Div([
        html.H3(
            children = 'Informations générales clientèle',
            style={'textAlign': 'center'}
            ),
        dcc.Graph(id= "4graph"),
        html.Div('AGE: 0:<30 ans, 1:30< <45ans, 2:45< <60ans, 3:>60 ans | REVENUS: 0:<50k, 1:50< <75ans, 2:75< <100ans, 3:>100 ans | EMPLOI: 0:>2ans, 1:<2ans')
        ], className = 'six columns')  
      
    ], className = 'row')
    
])

################################
#callbacks
################################

#@app.callback(Output('output-state', 'children'),
#              Input('submit-button-state', 'n_clicks'),
#              State('input-1-state', 'value'))
#def update_output(n_clicks, input1):
    #y = round(predInfo['proba'][predInfo['SK_ID_CURR'] == input1].values[0], 2)
#    y = round(predInfo[predInfo['SK_ID_CURR'] == int(input1)]['proba'].values[0], 2)
#    return u'''
#        Risque de défaut de paiement estimé à {}.
#    '''.format(y)


@app.callback(Output('gauge_chart2', 'figure'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))
def update_gauge(n_clicks, input1):
    round_score = round(predInfo[predInfo['SK_ID_CURR'] == int(input1)]['proba'].values[0],2),
    if round_score[0] <0.5:
        bar_color = '#66AA00'
    elif round_score[0] <0.6:
        bar_color = '#FF9900'
    elif round_score[0] <0.70:
        bar_color = '#FF7F0E'
    elif round_score[0] <0.80:
        bar_color = '#DC3912'
    elif round_score[0] <0.90:
        bar_color = '#B82E2E'
    else:
        bar_color = '#8C564B'

    fig = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = round_score[0],
      title = {'text': "Echelle de risque"},
      domain = {'x': [0, 1], 'y': [0, 1]},
      gauge = {'axis': {'range': [0,1]},
              'bar':{'color': bar_color}}
      )) 
    return fig 


@app.callback(Output('montantCredit', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))
def update_montantCredit(n_clicks, input1):
  return round(predInfo['AMT_CREDIT'][predInfo['SK_ID_CURR'] == int(input1)].values[0], 2)

@app.callback(Output('dureeCredit', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))
def update_montantCredit(n_clicks, input1):
  return round(predInfo['CREDIT_DURATION'][predInfo['SK_ID_CURR'] == int(input1)].values[0], 2)

@app.callback(Output('annuites', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))
def update_montantCredit(n_clicks, input1):
  return round(predInfo['AMT_ANNUITY'][predInfo['SK_ID_CURR'] == int(input1)].values[0], 2)

@app.callback(Output('revAnn', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))
def update_montantCredit(n_clicks, input1):
  return round(predInfo['AMT_INCOME_TOTAL'][predInfo['SK_ID_CURR'] == int(input1)].values[0], 2)

@app.callback(Output('txEndet', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))
def update_montantCredit(n_clicks, input1):
  return round(predInfo['DEBT_RATIO'][predInfo['SK_ID_CURR'] == int(input1)].values[0], 2)    



@app.callback(Output('text_value', 'children'),
              Input('dropdown0', 'value'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))    
def update_text_value(dropdownvalue, n_clicks, input1):
  if dropdownvalue == 'BIRTH':
    textDisplay = predInfo['DAYS_BIRTH_YEAR'][predInfo['SK_ID_CURR'] == int(input1)]
  elif dropdownvalue == 'EMPLOYED':
    textDisplay = predInfo['DAYS_EMPLOYED_YEAR'][predInfo['SK_ID_CURR'] == int(input1)]
  elif dropdownvalue == 'INCOME':
    textDisplay = predInfo['AMT_INCOME_TOTAL'][predInfo['SK_ID_CURR'] == int(input1)]
  elif dropdownvalue == 'STATUS':
    textDisplay = predInfo['NAME_FAMILY_STATUS'][predInfo['SK_ID_CURR'] == int(input1)]
  elif dropdownvalue == 'REALTY':
    textDisplay = predInfo['FLAG_OWN_REALTY_NAME'][predInfo['SK_ID_CURR'] == int(input1)]
  elif dropdownvalue == 'CHILDREN':
    textDisplay = predInfo['CNT_CHILDREN'][predInfo['SK_ID_CURR'] == int(input1)]
  elif dropdownvalue == 'SOURCE':
    textDisplay = predInfo['NAME_INCOME_TYPE'][predInfo['SK_ID_CURR'] == int(input1)]    
  return textDisplay


@app.callback(Output('gauge_ind', 'figure'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))
def update_gauge_indicators(n_clicks, input1):
  return gauge_indicators(int(input1))

@app.callback(Output('tx_endet', 'figure'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))
def update_graph_endet(n_clicks, input1):
  return var_graph_tx(int(input1))


@app.callback(Output('4graph', 'figure'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))
def update_graph_carcateristic(n_clicks, input1):
  code = predInfo['code'][predInfo['SK_ID_CURR'] == int(input1)].values[0]
  return trace_bar_ligne(code)


if __name__ == '__main__':
    app.run_server(debug=True)
