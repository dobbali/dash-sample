import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


df = pd.read_csv('resources/ntf_training_app_df.csv', index_col=0)
df_region_sales = df.groupby(['region'])['total_sales_2years'].sum().reset_index()


app.layout = html.Div([

    html.H1(children='Total sales two year for different regions per month'),
    html.Div(children='''
        Basic Bar Graph showing sales region-wise
    '''),

    dcc.Graph(
        id='region-sale',
        figure={
                'data': [
                    go.Bar(
                        x=df_region_sales['region'],
                        y=df_region_sales['total_sales_2years']


                    )

                ],
                'layout': go.Layout(
                    xaxis={'title':'Region'},
                    yaxis={'title':'Sales Total'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    hovermode='closest'
                                    )
                }

                )
])

if __name__ == '__main__':
    app.run_server(port=8001)

