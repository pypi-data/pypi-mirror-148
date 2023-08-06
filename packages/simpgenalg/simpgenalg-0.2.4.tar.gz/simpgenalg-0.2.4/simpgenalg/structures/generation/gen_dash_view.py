# -*- coding: utf-8 -*-
from dash import Dash, dcc, html, dash_table, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import scipy.stats
import random
import math

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Stores information
dfs = {'indvs':None, 'stats':None}
cols = {'indvs':None, 'stats':None, 'uniq_stats':None}


class generationViewer():

    def __init__(self, indvs=None, stats=None, rslts=None, debug=False, **kargs):

        if indvs is None and stats is None and rslts is None:
            raise ValueError('Need to pass idnvs, stats, or rslts')

        def load(input):
            if isinstance(input, str):
                df = pd.read_csv(input)
            elif isinstance(input, dict):
                df = pd.DataFrame(input)
            elif isinstance(input, pd.DataFrame):
                df = input
            df = df.select_dtypes(include=\
                ('int16','int32','int64','boolean',\
                 'float16','float32','float64'))
            return df

        # Interpret results
        if rslts is not None:
            print("Loading Results")
            indvs, stats = rslts.to_df()
            dfs['indvs'] = indvs
            cols['indvs'] = sorted(list(indvs.columns))
            dfs['stats'] = stats
            cols['stats'] = sorted([col for col in stats.columns \
                                        if '.95CI' not in col])
            cols['uniq_stats'] = sorted(list({col if '.' not in col \
                                        else ''.join(col.split('.')[:-1]) \
                                        for col in cols['stats']}))
        else:
            if indvs is not None:
                print("Loading Individuals")
                indvs = load(indvs)
                dfs['indvs'] = indvs
                cols['indvs'] = sorted(list(indvs.columns))
            if stats is not None:
                print("Loading Population Stats")
                stats = load(stats)
                dfs['stats'] = stats
                cols['stats'] = sorted([col for col in stats.columns \
                                            if '.95CI' not in col])
                cols['uniq_stats'] = sorted(list({col if '.' not in col \
                                            else ''.join(col.split('.')[:-1]) \
                                            for col in cols['stats']}))

        # Raise an error if min/max don't match
        if indvs is not None and stats is not None:
            gen_min, gen_max = stats['_gen'].min(), stats['_gen'].max()
            run_min, run_max = stats['_run'].min(), stats['_run'].max()

            if gen_min != indvs['_gen'].min():
                raise ValueError
            if gen_max != indvs['_gen'].max():
                raise ValueError
            if run_min != indvs['_run'].min():
                raise ValueError
            if run_max != indvs['_run'].max():
                raise ValueError

        print("Loading Dash Board")

        app.layout = html.Div([
            dcc.Tabs([
                dcc.Tab(label='Individual Info', children=[
                    html.Label('Run'),
                    dcc.RangeSlider(run_min, run_max, 1, value=[run_max, run_max],\
                                    id='indvs-run-slider', tooltip={"placement": "bottom",\
                                    "always_visible": True}),
                    html.Label('Generation'),
                    dcc.RangeSlider(gen_min, gen_max, value=[gen_max, gen_max],\
                                    id='indvs-gen-slider', tooltip={"placement": "bottom",\
                                    "always_visible": True}),
                    dcc.Graph(id='indvs-graph'),
                    html.Div(children=[
                        html.Label('X-Axis'),
                        dcc.Dropdown(cols['indvs'],\
                                        None,\
                                        id='indvs-x-axis-selector'),

                        html.Br(),
                        html.Label('Y-Axis'),
                        dcc.Dropdown(cols['indvs'],
                                     None,
                                     multi=True,\
                                     id='indvs-y-axis-selector'),

                        html.Br(),
                        html.Label('Color', id='indvs-color-selector-lbl'),
                        dcc.Dropdown(cols['indvs'],
                                     None,\
                                     id='indvs-color-selector'),
                        html.Br(),
                        html.Label('Size', id='indvs-size-selector-lbl'),
                        dcc.Dropdown(cols['indvs'],
                                     None,\
                                     id='indvs-size-selector'),
                        html.Br(),
                        html.Label('Graph Type'),
                        dcc.Dropdown(['Bar', 'Line', 'Scatter'], 'Scatter',\
                                            id='indvs-graph-type-selector'),


                    ], style={'padding': 10, 'flex-direction': 'row'}),

                    html.Br(),
                    dcc.Tabs([
                        dcc.Tab(label='variables', children=[
                            html.Div(children=\
                                [html.Label('variables')]+\
                                [html.Label(col) for col in cols['indvs']],\
                            style={'padding': 10, 'flex-direction': 'row'}),
                        ]),
                        dcc.Tab(label='Table', children=[
                            html.Div(children=[\
                                html.Label('Future table maybe'),
                            ],\
                            style={'padding': 10, 'flex-direction': 'row'}),
                        ]),
                    ]),

                ]),
                dcc.Tab(label='Population Statistics', children=[
                    html.Label('Run'),
                    dcc.RangeSlider(run_min, run_max, 1, value=[run_max, run_max],\
                                    id='stats-run-slider', tooltip={"placement": "bottom",\
                                    "always_visible": True}),
                    html.Label('Generation'),
                    dcc.RangeSlider(gen_min, gen_max, value=[gen_max, gen_max],\
                                    id='stats-gen-slider', tooltip={"placement": "bottom",\
                                    "always_visible": True}),
                    dcc.Graph(id='stats-graph'),
                    html.Div(children=[
                        html.Label('X-Axis'),
                        dcc.Dropdown(cols['stats'],\
                                        None,\
                                        id='stats-x-axis-selector'),

                        html.Br(),
                        html.Label('Y-Axis'),
                        dcc.Dropdown(cols['stats'],
                                     None,
                                     multi=True,\
                                     id='stats-y-axis-selector'),

                        html.Br(),
                        html.Label('Color', id='stats-color-selector-lbl'),
                        dcc.Dropdown(cols['stats'],
                                     None,\
                                     id='stats-color-selector'),

                        html.Br(),
                        html.Label('Size', id='stats-size-selector-lbl'),
                        dcc.Dropdown(cols['stats'],
                                     None,\
                                     id='stats-size-selector'),

                        html.Br(),
                        html.Label('Graph Type'),
                        dcc.Dropdown(['Bar', 'Line', 'Scatter', ''], 'Line',\
                                            id='stats-graph-type-selector'),

                        html.Br(),
                        dcc.Tabs([
                            dcc.Tab(label='Variables', children=[
                                html.Div(children=\
                                    [html.Label('Variables')]+\
                                    [html.Label(col) for col in cols['uniq_stats']],\
                                style={'padding': 10, 'flex-direction': 'row'}),
                            ]),
                        ]),
                    ], style={'padding': 10, 'flex-direction': 'row'})
                ]),
            ]),
        ])

        app.run_server(debug=debug,\
                       port=kargs.get('port', 8001),)

# Hides colors / size if not scatterplot / bar
@app.callback(
    Output('stats-size-selector', 'style'),
    Output('stats-size-selector-lbl', 'style'),
    Output('stats-color-selector', 'style'),
    Output('stats-color-selector-lbl', 'style'),
    Input('stats-graph-type-selector', 'value'),
    Input('stats-y-axis-selector', 'value')
)
def hide_or_show_clr_size_stats(graph_type, y_vals):
    if y_vals is not None and isinstance(y_vals, (list,tuple)) and len(y_vals) > 1:
        if graph_type == 'Scatter':
            return {'display': 'block'}, {'display': 'block'}, \
                                {'display': 'none'}, {'display': 'none'}
        return {'display': 'none'}, {'display': 'none'}, \
                            {'display': 'none'}, {'display': 'none'}
    elif graph_type == 'Scatter':
        return {'display': 'block'}, {'display': 'block'}, \
                            {'display': 'block'}, {'display': 'block'}
    elif graph_type == 'Bar':
        return {'display': 'none'}, {'display': 'none'}, \
                            {'display': 'block'}, {'display': 'block'}
    elif graph_type == 'Line':
        return {'display': 'none'}, {'display': 'none'}, \
                            {'display': 'block'}, {'display': 'block'}

# Hides colors / size if not scatterplot / bar
@app.callback(
    Output('indvs-size-selector', 'style'),
    Output('indvs-size-selector-lbl', 'style'),
    Output('indvs-color-selector', 'style'),
    Output('indvs-color-selector-lbl', 'style'),
    Input('indvs-y-axis-selector', 'value'),
    Input('indvs-graph-type-selector', 'value'),
)
def hide_or_show_clr_size_indvs(y_vals, graph_type):
    print('Called hide_or_show_clr_size_indvs')
    if y_vals is not None and isinstance(y_vals, (list,tuple)) and len(y_vals) > 1:
        if graph_type == 'Scatter':
            return {'display': 'block'}, {'display': 'block'}, \
                                {'display': 'none'}, {'display': 'none'}
        return {'display': 'none'}, {'display': 'none'}, \
                            {'display': 'none'}, {'display': 'none'}
    else:
        return {'display': 'block'}, {'display': 'block'}, \
                            {'display': 'block'}, {'display': 'block'}

def get_mean_and_CI(df, x, y):
    stats = df.groupby(x)[y].agg(['mean', 'count', 'std'])
    ci = [1.96*(row['std']/row['count']) \
                for index, row in stats.iterrows()]
    return stats.index.tolist(), stats['mean'].tolist(), ci

def _filter_by_runs_and_gens(df, run, gen):
    print('Called _filter_by_runs_and_gens')
    filtered_df = df[df._run >= run[0]]
    filtered_df = filtered_df[filtered_df._run <= run[1]]
    filtered_df = filtered_df[filtered_df._gen >= gen[0]]
    filtered_df = filtered_df[filtered_df._gen <= gen[1]]
    return filtered_df

def _create_line_graph(df, x, y, clr):
    print('Called _create_line_graph')

    fig = go.Figure()
    if len(y) == 1 and clr is not None:
        groups = df.groupby(clr)
        for name in groups.groups.keys():
            c1, c2, c3 = random.randint(0,255),\
                         random.randint(0,255),\
                         random.randint(0,255)
            x_vals, means, ci = get_mean_and_CI(groups.get_group(name), x, y[0])
            fig.add_trace(go.Scatter(x=x_vals, \
                                     y=means,\
                                     mode='lines', \
                                     name=name,\
                                     line_color=f'rgba({c1},{c2},{c3},1)',\
                                     showlegend=True,\
                                     error_y=dict(
                                            type='data',
                                            array=ci,
                                            visible=True)))
        return fig
    else:
        # Group by x-axis
        for y_indx, y_header in enumerate(y):
            c1, c2, c3 = random.randint(0,255),\
                         random.randint(0,255),\
                         random.randint(0,255)

            x_vals, means, ci = get_mean_and_CI(df, x, y_header)
            fig.add_trace(go.Scatter(x=x_vals, \
                                     y=means,\
                                     mode='lines', \
                                     name=y_header,\
                                     line_color=f'rgba({c1},{c2},{c3},1)',\
                                     showlegend=True,\
                                     error_y=dict(
                                            type='data',
                                            array=ci,
                                            visible=True)))
        return fig

def _create_scatter_plot(df, x, y, clr, size):
    print('Called _create_scatter_plot')
    if len(y) == 1:
        if clr is None and size is None:
            return px.scatter(df, x=x, y=y[0])
        elif clr is not None and size is not None:
            return px.scatter(df, x=x, y=y[0], color=clr, size=size)
        elif size is not None:
            return px.scatter(df, x=x, y=y[0], size=size)
        elif clr is not None:
            return px.scatter(df, x=x, y=y[0], color=clr)
    else:
        fig = go.Figure()
        for y_val in y:
            c1,c2,c3 = random.randint(0,255), \
                       random.randint(0,255), \
                       random.randint(0,255)
            if size is None:
                fig.add_trace(go.Scatter(x=df[x], \
                                         y=df[y_val],\
                                         mode='markers', \
                                         name=y_val,\
                                         line_color=f'rgba({c1},{c2},{c3},1)',\
                                         showlegend=True))
            else:
                df_size = df[size]
                print('x',df_size)
                if len(df_size) == 1:
                    df_size = [20]
                else:
                    df_size = ((df_size-df_size.min())/(df_size.max()-df_size.min()))*20
                print('xx',df_size)
                fig.add_trace(go.Scatter(x=df[x], \
                                         y=df[y_val],\
                                         mode='markers', \
                                         name=y_val,\
                                         line_color=f'rgba({c1},{c2},{c3},1)',\
                                         showlegend=True,\
                                         marker_size=df_size))
        return fig

def _create_bar_chart(df, x, y, clr):
    print('Called _create_bar_chart')

    fig = go.Figure()
    if len(y) == 1 and clr is not None:
        groups = df.groupby(clr)
        for name in groups.groups.keys():
            x_vals, means, ci = get_mean_and_CI(groups.get_group(name), x, y[0])
            fig.add_trace(go.Bar(x=x_vals, \
                                 y=means,\
                                 name=name,\
                                 showlegend=True,\
                                 error_y=dict(
                                        type='data',
                                        array=ci,
                                        visible=True)))
        return fig
    else:
        # Group by x-axis
        for y_indx, y_header in enumerate(y):
            x_vals, means, ci = get_mean_and_CI(df, x, y_header)
            fig.add_trace(go.Bar(x=x_vals, \
                                 y=means,\
                                 name=y_header,\
                                 showlegend=True,\
                                 error_y=dict(
                                        type='data',
                                        array=ci,
                                        visible=True)))
        return fig

@app.callback(
    Output('stats-graph', 'figure'),
    Input('stats-run-slider', 'value'),
    Input('stats-gen-slider', 'value'),
    Input('stats-x-axis-selector', 'value'),
    Input('stats-y-axis-selector', 'value'),
    Input('stats-color-selector', 'value'),
    Input('stats-size-selector', 'value'),
    Input('stats-graph-type-selector','value'))
def update_stats_fig(run, gen, x, y, clr, size, graph_type):
    print('Called update_stats_fig')

    # If missing any of essential values, just return
    if y == None or None in y or len(y) == 0 or x is None or graph_type is None:
        fig = go.Figure()
        fig.update_layout(legend_title_text = "Legend")
        fig.update_xaxes(title_text='')
        fig.update_layout(transition_duration=500)
        y_axis_name = y[0] if (y is not None and len(y) == 1) else 'y-axis'
        fig.update_layout(title = "Empty Plot",\
                          xaxis_title = x if x is not None else 'x-axis',\
                          yaxis_title = y_axis_name,\
                          legend_title = 'Legend')
        return fig

    # Get only values in run/gen range
    df = _filter_by_runs_and_gens(dfs['stats'], run, gen)

    # Sort by X-Axis
    df.sort_values(by=x)

    # Create the apropriate graph
    if graph_type == 'Line':
        fig = _create_line_graph(df, x, y, clr)
    elif graph_type == 'Scatter':
        fig = _create_scatter_plot(df, x, y, clr, size)
    elif graph_type == 'Bar':
        fig = _create_bar_chart(df, x, y, clr)

    y_axis_name = y[0] if len(y) == 1 else 'y-axis'

    fig.update_layout(legend_title_text = "Legend")
    fig.update_xaxes(title_text='')
    fig.update_layout(transition_duration=500)
    fig.update_layout(title = f"{y} over {x}",\
                      xaxis_title = x if x is not None else 'x-axis',\
                      yaxis_title = y_axis_name,\
                      legend_title = 'Legend')

    return fig


@app.callback(
    Output('indvs-graph', 'figure'),
    Input('indvs-run-slider', 'value'),
    Input('indvs-gen-slider', 'value'),
    Input('indvs-x-axis-selector', 'value'),
    Input('indvs-y-axis-selector', 'value'),
    Input('indvs-color-selector', 'value'),
    Input('indvs-size-selector', 'value'),
    Input('indvs-graph-type-selector', 'value'))
def update_indvs_fig(run, gen, x, y, clr, size, graph_type):
    print('Called update_indvs_fig')

    # If missing any of essential values, just return
    if y == None or None in y or len(y) == 0 or x is None or graph_type is None:
        fig = go.Figure()
        fig.update_layout(legend_title_text = "Legend")
        fig.update_xaxes(title_text='')
        fig.update_layout(transition_duration=500)
        y_axis_name = y[0] if (y is not None and len(y) == 1) else 'y-axis'
        fig.update_layout(title = "Empty Plot",\
                          xaxis_title = x if x is not None else 'x-axis',\
                          yaxis_title = y_axis_name,\
                          legend_title = 'Legend')
        return fig

    # Get only values in run/gen range
    df = _filter_by_runs_and_gens(dfs['indvs'], run, gen)

    # Sort by X-Axis
    df.sort_values(by=x)

    # Create the apropriate graph
    if graph_type == 'Line':
        fig = _create_line_graph(df, x, y, clr)
    elif graph_type == 'Scatter':
        fig = _create_scatter_plot(df, x, y, clr, size)
    elif graph_type == 'Bar':
        fig = _create_bar_chart(df, x, y, clr)

    y_axis_name = y[0] if len(y) == 1 else 'y-axis'

    fig.update_layout(legend_title_text = "Legend")
    fig.update_xaxes(title_text='')
    fig.update_layout(transition_duration=500)
    fig.update_layout(title = f"{y} over {x}",\
                      xaxis_title = x if x is not None else 'x-axis',\
                      yaxis_title = y_axis_name,\
                      legend_title = 'Legend')

    return fig


if __name__ == '__main__':
    #app.run_server(debug=True)
    generationViewer(indvs='indvs.csv', stats='popstats.csv', debug=False)
