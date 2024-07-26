from shiny import App, render, ui, reactive
from modules import chat_module_ui, chat_module_server


SYSTEM_MSG = """SYSTEM PROMPT"""
# compose the messages log
stream = [{"role": "system", "content": SYSTEM_MSG}]

# UI-----------------------------------------------
app_ui = ui.page_fluid(
    ui.row(
        ui.input_text(id="key_prompt", label="Paste openai api key here."),
        ui.p(ui.HTML("<strong>Note:</strong> This app does not store your key after the session ends.")),
        ),
    chat_module_ui(
        "chat_namespace",
        input_label="Type something",
        button_label="Send message"
        )
    )

# SERVER-----------------------------------------------


def server(input, output, session):
    chat_module_server("chat_namespace")

app = App(app_ui, server)
