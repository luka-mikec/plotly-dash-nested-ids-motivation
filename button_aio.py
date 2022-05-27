import uuid

from dash import html, Output, MATCH, Input, clientside_callback


class ids:
    button = lambda aio_id: {
        'component': 'ButtonAIO',
        'subcomponent': 'button',
        'aio_id': aio_id
    }


class ButtonAIO(html.Button):
    ids = ids

    def __init__(
        self,
        children="Click me!",
        aio_id=None
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        super().__init__(
            children,
            ids.button(aio_id=aio_id),
            n_clicks=1,
        )


clientside_callback(
    """
    function change_colour(n_clicks) {
        return {
            background: (n_clicks || 0) % 2 ? "#aa5555" : "#55aa55"
        };
    }
    """,
    Output(ids.button(MATCH), 'style'),
    Input(ids.button(MATCH), 'n_clicks'),
)