from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

def createcontent(numberofbanks: int, designation: str = 'dashboard_app_'):
    children = []

    for i in range(numberofbanks):
        card = html.Div([
                html.Div([
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    dbc.RadioItems(id=f'{designation}fileselect{i}',
                                                   options=[],
                                                   value=[]
                                                   ),
                                ],
                                id=f'{designation}fileselect-accordion{i}',
                                title="Select Data",
                            ),
                            dbc.AccordionItem(
                                [
                                    dbc.Input(id=f"{designation}numberofscans{i}", type="number", value=1, max=50,
                                              persistence=True,
                                              persistence_type='session')
                                ],
                                title="LLC Buffer",
                            )
                        ],
                        className='fileselect-accordion',
                        start_collapsed=True),

                    html.Br(),
                    html.Button(id=f'{designation}replot{i}', n_clicks=0, children='Update Plots', className='btn rats-btn',
                                type='button'),
                    html.Br(),
                    html.P([], id=f'{designation}interscanprompt{i}', className='text-danger')
                ], className='card-header rats-card-header'),

                html.Div([
                    html.Div([
                        html.Div(id=f'{designation}error_detection{i}', children=[
                            dcc.Loading([
                                dcc.Graph(id=f'{designation}error_detection_plot{i}', figure={
                                    'layout': go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                                        modebar=dict(bgcolor='rgba(0,0,0,0)', color='grey', activecolor='lightgrey'))
                                })
                            ]),
                            html.Button(id=f'{designation}download-error_detection-btn{i}', children=[html.Img(src='/assets/download.svg', alt='Download Plot')],
                                        className='btn rats-btn-outline', type='button', n_clicks=0),
                            dcc.Download(id=f'{designation}download_error_detection_plot{i}')
                        ], className='col-6 text-center'),

                        html.Div(id=f'{designation}scope{i}', children=[
                            dcc.Loading([
                                dcc.Graph(id=f'{designation}scopeplot{i}', figure={
                                    'layout': go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                                        modebar=dict(bgcolor='rgba(0,0,0,0)', color='grey', activecolor='lightgrey'))
                                })
                            ]),
                            html.Button(id=f'{designation}download-scope-btn{i}', children=[html.Img(src='/assets/download.svg', alt='Download Plot')],
                                        className='btn rats-btn-outline', type='button', n_clicks=0),
                            dcc.Download(id=f'{designation}download_scope{i}')
                        ], className='col-6 text-center'),

                    ], className='row')
                ], className='card-body')

            ], className='card rats-card rats-single-card', style={'height': 'auto'})

        children.append(card)

    layout = html.Div([
        ########################################
        # dynamic plot content goes below, based on function output. Generic 3 entries for now - max 3 entries - one option could be subplots but lock to one entry
        ########################################
        html.Div(id='plots', children=children,
                 className='container-fluid text-center'),
        ########################################
    ], className='container-fluid')

    return layout








