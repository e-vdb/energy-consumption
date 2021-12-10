import plotly.graph_objects as go

def setup_bar_chart(df, x_col, y_cols, title):
    bar = [go.Bar(x=df[x_col], y=df[col], name=col) for col in y_cols]
    fig = go.Figure(bar)
    fig.update_layout(
        title=title,
        xaxis_title="Months",
        yaxis_title="Consumption",
        legend_title="Legend",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="White"
        )
    )
    return fig