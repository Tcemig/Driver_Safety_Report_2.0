def add_annotation(fig, x, y, text, textangle):
    fig.add_annotation(
        x=x, # 1.015,
        y=y, # 0.57,
        xref="paper",
        yref="paper",
        text=text, # "Coachable Behaviors",
        showarrow=False,
        font=dict(size=14, color='black'),
        textangle=textangle # -90
    )

    return fig