from shiny import App, ui

_SYSTEM_MSG = """
You are the guide of a 'choose your own adventure'- style game: a mystical
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
Crown of Quetzalcoatl:\n
<div style="display: grid; place-items: center;"><img src="https://i.imgur.com/Fxa7p1D.jpeg" width=60%/></div>\n
However, many challenges stand in your way. Are you brave enough, strong enough
and clever enough to overcome the perils of the jungle and secure the crown?

Before we begin our journey, choose your name, gender and race. Select from the
following weapons: A broadsword, a flintlock pistol or thowing daggers.

"""
# compose the messages log
_SYS = {"role": "system", "content": _SYSTEM_MSG}
stream = [_SYS]
stream.append({"role": "assistant", "content": WELCOME_MSG})

# Create a welcome message
welcome = ui.markdown(
    WELCOME_MSG
)

# ui: user interface
app_ui = ui.page_fillable(
    ui.panel_title("Choose Your Own Adventure: Amazon Adventure!"),

    ui.accordion(
    ui.accordion_panel("Step 1: Your OpenAI API Key",
        ui.input_text(id="key_input", label="Enter your openai api key"),
        ui.markdown("**Note:** The app does not store your key when the session ends."),
        ui.markdown("Using openai api costs money. Please monitor your account fees."),
    ), id="acc", multiple=False,
    ),
    ui.chat_ui("chat"),
    fillable_mobile=True,
)


# server: code logic
def server(input, output, session):
    chat = ui.Chat(id="chat", messages=[welcome])

    # Define a callback to run when the user submits a message
    @chat.on_user_submit
    async def _():
        # Get the user's input
        user = chat.user_input()
        #  update the stream list
        stream.append({"role": "user", "content": user})
        # Append a response to the chat
        model_response = f"You said: {user}"
        await chat.append_message(model_response)
        stream.append({"role": "assistant", "content": model_response})


app = App(app_ui, server)
