import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash('Dash App Demo')
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


df = pd.read_csv('resources/ntf_training_app_df.csv', index_col=0)

month_dict = {
        '1':'Jan','2':'Feb','3':'Mar',
        '4':'Apr','5':'May','6':'Jun',
        '7':'Jul','8':'Aug','9':'Sep',
        '10':'Oct','11':'Nov','12':'Dec'
}

app.layout = html.Div([

    html.H1(children='Total sales two year for different regions per month'),
    html.Div(children='''
    Bar Graph showing sales region-wise and also monthly. You can choose the type of aggeration method that you would like to use
                    '''),
    html.Div([
    html.Div(''),
    html.Label('Dropdown'),
    dcc.Dropdown(
        id='agg',
        options=[{'label': i, 'value': i} for i in ['Average', 'Total']],
        value='Average'
                 ),
    ],style={'width': '48%', 'display': 'inline-block'}),


    dcc.Graph(id='region-sale'),

    dcc.Slider(
        id='month-slider',
        min=df['month'].min(),
        max=df['month'].max(),
        value=df['month'].min(),
        step=None,
        marks={str(month): month_dict[str(month)] for month in list(df['month'].unique())}
    ),


])

@app.callback(
    dash.dependencies.Output('region-sale', 'figure'),
    [dash.dependencies.Input('month-slider', 'value'),
     dash.dependencies.Input('agg','value')]
)
def update_figure(select_month, agg):

    filtered_df = df[df.month == select_month]
    traces = []
    filtered_df_gp = filtered_df.groupby(['region'])['total_sales_2years']


    if agg == 'Average': df_by_month = filtered_df_gp.mean().reset_index()
    else: df_by_month = filtered_df_gp.sum().reset_index()

    traces.append(go.Bar(
                        x=df_by_month['region'],
                        y=df_by_month['total_sales_2years'],
                        opacity=0.9)
                        )
    return {'data': traces,
            'layout': go.Layout(
                xaxis={'title':'Region'},
                yaxis={'title':'Sales'},
                legend={'x':0,'y':1}

            )}



if __name__ == '__main__':
    app.run_server(port=8004)