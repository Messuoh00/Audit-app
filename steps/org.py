from nicegui import ui
from session_state import main_card, session, next_step, prev_step

def step_org():
    main_card.clear()
    with main_card:
        ui.label("Organization Info").classes("text-xl font-semibold mb-2")
        ui.input("Organization Name", value=session["org"]).bind_value(session, "org").classes("w-full mb-2").props('outlined')
        ui.input("Assessor Name", value=session["assessor"]).bind_value(session, "assessor").classes("w-full mb-2").props('outlined')
        ui.input("Assessment Date", value=session["date"]).bind_value(session, "date").props('type=date outlined')
        ui.button("Next", on_click=next_step).props('color=primary').classes("mt-3 mr-2")
        ui.button("Back", on_click=prev_step).props('color=secondary flat').classes("mt-3")
