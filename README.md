Some motivating examples for:
 - allowing nested dictionaries as component IDs,
 - allowing creation of client-side callbacks after the server already started.

In this example there is a component called `TextFilterAIO` which wraps an HTML input field and also provides an "Apply filter" button. This button is an instance of another AIO component in this example, `ButtonAIO`, which wraps an HTML button, and makes it change its colour on click.

The idea is that every `TextFilterAIO` instance has its own "Apply filter" button. We need a callback that executes when the user presses that button.

In addition to that, there can be one or more "Reset" buttons. Unlike the "Apply filter" button, one "Reset" button instance can correspond to many `TextFilterAIO` instances (this is not actually shown in this example though, but that's the idea).

All this can be solved in one way or another even right now. One solution (for the "Reset" button, and for the "Apply filter" button it would be similar) is included in the code, but it's a bit hard to reason about. 

With nested dictionaries as IDs, we could easily match a `TextFilterAIO` instance with its "Apply filter" button (the "Apply filter" button's AIO ID would be the full ID of the `TextFilterAIO` instance, which is itself a dictionary).

With on-the-fly client-side callbacks we could generate a callback triggered by the reset button ID (specified in the constructor of the `TextFilterAIO` instance) that would clear the `TextFilterAIO` instance's value.
