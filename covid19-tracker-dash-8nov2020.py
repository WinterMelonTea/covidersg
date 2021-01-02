#Imports
import dash
import dash_html_components as html
import dash_core_components as dcc
import xlrd
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc

#It has come to my attention that we will have to separate the project into multiple apps.
#For this file, we will do the Global Total Cases with search input.

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server #Meant for Heroku.
#Import Documents
the_df = pd.read_excel('covid_19_dataset_recovered.xlsx', skiprows=1)

# 1 | Global Variables =========
# Store a list of possible countries to choose from.
options = []
locations = the_df['location'].unique()
for location in locations:
    mydict = {}
    mydict['label'] = location
    mydict['value'] = location
    options.append(mydict)
options


# Get a whole list of additional data that you want stored in individual variables.



# 2 | Initial Graph (by default) ========
# You can show the 'global' cases as the default.
fig_321_a = px.line()
fig_321_b = px.line()
fig_321_c = px.line()
fig_321_d = px.line()
fig_321_e = px.line()
fig_321_f = px.line()
fig_321_g = px.line()


# 3 | HTML Layout (best to create a simple layout in CODEPLY or your own HTML document first) ========
app.layout = html.Div([
    html.Div([
        html.H3('Please select the location: ', style={'display':'inline-block', 'margin':'0', 'color':'white'}),
        dcc.Dropdown(
            id='country-picker',
            options = options,
            value = 'World',
            multi = False,
            style={'display':'inline-block', 'width':'40%', 'width':'250px', 'marginLeft':'10px', 'marginRight':'10px'}
        ),
        html.Div(id='the-output', style={'font-size':'400%', 'margin':'20px 0 25px 0', 'color':'white'}),
        dbc.Row([
            dbc.Col([
                dcc.Markdown('**POPULATION:** ', style={'color':'white'}),
                dcc.Markdown(id='popn', style={'color':'white'})
            ], lg=2, md=4, sm=6),
            dbc.Col([
                dcc.Markdown('**CURRENT TOTAL CASES:** ', style={'color':'white'}),
                dcc.Markdown(id='current-total', style={'color':'white'})
            ], lg=2, md=4, sm=6),
            dbc.Col([
                dcc.Markdown('**NEW CASES TODAY** ', style={'color':'white'}),
                dcc.Markdown(id='new-cases-text', style={'color':'white'})
            ], lg=2, md=4, sm=6),
            dbc.Col([
                dcc.Markdown('**NEW DEATHS TODAY** ', style={'color':'white'}),
                dcc.Markdown(id='new-deaths-text', style={'color':'white'})
            ], lg=2, md=4, sm=6),
            dbc.Col([
                dcc.Markdown('**NEW RECOVERED TODAY** ', style={'color':'white'}),
                dcc.Markdown(id='new-recovered-text', style={'color':'white'})
            ], lg=2, md=4, sm=6),
            dbc.Col([
                dcc.Markdown('**CURRENT ACTIVE CASES** ', style={'color':'white'}),
                dcc.Markdown(id='active-text', style={'color':'white'})
            ], lg=2, md=4, sm=6)
        ])
    ], style={'padding':'7% 5%', 'textAlign':'center'}),
    dbc.Row([
        dbc.Col(dcc.Graph(id='my_graph1', figure = fig_321_a),lg=6,sm=12),
        dbc.Col(dcc.Graph(id='my_graph2', figure = fig_321_b),lg=6,sm=12)],
        no_gutters = True),
    dbc.Row([
        dbc.Col(dcc.Graph(id='my_graph3', figure = fig_321_c),lg=6,sm=12),
        dbc.Col(dcc.Graph(id='my_graph4', figure = fig_321_d),lg=6,sm=12)],
        no_gutters = True),
    dbc.Row([
        dbc.Col(dcc.Graph(id='my_graph5', figure = fig_321_e),lg=6,sm=12),
        dbc.Col(dcc.Graph(id='my_graph6', figure = fig_321_f),lg=6,sm=12)],
        no_gutters = True),
    dbc.Row([
        dbc.Col(dcc.Graph(id='my_graph7', figure = fig_321_g))])
], style={'backgroundColor':'grey', 'overflow-x':'hidden'})


#3.5 | Extra Callbacks and Functions =======
@app.callback(
    Output('the-output', 'children'),
    [Input('country-picker', 'value')]
)

def update_text(country):
    return country

@app.callback(
    Output('popn', 'children'),
    [Input('country-picker', 'value')]
)

def update_text2(country):
    dfa = the_df[the_df['location']==country]
    return '{:,}'.format(dfa['population'].max())


@app.callback(
    Output('current-total', 'children'),
    [Input('country-picker', 'value')]
)

def update_text3(country):
    dfa = the_df[the_df['location']==country]
    return '{:,}'.format(dfa['total_cases'].max())

@app.callback(
    Output('new-cases-text', 'children'),
    [Input('country-picker', 'value')]
)

def update_text4(country):
    dfa = the_df[the_df['location']==country]
    return '{:,}'.format(dfa['new_cases'].iloc[-1])

@app.callback(
    Output('new-deaths-text', 'children'),
    [Input('country-picker', 'value')]
)

def update_text5(country):
    dfa = the_df[the_df['location']==country]
    return '{:,}'.format(dfa['new_deaths'].iloc[-1])

@app.callback(
    Output('new-recovered-text', 'children'),
    [Input('country-picker', 'value')]
)

def update_text6(country):
    dfa = the_df[the_df['location']==country]
    return '{:,}'.format(dfa['new_recovered'].iloc[-1])

@app.callback(
    Output('active-text', 'children'),
    [Input('country-picker', 'value')]
)

def update_text7(country):
    dfa = the_df[the_df['location']==country]
    return '{:,}'.format(dfa['active_cases'].iloc[-1])


# 4 | Callback and Function 1 - Total Cases ========
@app.callback(
    Output('my_graph1', 'figure'),
    [Input('country-picker', 'value')]
)

def update_graph1(country):
    c_df1 = the_df[the_df['location']==country]
    g_type1 = 'total_cases'
    fig_321_a = px.bar(c_df1,
                       x='date',
                       y=g_type1,
                       hover_data={
                        'date':False,
                        g_type1:False,
                        'Total Cases':(':,', c_df1[g_type1])
                       })
    fig_321_a.data[-1].showlegend=True
    fig_321_a.data[-1].name = 'Total Cases'

    fig_321_a.update_traces(marker_color='#ff9999', marker_line_width = 0)
    fig_321_a.update_layout(hovermode = 'x unified', legend_title = 'Legend',
                            title={
                                'text': "Total Cases",
                                'y':0.95,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                            font=dict(
                                family="Arial",
                                color='white'
                                ),
                            plot_bgcolor = 'grey',
                            paper_bgcolor = 'grey',
                            legend = dict(orientation = 'h', x=0.8, y=-0.15)
                           )

    fig_321_a.add_shape(type='line',
                        xref='paper',
                        x0=0, x1=1,
                        y0=c_df1[g_type1].mean(),
                        y1=c_df1[g_type1].mean(),
                        line=dict(color='black'))

    fig_321_a.add_annotation(
        x = '2020-02-15',
        y = c_df1[g_type1].mean(),
        showarrow=True,
        text = 'Average: '+ str('{:,.0f}'.format(c_df1[g_type1].mean())),
        bgcolor='black'
    )

    fig_321_a.update_yaxes(title='Number of Cases', gridcolor='lightgrey')
    fig_321_a.update_xaxes(title='Date')
    return fig_321_a

# 5 | Callback and Function 2 - New Cases ========
@app.callback(
    Output('my_graph2', 'figure'),
    [Input('country-picker', 'value')]
)

def update_graph2(country):
    c_df2 = the_df[the_df['location']==country]
    g_type2 = 'new_cases'
    fig_321_b = px.bar(c_df2,
                       x='date',
                       y=g_type2,
                       hover_data={
                        'date':False,
                        g_type2:False,
                        'New Cases':(':,', c_df2[g_type2])
                       })
    fig_321_b.data[-1].showlegend=True
    fig_321_b.data[-1].name = 'New Cases'

    fig_321_b.update_traces(marker_color='#ff9999', marker_line_width = 0)
    fig_321_b.update_layout(hovermode = 'x unified', legend_title = 'Legend',
                            title={
                                'text': "New Cases",
                                'y':0.95,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                            font=dict(
                                family="Arial",
                                color='white'
                                ),
                            plot_bgcolor = 'grey',
                            paper_bgcolor = 'grey',
                            legend = dict(orientation = 'h', x=0.8, y=-0.15)
                           )

    fig_321_b.add_shape(type='line',
                        xref='paper',
                        x0=0, x1=1,
                        y0=c_df2[g_type2].mean(),
                        y1=c_df2[g_type2].mean(),
                        line=dict(color='black'))

    fig_321_b.add_annotation(
        x = '2020-02-15',
        y = c_df2[g_type2].mean(),
        showarrow=True,
        text = 'Average: '+ str('{:,.0f}'.format(c_df2[g_type2].mean())),
        bgcolor='black'
    )

    fig_321_b.update_yaxes(title='Number of Cases', gridcolor='lightgrey')
    fig_321_b.update_xaxes(title='Date')
    return fig_321_b

# 6 | Callback and Function 3 - Total Deaths ========
@app.callback(
    Output('my_graph3', 'figure'),
    [Input('country-picker', 'value')]
)

def update_graph3(country):
    c_df3 = the_df[the_df['location']==country]
    g_type3 = 'total_deaths'
    fig_321_c = px.bar(c_df3,
                       x='date',
                       y=g_type3,
                       hover_data={
                        'date':False,
                        g_type3:False,
                        'Total Deaths':(':,', c_df3[g_type3])
                       })
    fig_321_c.data[-1].showlegend=True
    fig_321_c.data[-1].name = 'Total Deaths'

    fig_321_c.update_traces(marker_color='black', marker_line_width = 0)
    fig_321_c.update_layout(hovermode = 'x unified', legend_title = 'Legend',
                            title={
                                'text': "Total Deaths",
                                'y':0.95,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                            font=dict(
                                family="Arial",
                                color='white'
                                ),
                            plot_bgcolor = 'grey',
                            paper_bgcolor = 'grey',
                            legend = dict(orientation = 'h', x=0.8, y=-0.15)
                           )

    fig_321_c.add_shape(type='line',
                        xref='paper',
                        x0=0, x1=1,
                        y0=c_df3[g_type3].mean(),
                        y1=c_df3[g_type3].mean(),
                        line=dict(color='black'))

    fig_321_c.add_annotation(
        x = '2020-02-15',
        y = c_df3[g_type3].mean(),
        showarrow=True,
        text = 'Average: '+ str('{:,.0f}'.format(c_df3[g_type3].mean())),
        bgcolor='black'
    )

    fig_321_c.update_yaxes(title='Number of Cases', gridcolor='lightgrey')
    fig_321_c.update_xaxes(title='Date')
    return fig_321_c

# 6 | Callback and Function 3 - New Deaths ========
@app.callback(
    Output('my_graph4', 'figure'),
    [Input('country-picker', 'value')]
)

def update_graph4(country):
    c_df4 = the_df[the_df['location']==country]
    g_type4 = 'new_deaths'
    fig_321_d = px.bar(c_df4,
                       x='date',
                       y=g_type4,
                       hover_data={
                        'date':False,
                        g_type4:False,
                        'New Deaths':(':,', c_df4[g_type4])
                       })
    fig_321_d.data[-1].showlegend=True
    fig_321_d.data[-1].name = 'New Deaths'

    fig_321_d.update_traces(marker_color='black', marker_line_width = 0)
    fig_321_d.update_layout(hovermode = 'x unified', legend_title = 'Legend',
                            title={
                                'text': "New Deaths",
                                'y':0.95,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                            font=dict(
                                family="Arial",
                                color='white'
                                ),
                            plot_bgcolor = 'grey',
                            paper_bgcolor = 'grey',
                            legend = dict(orientation = 'h', x=0.8, y=-0.15)
                           )

    fig_321_d.add_shape(type='line',
                        xref='paper',
                        x0=0, x1=1,
                        y0=c_df4[g_type4].mean(),
                        y1=c_df4[g_type4].mean(),
                        line=dict(color='black'))

    fig_321_d.add_annotation(
        x = '2020-02-15',
        y = c_df4[g_type4].mean(),
        showarrow=True,
        text = 'Average: '+ str('{:,.0f}'.format(c_df4[g_type4].mean())),
        bgcolor='black'
    )

    fig_321_d.update_yaxes(title='Number of Cases', gridcolor='lightgrey')
    fig_321_d.update_xaxes(title='Date')
    return fig_321_d

# 7 | Callback and Function 3 - Total Recovered ========
@app.callback(
    Output('my_graph5', 'figure'),
    [Input('country-picker', 'value')]
)

def update_graph5(country):
    c_df5 = the_df[the_df['location']==country]
    g_type5 = 'total_recovered'
    fig_321_e = px.bar(c_df5,
                       x='date',
                       y=g_type5,
                       hover_data={
                        'date':False,
                        g_type5:False,
                        'Total Recovered':(':,', c_df5[g_type5])
                       })
    fig_321_e.data[-1].showlegend=True
    fig_321_e.data[-1].name = 'Total Recovered'

    fig_321_e.update_traces(marker_color='lightgreen', marker_line_width = 0)
    fig_321_e.update_layout(hovermode = 'x unified', legend_title = 'Legend',
                            title={
                                'text': "Total Recovered",
                                'y':0.95,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                            font=dict(
                                family="Arial",
                                color='white'
                                ),
                            plot_bgcolor = 'grey',
                            paper_bgcolor = 'grey',
                            legend = dict(orientation = 'h', x=0.8, y=-0.15)
                           )

    fig_321_e.add_shape(type='line',
                        xref='paper',
                        x0=0, x1=1,
                        y0=c_df5[g_type5].mean(),
                        y1=c_df5[g_type5].mean(),
                        line=dict(color='black'))

    fig_321_e.add_annotation(
        x = '2020-02-15',
        y = c_df5[g_type5].mean(),
        showarrow=True,
        text = 'Average: '+ str('{:,.0f}'.format(c_df5[g_type5].mean())),
        bgcolor='black'
    )

    fig_321_e.update_yaxes(title='Number of Cases', gridcolor='lightgrey')
    fig_321_e.update_xaxes(title='Date')
    return fig_321_e

# 8 | Callback and Function 6 - New Recovered ========
@app.callback(
    Output('my_graph6', 'figure'),
    [Input('country-picker', 'value')]
)

def update_graph6(country):
    c_df6 = the_df[the_df['location']==country]
    g_type6 = 'new_recovered'
    fig_321_f = px.bar(c_df6,
                       x='date',
                       y=g_type6,
                       hover_data={
                        'date':False,
                        g_type6:False,
                        'New Recovered':(':,', c_df6[g_type6])
                       })
    fig_321_f.data[-1].showlegend=True
    fig_321_f.data[-1].name = 'New Recovered'

    fig_321_f.update_traces(marker_color='lightgreen', marker_line_width = 0)
    fig_321_f.update_layout(hovermode = 'x unified', legend_title = 'Legend',
                            title={
                                'text': "New Recovered",
                                'y':0.95,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                            font=dict(
                                family="Arial",
                                color='white'
                                ),
                            plot_bgcolor = 'grey',
                            paper_bgcolor = 'grey',
                            legend = dict(orientation = 'h', x=0.8, y=-0.15)
                           )

    fig_321_f.add_shape(type='line',
                        xref='paper',
                        x0=0, x1=1,
                        y0=c_df6[g_type6].mean(),
                        y1=c_df6[g_type6].mean(),
                        line=dict(color='black'))

    fig_321_f.add_annotation(
        x = '2020-02-15',
        y = c_df6[g_type6].mean(),
        showarrow=True,
        text = 'Average: '+ str('{:,.0f}'.format(c_df6[g_type6].mean())),
        bgcolor='black'
    )

    fig_321_f.update_yaxes(title='Number of Cases', gridcolor='lightgrey')
    fig_321_f.update_xaxes(title='Date')
    return fig_321_f

# 9 | Callback and Function 7 - Active Cases ========
@app.callback(
    Output('my_graph7', 'figure'),
    [Input('country-picker', 'value')]
)

def update_graph7(country):
    c_df7 = the_df[the_df['location']==country]
    g_type7 = 'active_cases'
    fig_321_g = px.bar(c_df7,
                       x='date',
                       y=g_type7,
                       hover_data={
                        'date':False,
                        g_type7:False,
                        'Active Cases':(':,', c_df7[g_type7])
                       })
    fig_321_g.data[-1].showlegend=True
    fig_321_g.data[-1].name = 'Active Cases'

    fig_321_g.update_traces(marker_color='#ff9999', marker_line_width = 0)
    fig_321_g.update_layout(hovermode = 'x unified', legend_title = 'Legend',
                            title={
                                'text': "Active Cases",
                                'y':0.95,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                            font=dict(
                                family="Arial",
                                color='white'
                                ),
                            plot_bgcolor = 'grey',
                            paper_bgcolor = 'grey',
                            legend = dict(orientation = 'h', x=0.8, y=-0.15)
                           )

    fig_321_g.add_shape(type='line',
                        xref='paper',
                        x0=0, x1=1,
                        y0=c_df7[g_type7].mean(),
                        y1=c_df7[g_type7].mean(),
                        line=dict(color='black'))

    fig_321_g.add_annotation(
        x = '2020-02-15',
        y = c_df7[g_type7].mean(),
        showarrow=True,
        text = 'Average: '+ str('{:,.0f}'.format(c_df7[g_type7].mean())),
        bgcolor='black'
    )

    fig_321_g.update_yaxes(title='Number of Cases', gridcolor='lightgrey')
    fig_321_g.update_xaxes(title='Date')
    return fig_321_g

#==========================================

# Run Server
if __name__ == '__main__': #If this script is called, run the following:
    app.run_server(debug=True)
