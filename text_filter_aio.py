import uuid

from dash import html, Output, Input, State, dcc, ALL, clientside_callback

from .button_aio import ButtonAIO


class ids:
    apply_changes = lambda aio_id: {
        'component': 'TextFilterAIO',
        'subcomponent': 'apply_changes',
        'aio_id': aio_id
    }    
    input = lambda aio_id: {
        'component': 'TextFilterAIO',
        'subcomponent': 'input',
        'aio_id': aio_id
    }
    store = lambda aio_id: {
        'component': 'TextFilterAIO',
        'subcomponent': 'store',
        'aio_id': aio_id
    }


class TextFilterAIO(html.Div):
    ids = ids

    def __init__(
        self,
        reset_to_defaults_button_id=None,
        aio_id=None
    ):
        """
        This component serves to e.g. filter a table given the text that the user enters.
         
        Args:
            reset_to_defaults_button_id: The ID of a button that will reset this filter.
                A better design might be to pass to the reset button the IDs of the filters
                that it's supposed to reset, but let's say we decide to have it this way for
                some reason, for example the reset button does not know how to reset all fields.
            aio_id: AIO ID.
        """
        
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        super().__init__(
            [
                dcc.Input(id=ids.input(aio_id=aio_id)),
                ButtonAIO(
                    "Apply filters",
                    # Ideally, we'd do this: aio_id=ids.apply_changes(aio_id=aio_id)
                    # So, the "Apply filter" button would have the following ID:
                    # {
                    #     "component": "ButtonAIO",
                    #     "subcomponent": "button",
                    #     "aio_id": {
                    #         "component": "TextFilterAIO",
                    #         "subcomponent": "apply_changes",
                    #         "aio_id": <AIO ID of the current TextFilterAIO component>
                    #     }
                    # }
                    # Then we could write a callback with the following input:
                    # Input(ButtonAIO.ids.button(TextFilterAIO.ids.apply_changes(MATCH)), 'n_clicks')
                    #
                    # This is not possible (matching on nested IDs) right now, but one workaround
                    # is to 'extend in breadth' instead of depth and let the ID of "Apply filter" be:
                    # So, the "Apply filter" button would have the following ID:
                    # {
                    #     "component": "ButtonAIO",
                    #     "subcomponent": "button",
                    #     "aio_id": <AIO ID of the current TextFilterAIO component>,
                    #     "purpose": "apply_filters",
                    # }
                    # Now we can match:
                    # Input(
                    #     {
                    #         "component": "ButtonAIO",
                    #         "subcomponent": "button",
                    #         "aio_id": MATCH,
                    #         "purpose": "apply_filters",
                    #     },
                    #     "n_clicks"
                    # )
                    # A major drawback of this workaround is that the original AIO component's
                    # callbacks don't work now, since their callbacks do not have "apply_filters".
                    # We could leave out "purpose", but then we cannot have another ButtonAIO in this AIO.
                    #
                    # What we can do without major drawbacks (apart from performance) is to
                    # create a new UUID in this function (TextFilterAIO.__init__)
                    # and store the UUID in a store associated with this instance of TextFilterAIO.
                    # We would use this UUID as the aio_id of our "Apply filter" ButtonAIO.
                    # Our callback would then pattern-match all ButtonAIOs, however inside the function body
                    # we would compare the button's aio_id with the store's one, and only proceed if they are equal.
                    # I have not written the implementation here,
                    # but it would look similar to the solution that I wrote for the "Reset" button below.
                ),
                dcc.Store(id=ids.store(aio_id=aio_id), data=reset_to_defaults_button_id),
            ]
        )

# Within the super().__init__(...) call above, ideally we would add
# a client-side-callback-component (as in the old PR) that has the following input:
# Input(reset_to_defaults_button_id, "n_clicks")
#
# and the following output:
# Output(ids.input(aio_id=aio_id), "value")
#
# with the code:
# function(n_clicks) { if (n_clicks) return ""; return dash_clientside.no_update; }
#
# Right now, the way to accomplish this is to add a Store in TextFilterAIO,
# which contains just the string reset_to_defaults_button_id.
# Then, to add a client-side pattern matching callback which is triggered on clicking
# any button (ButtonAIO.button), and takes the Store as state.
# When the new callback executes, we compare the store's contents with the trigger.
# (The comparison is done within the function body, not on pattern-matching level.)
# If it's a match, we execute the desired code.
#
# This workaround is implemented below:

clientside_callback(
    """
    function reset_to_defaults(n_clicks, data) {
        const triggers = dash_clientside.callback_context.triggered;
        if (!triggers.length)
            throw dash_clientside.PreventUpdate;
            
        const trigger = JSON.parse(
            triggers[0].prop_id.replace(".n_clicks", "")
        );
        
        const states_list = dash_clientside.callback_context.states_list[0];
        
        return states_list.map(
            state => (
                state.value.component === trigger.component &&
                state.value.subcomponent === trigger.subcomponent &&
                state.value.aio_id === trigger.aio_id
            ) ? "" : dash_clientside.no_update
        ); 
    }
    
    """,
    Output(ids.input(ALL), 'value'),
    Input(ButtonAIO.ids.button(ALL), 'n_clicks'),
    State(ids.store(ALL), 'data'),
)