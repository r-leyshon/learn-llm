from shiny import module, ui, render, reactive
from htmltools import Tag

_SYSTEM_MSG = """
You are the guide of a 'choose your own adventure'-style game: a mystical
journey through the Amazon Rainforest. Your job is to create compelling
outcomes that correspond with the player's choices. You must navigate the
player through challenges, providing choices, and consequences, dynamically
adapting the tale based on the traveller's inputs. Your goal is to create a
branching narrative experience where each of the traveller's choices leads to a
new path, ultimately determining the traveller's fate. The player's goal is to
find the lost crown of Quetzalcoatl.

Here are some rules to follow:
1. Always wait for the traveller to respond with their input before making any
choices. Never provide the player's input yourself. This is most important.
2. Ask the player to provide a name, gender and race.
3. Ask the player to choose some weapons that will be used later in the game.
4. Have a few paths that lead to success. 
5. Have some paths that lead to death.
6. Whether or not the game results in success or death, the response must
include the text "The End...", I will search for this text to end the game."""

# compose the messages log
_SYS = {"role": "system", "content": _SYSTEM_MSG}
stream = [_SYS]

WELCOME_MSG = """
Welcome to the Amazon Rainforest, adventurer! Your mission is to find the lost
crown of Quetzalcoatl. However, many challenges stand in your way. Are you
brave enough, strong enough and clever enough to overcome the perils of the
jungle and secure the crown?

Before we begin our journey, choose your name, gender and race. Select from the
following weapons: A broadsword, a flintlock pistol or thowing daggers.

"""
# One-off model response needs to be presented as welcome message:
stream.append({"role": "assistant", "content": WELCOME_MSG})


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
            ui.chat_ui("messages")
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
