from dash import Dash, html

from .button_aio import ButtonAIO
from .text_filter_aio import TextFilterAIO

app = Dash(suppress_callback_exceptions=True)
app.layout = html.Div(
    [
        TextFilterAIO(
            reset_to_defaults_button_id=ButtonAIO.ids.button(aio_id="reset_button_1"),
        ),
        ButtonAIO(
            "Reset 1",
            aio_id="reset_button_1",
        ),
        TextFilterAIO(
            reset_to_defaults_button_id=ButtonAIO.ids.button(aio_id="reset_button_2"),
        ),
        ButtonAIO(
            "Reset 2",
            aio_id="reset_button_2",
        )
    ]
)

if __name__ == "__main__":
    app.server.run("0.0.0.0", 5000)
