from shiny import App, render, ui, reactive


SYSTEM_MSG = """SYSTEM PROMPT"""
# compose the messages log
stream = [{"role": "system", "content": SYSTEM_MSG}]

# UI-----------------------------------------------
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_text_area(
            id="usr_input", label="Type your response", spellcheck=True
            ),
        ui.input_action_button(id="update_messages", label="Click to send"),
    ),
    ui.output_text("messages"),
    )

# SERVER-----------------------------------------------


def server(input, output, session):


    @render.text
    @reactive.event(input.update_messages)
    def messages():
        stream.append({"role": "user", "content": input.usr_input()})
        stream.append({"role": "assistant", "content": response_placeholder()})
        return str(stream)


    @reactive.event(input.update_messages)
    def response_placeholder():
        return f"model response to ({input.usr_input()[0:5]})"

app = App(app_ui, server)
