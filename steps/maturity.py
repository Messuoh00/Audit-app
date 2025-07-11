from nicegui import ui
from data import maturity_levels
from session_state import main_card, session, next_step, prev_step

def step_maturity():
    domains = sorted(set(q['Domain'] for q in session["questionnaire"] if q.get('Domain')))
    if not domains:
        next_step()
        return
    main_card.clear()
    with main_card:
        ui.label("Domain Maturity Self-Assessment").classes("text-xl font-semibold mb-2")
        ui.label("Rate your organization's maturity for each domain.").classes("mb-4")
        for dom in domains:
            ui.label(dom).classes("font-semibold")
            ui.radio(maturity_levels, value=session["domain_maturity"].get(dom, maturity_levels[0])).bind_value(session["domain_maturity"], dom).classes("mb-4")
        ui.button("Next", on_click=next_step).props('color=primary').classes("mr-2 mt-2")
        ui.button("Back", on_click=prev_step).props('color=secondary flat').classes("mt-2")
