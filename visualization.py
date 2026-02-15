import plotly.graph_objects as go

def radar_chart(scores):

    categories = list(scores.keys())
    values = list(scores.values())

    # Close the loop
    values += values[:1]
    categories += categories[:1]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False
    )

    return fig
