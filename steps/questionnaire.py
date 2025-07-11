from nicegui import ui
import os
from datetime import datetime
from data import controls_df, UPLOAD_DIR
from session_state import main_card, session, next_step, prev_step

def step_questionnaire():
    df = controls_df.copy()
    if session["standards"]:
        df = df[df["Standard"].isin(session["standards"])]
    if session["domains"]:
        df = df[df["Domain"].isin(session["domains"])]
    if session["keyword"]:
        mask = (
            df["Control Title"].str.contains(session["keyword"], case=False, na=False) |
            df["Control Description"].str.contains(session["keyword"], case=False, na=False)
        )
        df = df[mask]
    df_grouped = df.groupby(['Control Title', 'Control Description'], as_index=False).agg({
        'Control ID': 'first',
        'Domain': 'first',
        'Clause ID': 'first',
        'Standard': lambda x: ', '.join(sorted(set(x))),
        'Recommendation': 'first',
        'Comment': 'first'
    })
    df_grouped = df_grouped.rename(columns={'Standard': 'Standards'})
    session["questionnaire"] = df_grouped.to_dict("records")
    if not session["questionnaire"]:
        session["answers"] = []
        session["evidence"] = []
    else:
        session["answers"] = [{"answer": "No", "note": ""} for _ in session["questionnaire"]]
        session["evidence"] = [None for _ in session["questionnaire"]]

    main_card.clear()
    with main_card:
        ui.label("Assessment Questionnaire").classes("text-xl font-semibold mb-2")
        if not session["questionnaire"]:
            ui.label("No questions found with the selected filters.").classes("text-red")
        else:
            for i, q in enumerate(session["questionnaire"]):
                with ui.card().classes("mb-4 shadow-md"):
                    ui.label(f"{i+1}. {q['Control Title']}").classes("font-bold")
                    ui.label(q["Control Description"]).classes("mb-1")
                    ui.label(f"Domain: {q['Domain']} | Standards: {q['Standards']}").classes("text-xs text-blue-800")
                    def update_answer(e, idx=i):
                        session["answers"][idx]["answer"] = e.value
                    ui.radio(["Yes", "Partial", "No"],
                             value=session["answers"][i]["answer"],
                             on_change=update_answer).classes("mt-2 mb-2")
                    def update_note(e, idx=i):
                        session["answers"][idx]["note"] = e.value
                    ui.textarea("Notes (optional)", value=session["answers"][i]["note"], on_change=update_note).classes("mb-2")
                    # Evidence upload
                    def save_file(e, idx=i):
                        if e.files:
                            file = e.files[0]
                            dest = os.path.join(UPLOAD_DIR, f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.name}")
                            file.save(dest)
                            session["evidence"][idx] = dest
                            ui.notify(f"Uploaded evidence: {file.name}")
                    ui.upload(label="Upload Evidence", on_upload=save_file, auto_upload=True, max_files=1).classes("mb-2")
                    if session["evidence"][i]:
                        file_name = os.path.basename(session["evidence"][i])
                        ui.link(f"View evidence: {file_name}", f"/{session['evidence'][i]}", target="_blank").classes("text-blue-600 mb-1")
                    ui.label(f"Recommendation: {q['Recommendation']}").classes("text-sm text-gray-700")
                    ui.label(q["Comment"]).classes("text-sm text-gray-400")
        ui.button("Next", on_click=next_step).props('color=primary').classes("mr-2 mt-2")
        ui.button("Back", on_click=prev_step).props('color=secondary flat').classes("mt-2")
