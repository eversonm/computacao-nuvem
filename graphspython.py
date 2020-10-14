import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
def pĺot_graphs_front(dataframe = 'data', x='attr1', y='attr2', tipo='barra'):
	if tipo=="barra":
		fig = go.Figure()
		fig.add_trace(go.Bar(x=dataframe[x].value_counts().index, y=dataframe[x].value_counts()))
		return fig
	if tipo=="barrah":
		return go.Figure([go.Bar(y=dataframe[x].value_counts().sort_values(ascending=True).index, x=dataframe[x].value_counts().sort_values(ascending=True), width=0.6,orientation='h')])
	if tipo=="linha":
		return go.Figure([go.Scatter(x=dataframe[x].value_counts().index, y=dataframe[x].value_counts())])
	if tipo=="histograma":
		return go.Figure(data=[go.Histogram(x=dataframe[x])])
	if tipo=="boxplot":
		return go.Figure(data=[go.Box(y=dataframe[x], boxpoints='all', jitter=0.3, pointpos=-1.8)])
	if tipo=="setores":
		return go.Figure(data=[go.Pie(labels=dataframe[x].unique(), values=dataframe[x].value_counts())])
	if tipo=="scatterplot":
		return go.Figure(data=go.Scatter(x=dataframe[x], y=dataframe[y], mode='markers'))
	if tipo=="scattergeo":
		return go.Figure(data=[go.Scattergeo(lon = dataframe[y], lat = dataframe[x], mode = 'markers')])
	if tipo=="linha-ano":
		dates = pd.DatetimeIndex(dataframe[x]).year
		line_chart_1 = dates.value_counts().sort_index()
		try:
			fig = go.Figure([(go.Scatter(x=line_chart_1.index, y=line_chart_1.values,
		                mode='lines+markers',
		                name='Ameaças Adicionadas'))])
		except:
			fig = go.Figure([go.Scatter(x=dataframe[x].value_counts().index, y=dataframe[x].value_counts())])
		return fig

	if tipo=="linha-mes":
		dates = pd.DatetimeIndex(dataframe[x]).month
		line_chart_1 = dates.value_counts().sort_index()
		try:
			fig = go.Figure([(go.Scatter(x=line_chart_1.index, y=line_chart_1.values,
		                mode='lines+markers',
		                name='Ameaças Adicionadas'))])
		except:
			fig = go.Figure([go.Scatter(x=dataframe[x].value_counts().index, y=dataframe[x].value_counts())])
		return fig
