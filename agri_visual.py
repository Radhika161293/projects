import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc

df = pd.read_csv('agri.csv')

df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('/', '_').str.lower()

df['year'] = pd.to_numeric(df['year'], errors='coerce')

app = Dash(__name__)


top_rice_states = df.groupby('state_name')['rice_production_1000_tons'].sum().nlargest(7).reset_index()

top_wheat_states = df.groupby('state_name')['wheat_production_1000_tons'].sum().nlargest(5).reset_index()

top_oilseed_states = df.groupby('state_name')['oilseeds_production_1000_tons'].sum().nlargest(5).reset_index()

top_sunflower_states = df.groupby('state_name')['sunflower_production_1000_tons'].sum().nlargest(7).reset_index()

sugarcane_trend = df.groupby('year')['sugarcane_production_1000_tons'].sum().reset_index()

rice_wheat_trend = df.groupby('year')[['rice_production_1000_tons', 'wheat_production_1000_tons']].sum().reset_index()

wb_rice = df[df['state_name'] == 'West Bengal'].groupby('dist_name')['rice_production_1000_tons'].sum().reset_index().nlargest(10, 'rice_production_1000_tons')

up_wheat = df[df['state_name'] == 'Uttar Pradesh'].groupby('year')['wheat_production_1000_tons'].sum().nlargest(10).reset_index()

millet_trend = df.groupby('year')['pearl_millet_production_1000_tons'].sum().reset_index()

sorghum_data = df.groupby('state_name')[['kharif_sorghum_production_1000_tons', 'rabi_sorghum_production_1000_tons']].sum().reset_index()

top_groundnut_states = df.groupby('state_name')['groundnut_production_1000_tons'].sum().nlargest(7).reset_index()

top_soybean_states = df.groupby('state_name')[['soyabean_production_1000_tons', 'soyabean_yield_kg_per_ha']].sum().nlargest(5, 'soyabean_production_1000_tons').reset_index()

oilseed_data = df.groupby('state_name')['oilseeds_production_1000_tons'].sum().nlargest(10).reset_index()

yield_data = df.groupby('state_name')[['rice_yield_kg_per_ha', 'wheat_yield_kg_per_ha']].mean().reset_index()

app.layout = html.Div([
    html.H1("Indian Agricultural Data Visualization", style={'textAlign': 'center'}),

    html.Div([
        dcc.Graph(figure=px.bar(top_rice_states, x='state_name', y='rice_production_1000_tons',
                                title='Top 7 Rice Producing States in India'))
    ]),

    html.Div([
        dcc.Graph(figure=px.bar(top_wheat_states, x='state_name', y='wheat_production_1000_tons',
                                title='Top 5 Wheat Producing States in India')),
        dcc.Graph(figure=px.pie(top_wheat_states, names='state_name', values='wheat_production_1000_tons',
                                title='Percentage Share of Top 5 Wheat Producing States'))
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),

    html.Div([
        dcc.Graph(figure=px.bar(top_oilseed_states, x='state_name', y='oilseeds_production_1000_tons',
                                title='Top 5 Oilseed Producing States')),
        dcc.Graph(figure=px.bar(top_sunflower_states, x='state_name', y='sunflower_production_1000_tons',
                                title='Top 7 Sunflower Producing States'))
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),

    html.Div([
        dcc.Graph(figure=px.line(sugarcane_trend, x='year', y='sugarcane_production_1000_tons',
                                 title="India's Sugarcane Production in Last 50 Years"))
    ]),

    html.Div([
        dcc.Graph(figure=go.Figure([
            go.Scatter(x=rice_wheat_trend['year'], y=rice_wheat_trend['rice_production_1000_tons'],
                       mode='lines', name='Rice Production'),
            go.Scatter(x=rice_wheat_trend['year'], y=rice_wheat_trend['wheat_production_1000_tons'],
                       mode='lines', name='Wheat Production')
        ]).update_layout(title='Rice vs. Wheat Production in Last 50 Years', xaxis_title='Year',
                         yaxis_title='Production (1000 tons)'))
    ]),

    html.Div([
        dcc.Graph(figure=px.bar(wb_rice, x='dist_name', y='rice_production_1000_tons',
                                title='Top Districts in West Bengal for Rice Production'))
    ]),

    html.Div([
        dcc.Graph(figure=px.bar(up_wheat, x='year', y='wheat_production_1000_tons',
                                title='Top 10 Wheat Production Years in Uttar Pradesh'))
    ]),

    html.Div([
        dcc.Graph(figure=px.line(millet_trend, x='year', y='pearl_millet_production_1000_tons',
                                 title='Millet Production in India Over Last 50 Years')),
        dcc.Graph(figure=go.Figure([
            go.Bar(x=sorghum_data['state_name'], y=sorghum_data['kharif_sorghum_production_1000_tons'], name='Kharif Sorghum'),
            go.Bar(x=sorghum_data['state_name'], y=sorghum_data['rabi_sorghum_production_1000_tons'], name='Rabi Sorghum')
        ]).update_layout(barmode='group', title='Sorghum Production (Kharif and Rabi) by State'))
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),

    html.Div([
        dcc.Graph(figure=px.bar(top_groundnut_states, x='state_name', y='groundnut_production_1000_tons',
                                title='Top 7 States for Groundnut Production')),
        dcc.Graph(figure=px.bar(top_soybean_states, x='state_name', y='soyabean_production_1000_tons',
                                title='Soybean Production by Top 5 States'))
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),

    html.Div([
        dcc.Graph(figure=px.bar(oilseed_data, x='state_name', y='oilseeds_production_1000_tons',
                                title='Oilseed Production in Major States')),
        dcc.Graph(figure=go.Figure([
            go.Bar(x=yield_data['state_name'], y=yield_data['rice_yield_kg_per_ha'], name='Rice Yield'),
            go.Bar(x=yield_data['state_name'], y=yield_data['wheat_yield_kg_per_ha'], name='Wheat Yield')
        ]).update_layout(barmode='group', title='Rice vs Wheat Yield Across States', xaxis_title='State',
                         yaxis_title='Yield (Kg per ha)'))
    ], style={'display': 'flex', 'justifyContent': 'space-around'})
])

if __name__ == '__main__':
    app.run(debug=True)
