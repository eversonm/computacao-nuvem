import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
def pĺot_graphs_front(dataframe = 'data', x='attr1', y='attr2', tipo='barra'):
    if tipo=="barra":
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=dataframe[x].value_counts().index,
            y=dataframe[x].value_counts(),
            name=x       # this sets its legend entry
        ))
        fig.update_layout(
            title="Gráfico de Barra ",
            xaxis_title=x,
            legend_title="Nome da linha",
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="Blue"
            )
        )
        return fig
    if tipo=="barrah":
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=dataframe[x].value_counts().sort_values(ascending=True),
            y=dataframe[x].value_counts().sort_values(ascending=True).index,
            orientation='h',
            name=x       # this sets its legend entry
        ))
        fig.update_layout(
            title="Gráfico de Barras Horizontal",
            xaxis_title=x,
            legend_title="Nome da linha",
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="Blue"
            )
        )
        return fig
    
    if tipo=="linha":
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dataframe[x].index,
            y=dataframe[x].value_counts(),
            name=x       # this sets its legend entry
        ))
        fig.update_layout(
            title="Gráfico de linha ",
            xaxis_title=x,
            legend_title="Nome da linha",
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="Blue"
            )
        )
        return fig
    if tipo=="histograma":
        fig = go.Figure()

        fig.add_trace(go.Histogram(
            x=dataframe[x],
            name=x       # this sets its legend entry
        ))
        fig.update_layout(
            title="Gráfico Histograma",
            xaxis_title=x,
            legend_title="Nome da linha",
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="Blue"
            )
        )
        return fig        
    if tipo=="boxplot":
        fig = go.Figure()

        fig.add_trace(go.Box(
            y=dataframe[x],
            boxpoints='all', 
            jitter=0.3, 
            pointpos=-1.8,
            name=y       # this sets its legend entry
        ))
        fig.update_layout(
            title="Gráfico BoxPlot com plot de Dispersão",
            xaxis_title=x,
            legend_title="Nome da linha",
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="Blue"
            )
        )
        return fig
    if tipo=="setores":
        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=dataframe[x].unique(),
            values=dataframe[x].value_counts(),
            name=x       # this sets its legend entry
        ))
        fig.update_layout(
            title="Gráfico de Pizza - "+x,
            xaxis_title=x,
            legend_title="Tipos",
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="Blue"
            )
        )
        return fig
    if tipo=="scatterplot":
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dataframe[x],
            y=dataframe[y],
            mode='markers'
        ))
        fig.update_layout(
            title="Gráfico de Dispersão",
            xaxis_title=x,
            yaxis_title=y,
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="Blue"
            )
        )
        return fig
    if tipo=="scattergeo":
        fig = go.Figure()

        fig.add_trace(go.Scattergeo(
            lat = dataframe[x],
            lon = dataframe[y],
            mode='markers'
        ))
        fig.update_layout(
            title="Gráfico de Dispersão Geolocalizado",
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="Blue"
            )
        )
        return fig
    if tipo=="linha-ano":
        data = pd.to_datetime(dataframe[x])
        dates = pd.DatetimeIndex(data).year
        line_chart_1 = dates.value_counts().sort_index()
    
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=line_chart_1.index, 
            y=line_chart_1.values,
            mode='lines+markers'
        ))
        fig.update_layout(
            title="Gráfico de Linha por Ano",
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="Blue"
            )
        )
        return fig

    if tipo=="linha-mes":
        data = pd.to_datetime(dataframe[x])
        dates = pd.DatetimeIndex(data).month
        line_chart_1 = dates.value_counts().sort_index()
    
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=line_chart_1.index, 
            y=line_chart_1.values,
            mode='lines+markers'
        ))
        fig.update_layout(
            title="Gráfico de Linha por Mês",
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="Blue"
            )
        )
        return fig
    if tipo=="linha-semana":
        data = pd.to_datetime(dataframe[x])
        dates = pd.DatetimeIndex(data).dayofweek
        line_chart_1 = dates.value_counts().sort_index()
    
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=line_chart_1.index, 
            y=line_chart_1.values,
            mode='lines+markers'
        ))
        fig.update_layout(
            title="Gráfico de Linha por Dias da Semana (Segunda=0, Domingo=6)",
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="Blue"
            )
        )
        return fig
    if tipo=="linha-combinado":
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dataframe[x].index,
            y=dataframe[x].value_counts(),
            name=x       # this sets its legend entry
        ))


        fig.add_trace(go.Scatter(
            x=dataframe[x].index,
            y=dataframe[y].value_counts(),
            name=y
        ))

        fig.update_layout(
            title="Gráfico de linha Combinado",
            legend_title="Nome da linha",
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="Blue"
            )
        )
        return fig
