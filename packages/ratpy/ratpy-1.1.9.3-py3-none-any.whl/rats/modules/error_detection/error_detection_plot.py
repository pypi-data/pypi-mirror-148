import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
pd.options.mode.chained_assignment = None


def error_detection_plot(df, decimate=True):

    def assign_erroneous_edbs(df):
        # Function for use in a pandas .apply() method to a pandas groupby object
        errors = ' '.join(df[df['state'] == 'ERROR']['ACTIVE_EDBS'].astype(str).to_list())
        df['EDBs in error'] = errors
        return (df)

    title = df.board.unique()[0]
    df = df[['FUNCTION', 'PACKET_COUNT', 'LLC_COUNT',
             'ACTIVE_EDBS', 'anomalous']]

    df.drop_duplicates(subset=['LLC_COUNT', 'ACTIVE_EDBS', 'anomalous'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['state'] = np.where(df['anomalous'] == 0, 'OK', 'ERROR')

    if decimate:

        def decimate_bp_plot(df):
            if 'ERROR' in df['state'].values:
                return df
            else:
                first = df.drop_duplicates(subset='FUNCTION', keep='first')
                last = df.drop_duplicates(subset='FUNCTION', keep='last')
                return pd.concat([first, last])

        df = df.groupby('state').apply(decimate_bp_plot)
        df['FUNCTION'] = df['FUNCTION'].astype('category')

        df = df.groupby('LLC_COUNT').apply(assign_erroneous_edbs)

        traces = []
        legend = True
        for function in df['FUNCTION'].unique().to_list():
            trace_df = df[df['FUNCTION'] == function]
            traces.append(
                go.Scatter(x=trace_df[trace_df['state']=='OK']['LLC_COUNT'],
                           y=trace_df[trace_df['state'] == 'OK']['FUNCTION'],
                           hovertemplate='LLC: %{x} <br> Function: %{y}',
                           legendgroup=1,
                           name='OK',
                           line_color='blue',
                           marker_color='blue',
                           showlegend=legend)
            )
            if trace_df[trace_df['state'] == 'ERROR']['LLC_COUNT'].shape[0] > 0:
                traces.append(
                    go.Scatter(x=trace_df[trace_df['state'] == 'ERROR']['LLC_COUNT'],
                               y=trace_df[trace_df['state'] == 'ERROR']['FUNCTION'],
                               customdata=trace_df[trace_df['state'] == 'ERROR']['EDBs in error'],
                               legendgroup=2,
                               hovertemplate="LLC: %{x} <br> Function: %{y} <br> EDBs in error: %{customdata}",
                               name='ERROR',
                               mode='markers',
                               marker_color='red',
                               showlegend=legend)
                )
            legend=False

        fig = go.Figure()
        fig.add_traces(traces)

    else:
        df['EDBs in error'] = np.where(df['state'] == 'ERROR', df['ACTIVE_EDBS'], 'NA')
        df = df.groupby('LLC_COUNT').apply(assign_erroneous_edbs)
        fig = px.scatter(df, x='LLC_COUNT', y='FUNCTION', color='state',
                         hover_data=['LLC_COUNT', 'EDBs in error'],
                         title=title, render_mode='webgl', template='simple_white')
        errors = df[df['state'] == 'ERROR']

        if len(errors) > 0:
            fig.data[0].mode = 'markers'
            fig.data[1].mode = 'markers'
            fig.data[1].marker.color = 'red'
            fig.data[0].marker.color = 'blue'

    fig.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      modebar=dict(bgcolor='rgba(0,0,0,0)', color='grey', activecolor='lightgrey'),
                      template='simple_white')
    fig.update_traces(marker=dict(size=12))
    fig.update_xaxes(showgrid=True, title='LLC Trigger Count')
    fig.update_yaxes(showgrid=True, title='Function Number')

    return fig

