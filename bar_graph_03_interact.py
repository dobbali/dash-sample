import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


df = pd.read_csv('resources/ntf_training_app_df.csv', index_col=0)
df_region_sales = df.groupby(['region', 'month'])['total_sales_2years'].sum().reset_index()
month_dict = {
        '1':'Jan','2':'Feb','3':'Mar',
        '4':'Apr','5':'May','6':'Jun',
        '7':'Jul','8':'Aug','9':'Sep',
        '10':'Oct','11':'Nov','12':'Dec'
}



app.layout = html.Div([

    html.H1(children='Total sales two year for different regions per month'),
    html.Div(children='''
        Basic Bar Graph showing sales region-wise
    '''),

    dcc.Graph(id='region-sale'),

    dcc.Slider(
        id='month-slider',
        min=df['month'].min(),
        max=df['month'].max(),
        value=df['month'].min(),
        step=None,
        marks={str(month): month_dict[str(month)] for month in df['month'].unique()}
    )

])

@app.callback(
    dash.dependencies.Output('region-sale', 'figure'),
    [dash.dependencies.Input('month-slider', 'value')]
)
def update_figure(select_month):
    filtered_df = df[df.month == select_month]
    traces = []
    df_by_month = filtered_df.groupby(['region'])['total_sales_2years'].sum().reset_index()
    traces.append(go.Bar(
                        x=df_by_month['region'],
                        y=df_by_month['total_sales_2years'],
                        opacity=0.7)
                        )
    return {'data': traces,
            'layout': go.Layout(
                xaxis={'title':'Region'},
                yaxis={'title':'Sales'},
                legend={'x':0,'y':1}

            )}


if __name__ == '__main__':
    app.run_server(port=8003)
