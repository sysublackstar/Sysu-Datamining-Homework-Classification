import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
import dateutil.relativedelta
import pandas as pd
from plotly import graph_objs as go


df = pd.read_csv('example.csv')
df['date'] = pd.to_datetime(df['date'])
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
available_columns = ['impressions', 'clicks', 'website_purchases', 'spend($)', 'revenue($)',
                     'ctr(%)', 'cvr(%)', 'cpm($)', 'cpc($)', 'roas']

# layout = dict(
#     autosize=True,
#     automargin=True,
#     margin=dict(l=30, r=30, b=20, t=40),
#     hovermode="closest",
#     plot_bgcolor="#F9F9F9",
#     paper_bgcolor="#F9F9F9",
#     legend=dict(font=dict(size=10), orientation="h"),
#     title="Satellite Overview",
#     mapbox=dict(
#         # accesstoken=mapbox_access_token,
#         style="light",
#         center=dict(lon=-78.05, lat=42.54),
#         zoom=7,
#     ),
# )

bar_layout = dict(
    height=600,
    # width=900,
    yaxis={
        'hoverformat': '.0f',
        'categoryorder': 'total ascending'},
    margin={'l': 200},
    hovermode='closest',
    # transition={'duration': 500},
    font=dict(color="#777777")
    # legend=dict(font=dict(size=15), orientation="h")
)

pie_layout = dict(
    margin=dict(t=50, b=0, l=0, r=0),
    font=dict(color="#777777"),
    hoverinfo="label+text+value+percent",
    # color_discrete_sequence=px.colors.sequential.RdBu,
    # legend=dict(
    #     font=dict(color="#CCCCCC", size="10"), bgcolor="rgba(0,0,0,0)"
    # )
)

line_layout = dict(
    height=600,
    yaxis={'hoverformat': '.0f'},
    margin={'b': 100},
    hovermode='closest',
    transition={'duration': 500},
    legend=dict(font=dict(size=15), orientation="h"),
)

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
# app = dash.Dash(external_stylesheets=[BS])
# app = dash.Dash()
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        html.Div(id="output-clientside"),
        # logo
        html.Div(
            [
                html.Div(className="one-third column"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H1(
                                    "垃圾分类器",
                                    style={
                                        "margin-bottom": "0px",
                                        "text-align": "center"},
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(className="one-third column")
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"}
        ),


    ])


@app.callback(
    Output('spend', 'figure'),
    [Input('dt-range', 'start_date'),
     Input('dt-range', 'end_date')])
def update_figure(start_date, end_date):
    fig = go.Figure()
    img_width = 1600
    img_height = 900
    scale_factor = 0.5
    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )

    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )

    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source="https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg")
    )

    # Configure other layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )
    return fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)


