from nicegui import ui
import os
import pandas as pd
from session_state import main_card, session, next_step, prev_step

def step_review():
    if not session["questionnaire"] or not session["answers"]:
        next_step()
        return
    df = pd.DataFrame([
        {**q, "Answer": a["answer"], "Note": a["note"], "Evidence": os.path.basename(ev) if ev else ""}
        for q, a, ev in zip(session["questionnaire"], session["answers"], session["evidence"])
    ])
    score = df["Answer"].map({"Yes": 2, "Partial": 1, "No": 0}).sum()
    max_score = len(df) * 2
    percent = round(100 * score / max_score, 1) if max_score > 0 else 0
    maturity = (
        "Mature" if percent >= 67 else
        "Developing" if percent >= 34 else
        "Initial"
    )
    main_card.clear()
    with main_card:
        ui.label("Review Assessment").classes("text-xl font-semibold mb-2")
        ui.label(f"Compliance Score: {score}/{max_score} ({percent}%) | Maturity: {maturity}").classes("text-blue-700 mb-3")
        ui.table.from_pandas(df[["Control Title", "Domain", "Standards", "Answer", "Note", "Evidence"]]).classes("mb-2")
        ui.button("Submit & See Results", on_click=next_step).props('color=red').classes("mr-2 mt-2")
        ui.button("Back", on_click=prev_step).props('color=secondary flat').classes("mt-2")
