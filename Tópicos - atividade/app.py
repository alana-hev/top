from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import dash
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# ========== Dados ============== #
df = pd.read_csv('vgsales.csv')

# Dados para os gráficos
df_nomes = df[['Name', 'Global_Sales']].sort_values(by='Global_Sales', ascending=False)[:15]
df_anos = df.groupby('Year')['Global_Sales'].sum().reset_index()
df_editor = df.groupby('Publisher')['Global_Sales'].sum().reset_index().sort_values(by='Global_Sales', ascending=False)[:20]
df_genero = df.groupby('Genre')['Global_Sales'].sum().reset_index()
df_na = df['NA_Sales'].sum()
df_eu = df['EU_Sales'].sum()
df_jp = df['JP_Sales'].sum()
df_gl = df['Global_Sales'].sum()

# Criação dos gráficos
nomes_fig = px.bar(df_nomes, x='Name', y='Global_Sales')
anos_fig = px.bar(df_anos, y="Year", x="Global_Sales",
                  color="Year", orientation="h")
editor_fig = px.bar(df_editor, x="Global_Sales",
                    y="Publisher", color="Publisher", orientation="h")
nomes_fig_pizza = px.pie(
    df_nomes, values='Global_Sales', names='Name', hole=.4)
genero_fig = px.pie(df_genero, values='Global_Sales', names='Genre', hole=.4)
region_fig = px.pie(values=[df_na, df_eu, df_jp, df_gl],
                    names=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales'],
                    hole=.4)

# =========  Layout  =========== #
app.layout = html.Div(children=[
    html.H3("Relatório de Faturamento", style={'text-align': 'center'}),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.Label("Vendas:", className="mb-0"),
            dbc.RadioItems(
            options=[
                {"label": "Global", "value": 'Global_Sales'},
                {"label": "Europa", "value": 'EU_Sales'},
                {"label": "América do Norte", "value": 'NA_Sales'},
                {"label": "Japão", "value": 'JP_Sales'},
                {"label": "Outras", "value": 'Other_Sales'},
            ],
            value='Global_Sales',
            id="region",
        )], sm=3),
        dbc.Col([
            dcc.Graph(figure=nomes_fig, id="nomes_fig"),
            dcc.Graph(figure=anos_fig, id="anos_fig"),
            dcc.Graph(figure=editor_fig, id="editor_fig"),
            dcc.Graph(figure=nomes_fig_pizza, id="nomes_fig_pizza"),
            dcc.Graph(figure=genero_fig, id="genero_fig"),
            dcc.Graph(figure=region_fig, id="region_fig")
        ], sm=9)
    ])
])

# Callbacks


@app.callback([
    Output("nomes_fig", "figure"),
    Output("anos_fig", "figure"),
    Output("editor_fig", "figure"),
    Output("nomes_fig_pizza", "figure"),
    Output("genero_fig", "figure"),
],
    [
    Input("region", "value")
])
def atualizar_graficos(region):
    df_nomes = df[['Name', region]].sort_values(by=region, ascending=False)[:15]
    df_anos = df.groupby('Year')[region].sum().reset_index()
    df_editor = df.groupby('Publisher')[region].sum().reset_index().sort_values(by=region, ascending=False)[:20]
    df_genero = df.groupby('Genre')[region].sum().reset_index()

    nomes_fig = px.bar(df_nomes, x='Name', y=region)

    anos_fig = px.bar(df_anos, y="Year", x=region,
                    color="Year", orientation="h")
    editor_fig = px.bar(df_editor, x=region,
                        y="Publisher", color="Publisher", orientation="h")
    nomes_fig_pizza = px.pie(df_nomes,
                             values=region, names='Name', hole=.4)
    genero_fig = px.pie(df_genero, values=region, names='Genre', hole=.4)

    return nomes_fig, anos_fig, editor_fig, nomes_fig_pizza, genero_fig


if __name__ == "__main__":
    app.run_server(port=8051, debug=True)
