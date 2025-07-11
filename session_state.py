from datetime import datetime
from data import all_standards
from nicegui import ui

# Place main_card here for global access
main_card = ui.card().style("max-width:1400px; margin:auto; padding:48px;")

session = {
    "step": 0,
    "org": "",
    "assessor": "",
    "date": datetime.today().strftime('%Y-%m-%d'),
    "standards": list(all_standards),
    "domains": [],
    "keyword": "",
    "questionnaire": [],
    "answers": [],
    "evidence": [],
    "domain_maturity": {},
}

def reset_session():
    session.update({
        "step": 0,
        "org": "",
        "assessor": "",
        "date": datetime.today().strftime('%Y-%m-%d'),
        "standards": list(all_standards),
        "domains": [],
        "keyword": "",
        "questionnaire": [],
        "answers": [],
        "evidence": [],
        "domain_maturity": {},
    })

def next_step():
    session["step"] += 1
    refresh()
def prev_step():
    session["step"] = max(0, session["step"] - 1)
    refresh()
def to_step(n):
    session["step"] = n
    refresh()

from steps.welcome import step_welcome
from steps.org import step_org
from steps.scope import step_scope
from steps.questionnaire import step_questionnaire
from steps.maturity import step_maturity
from steps.review import step_review
from steps.results import step_results

steps = [
    step_welcome,
    step_org,
    step_scope,
    step_questionnaire,
    step_maturity,
    step_review,
    step_results,
]

def refresh():
    steps[session["step"]]()
