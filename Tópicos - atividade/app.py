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
df_nomes  = df.groupby('Name')['Global_Sales'].sum().reset_index()
df_anos = df.groupby('Year')['Global_Sales'].sum().reset_index()
df_editor = df.groupby('Publisher')['Global_Sales'].sum().reset_index()
df_genero = df.groupby('Genre')['Global_Sales'].sum().reset_index()
df_na = df['NA_Sales'].sum()
df_eu = df['EU_Sales'].sum()
df_jp = df['JP_Sales'].sum()
df_gl = df['Global_Sales'].sum()

#Criação dos gráficos
nomes_fig = px.bar(df_nomes, x='Name', y='Global_Sales')
anos_fig = px.bar(df_anos, y="Year", x="Global_Sales", color="Year", orientation="h")
editor_fig = px.bar(df_editor, x="Global_Sales", y="Publisher", color="Publisher", orientation="h")
nomes_fig_pizza = px.pie(df_nomes, values='Global_Sales', names='Name', hole=.4)
genero_fig = px.pie(df_genero, values='Global_Sales', names='Genre', hole=.4)
region_fig = px.pie(values=[df_na,df_eu, df_jp, df_gl],
                    names=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales'],
                    hole=.4)
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
    dcc.Graph(figure=region_fig, id="region_fig"),
])

#Callbacks
@app.callback([
    Output("nomes_fig", "figure"),
    Output("anos_fig", "figure"),
    Output("editor_fig", "figure"),
    Output("nomes_fig_pizza", "figure"),    
    Output("genero_fig", "figure")
],
    [
    Input("checklist_name", "value")
])

def atualizar_graficos(nomes):
    df_nomes = df[df["Name"].isin(nomes)]
    
    faturamento = df_nomes.groupby('Name').sum().reset_index()
    anos = df_nomes.groupby('Year').sum().reset_index()
    editor = df_nomes.groupby("Publisher").sum().reset_index()
    genero = df_nomes.groupby("Gender").sum().reset_index()

    nomes_fig = px.bar(faturamento, x="Name", y="Global_Sales", template="plotly_dark")    
    anos_fig = px.bar(anos, y="Year",
                            x="Global_Sales",
                            orientation="h",
                            template="plotly_dark")

    editor_fig = px.bar(editor, x="Global_Sales",
                                y="Publisher", color="City", 
                                orientation="h",
                                template="plotly_dark")  

    nomes_fig_pizza = px.pie(df_nomes, values='Global_Sales',
                                       name='Name',
                                       hole=.4,
                                       template="plotly_dark")

    genero_fig = px.pie(genero, values='Global_Sales',
                                name='Gender', 
                                title='Faturamento por genero',
                                hole=.4,
                                template="plotly_dark")

    return nomes_fig, anos_fig, editor_fig, nomes_fig_pizza, genero_fig

if __name__ == "__main__":
    app.run_server(port=8051, debug=True)









