from nicegui import ui
from session_state import main_card, next_step

def step_welcome():
    main_card.clear()
    with main_card:
        ui.label("🛡️ Cybersecurity Assessment").classes("text-2xl mb-2 font-bold")
        ui.label("Assess your organization's cybersecurity compliance across multiple standards.").classes("mb-4")
        ui.button("Start Assessment", on_click=next_step).props('color=primary size=lg')
