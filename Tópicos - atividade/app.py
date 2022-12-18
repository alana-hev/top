from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import dash
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

#========== Dados ============== #
df = pd.read_csv('vgsales.csv')

#Dados para os gráficos
df_nomes  = df.groupby('Name').sum().reset_index()
df_anos = df.groupby('Year').sum().reset_index()
df_editor = df.groupby('Publisher').sum().reset_index()
df_genero = df.groupby('Genre').sum().reset_index()
df_na = df.groupby('Na_Sales').sum().reset_index()
df_eu = df.groupby('Eu_Sales').sum().reset_index()
df_jp = df.groupby('Jp_Sales').sum().reset_index()

#Criação dos gráficos
nomes_fig = px.bar(df_nomes,x='Name',y='Global_Sales')
anos_fig = px.bar(df_anos, y="Year",
                    x="Global_Sales", color="Year",orientation="h")
editor_fig = px.bar(df_editor, x="Global_Sales",
                    y="Publisher", color="Publisher", orientation="h")

nomes_fig_pizza = px.pie(
        df_nomes, values='Global_Sales', 
        names='Name', hole=.4)

genero_fig = px.pie(
        df_genero, values='Global_Sales', 
        names='Genre', hole=.4)

na_fig = px.bar(df_na, y="Na_Sales",
                    x="Global_Sales", color="Na_Sales",orientation="h")

eu_fig = px.bar(df_eu, y="Eu_Sales",
                    x="Global_Sales", color="Eu_Sales",orientation="h")

jp_fig = px.bar(df_jp, y="Jp_Sales",
                    x="Global_Sales", color="Jp_Sales",orientation="h")

# =========  Layout  =========== #
app.layout = html.Div(children=[        
    html.H3("Relatório de Faturamento",style={'text-align':'center'}),
    html.Hr(),    
    dcc.Checklist(df['Name'].unique(), df['Name'].unique(), 
        id="checklist_name"),
    dcc.Graph(figure=nomes_fig,id="nomes_fig"),
    dcc.Graph(figure=anos_fig,id="anos_fig"),
    dcc.Graph(figure=editor_fig,id="editor_fig"),
    dcc.Graph(figure=nomes_fig_pizza,id="nomes_fig_pizza"),
    dcc.Graph(figure=genero_fig, id="genero_fig"),
    dcc.Graph(figure=na_fig, id="na_fig"),
    dcc.Graph(figure=eu_fig, id="eu_fig"),
    dcc.Graph(figure=jp_fig, id="jp_fig")
])

#Callbacks
@app.callback([
    Output("nomes_fig", "figure"),
    Output("anos_fig", "figure"),
    Output("editor_fig", "figure"),
    Output("nomes_fig_pizza", "figure"),    
    Output("genero_fig", "figure"),
    Output("na_fig", "figure"),
    Output("eu_fig", "figure"),
    Output("jp_fig", "figure"),
],
    [
    Input("checklist_name", "value")
])
def atualizar_graficos(nome):
    df_nomes = df[df["Name"].isin(nomes]
    
    faturamento = df_nomes.groupby('Name').sum().reset_index()
    anos = df_nomes.groupby('Year').sum().reset_index()
    editor = df_nomes.groupby("Publisher").sum().reset_index()
    genero = df_nomes.groupby("Gender").sum().reset_index()

    nomes_fig = px.bar(faturamento, x="Name", y="Global_Sales",
    template="plotly_dark")    
    anos_fig = px.bar(anos, y="Year",
                            x="Global_Sales", orientation="h",
                            template="plotly_dark")    
    editor_fig = px.bar(editor, x="Global_Sales",
                          y="Publisher", color="City", 
                          orientation="h",
                          template="plotly_dark")        
    nomes_fig_pizza = px.pie(df_name, 
    values='Global_Sales', name='Name', hole=.4,
    template="plotly_dark")
    genero_fig = px.pie(
        genero, values='Global_Sales', name='Gender', 
        title='Faturamento por genero',  hole=.4,
        template="plotly_dark")
    
   na_fig = px.pie(
        na, values='Global_Sales', name='Na_Sales', 
        title='Faturamentos pelo a_norte',  hole=.4,
        template="plotly_dark")
    
    eu_fig = px.pie(
        eu, values='Global_Sales', name='Eu_Sales', 
        title='Faturamentos pelo europa',  hole=.4,
        template="plotly_dark")
    
    jp_fig = px.pie(
        jp, values='Global_Sales', name='Jp_Sales', 
        title='Faturamentos pelo japao',  hole=.4,
        template="plotly_dark")

    return nomes_fig, anos_fig, editor_fig, nomes_fig_pizza, genero_fig, na_fig, eu_fig, jp_fig


if __name__ == "__main__":
    app.run_server(port=8051, debug=True)









