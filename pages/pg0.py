import pandas as pd
import json
import dash
from dash import dcc,html, callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np
import pathlib

dash.register_page(__name__, path = '/', name="Home")

## Données 
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("assets").resolve()

with open(DATA_PATH.joinpath("base_finale.txt"),'r') as file:
    dico_produits = json.load(file)

BASE_PRODUITS = pd.DataFrame.from_dict(dico_produits)


base_communes = pd.read_csv(DATA_PATH.joinpath("villes-france-codes-postaux.csv"),sep=';',decimal=',')
base_communes.rename(columns={"cp":"CP"}, inplace=True)
base_longlat = base_communes[["CP","latitude_degre","longitude_degre"]]
base_longlat = base_longlat.groupby("CP").agg(np.mean)
base_carte = BASE_PRODUITS.merge(base_longlat, how="left",on="CP")
#df = df.head(10)

fig = px.scatter_mapbox(base_carte, lat="latitude_degre", lon="longitude_degre",zoom=4)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()

nb_villes = len(pd.unique(BASE_PRODUITS["Ville"]))
nb_produits = len(pd.unique(BASE_PRODUITS["Nom_produit"]))
nb_magasins = len(pd.unique(BASE_PRODUITS["Adresse"]))


# page 0

alerte1 = dbc.Alert([
    html.H3(str(nb_magasins), style={"color":"#ffffff"}),
    html.H5("Magasins enregistés", style={"color":"#ffffff"})
],color="#1560bd")

alerte2 = dbc.Alert([
    html.H3(str(nb_villes), style={"color":"#ffffff"}),
    html.H5("Communes", style={"color":"#ffffff"})
],color="#00cccb")

alerte3 = dbc.Alert([
    html.H3(str(nb_produits), style={"color":"#ffffff"}),
    html.H5("Produits analysés", style={"color":"#ffffff"})
],color="#17657d")


layout = html.Div([
    dbc.Row([
        dbc.Col([alerte1],style={"textAlign":"center"}),
        dbc.Col([alerte2],style={"textAlign":"center"}),
        dbc.Col([alerte3],style={"textAlign":"center"})
    ], style = {"padding":"1rem 1rem"}),
    dbc.Row([
        dcc.Graph(
            id = "graphe_carrefours_france",
            figure = fig,
            style={"width":"58rem","margin-left":"1rem"}
        )
    ])
])

@callback(
    Output("graphe2","figure"),
    Input("produit2","children")
)

def afficher_p2(produit2):
    return None