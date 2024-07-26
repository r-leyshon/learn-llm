from shiny import module, ui, render, reactive
from htmltools import Tag

_SYSTEM_MSG = """SYSTEM PROMPT"""
# compose the messages log
_SYS = {"role": "system", "content": _SYSTEM_MSG}
stream = [_SYS]
model_resp = "PLACEHOLDER"


@module.ui
def chat_module_ui(input_label:str, button_label:str) -> Tag:
    """Provide UI structure for chat module.

    Provide a row tag with text input & action button wired into
    chat_module_server(). Provide text outputting messages stream wired into
    chat_module_server().

    Parameters
    ----------
    input_label : str
        String to display above text input.
    button_label : str
        String to display on action button.

    Returns
    -------
    Tag
        _description_
    """
    return ui.row(
        ui.card(
            ui.input_text_area(
                id="usr_input",
                label=input_label,
                spellcheck=True
            ),
        ui.input_action_button(id="update_messages", label=button_label),
        ),
        ui.card(
            ui.output_text("messages")
        ),
    )



@module.server
def chat_module_server(input, output, session):
    """Provides server logic for chat module.

    First argument expects a string giving the namespace for the chat module.
    """
    
    
    @render.text
    @reactive.event(input.update_messages)
    def messages() -> str:
        """Append user & model messages to the conversation stream."""
        stream.append({"role": "user", "content": input.usr_input()})
        stream.append({"role": "assistant", "content": response_placeholder()})
        return str(stream)


    def response_placeholder() -> str:
        """Provide some sample text in place of model."""
        return f"model response to ({input.usr_input()[0:5]})"
