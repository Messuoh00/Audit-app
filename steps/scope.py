from nicegui import ui
from data import all_standards, all_domains
from session_state import main_card, session, next_step, prev_step

def step_scope():
    main_card.clear()
    with main_card:
        ui.label("Select Scope").classes("text-xl font-semibold mb-2")
        ui.label("Choose the standards and domains relevant to your assessment.").classes("mb-3")
        ui.select(options=all_standards, label="Standards", multiple=True).bind_value(session, "standards").classes("mb-3")
        ui.select(options=all_domains, label="Domains (leave empty for all)", multiple=True).bind_value(session, "domains").classes("mb-3")
        ui.input("Optional keyword filter...", value=session["keyword"]).bind_value(session, "keyword").classes("mb-3")
        ui.button("Generate Questionnaire", on_click=next_step).props('color=primary').classes("mr-2")
        ui.button("Back", on_click=prev_step).props('color=secondary flat').classes("mt-2")
