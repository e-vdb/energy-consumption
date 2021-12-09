import plotly.graph_objects as go

def setup_bar_chart(df, x_col, y_cols):
    bar = [go.Bar(x=df[x_col], y=df[col]) for col in y_cols]
    fig = go.Figure(bar)
    return fig