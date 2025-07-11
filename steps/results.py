from nicegui import ui
import os
import pandas as pd
import plotly.express as px
from pdf_export import export_pdf
from session_state import main_card, session, reset_session, to_step,refresh


def step_results():
    if not session["questionnaire"] or not session["answers"]:
        to_step(2)
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
    by_domain = df.groupby("Domain")["Answer"].apply(lambda x: (x == "Yes").sum() / len(x) * 100 if len(x) > 0 else 0)
    by_standard = df.copy()
    standards_list = []
    for _, row in by_standard.iterrows():
        for s in row["Standards"].split(","):
            standards_list.append({"Standard": s.strip(), "Answer": row["Answer"]})
    df_standards = pd.DataFrame(standards_list)
    by_std = df_standards.groupby("Standard")["Answer"].apply(lambda x: (x == "Yes").sum() / len(x) * 100 if len(x) > 0 else 0)

    pie = px.pie(df, names="Answer", title="Answer Distribution")
    gap_counts = df[df["Answer"] == "No"]["Domain"].value_counts()
    bar_gaps = px.bar(x=gap_counts.index, y=gap_counts.values, labels={'x': 'Domain', 'y': 'No Answers'}, title="Top Gaps by Domain")

    maturity_scores = {
        'Initial': 1,
        'Repeatable': 2,
        'Defined': 3,
        'Managed': 4,
        'Optimizing': 5,
    }
    domain_maturity = session["domain_maturity"]
    radar_df = pd.DataFrame([{"Domain": d, "Maturity": maturity_scores.get(domain_maturity.get(d, "Initial"), 1)} for d in domain_maturity])
    radar = px.line_polar(radar_df, r='Maturity', theta='Domain', line_close=True, title="Maturity by Domain", range_r=[1, 5])
    main_card.clear()
    with main_card:
        ui.label("Assessment Results").classes("text-2xl font-bold mb-2")
        ui.label(f"Compliance Score: {score}/{max_score} ({percent}%) | Maturity: {maturity}").classes("text-blue-800 mb-3")
        ui.echart({
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": list(by_domain.index)},
            "yAxis": {"type": "value"},
            "series": [{"type": "bar", "data": list(by_domain.values)}],
        }).classes("w-full h-64 mb-4").style("width:100%; height:500px; margin-bottom:36px;")
        ui.echart({ 
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": list(by_std.index)},
            "yAxis": {"type": "value"},
            "series": [{"type": "bar", "data": list(by_std.values)}],
        }).classes("w-full h-64 mb-4").style("width:100%; height:500px; margin-bottom:36px;")
        ui.plotly(pie).classes("mb-4").style("width:100%; height:500px; margin-bottom:36px;")
        ui.plotly(bar_gaps).classes("mb-4").style("width:100%; height:500px; margin-bottom:36px;")
        if not radar_df.empty:
            ui.plotly(radar).style("width:100%; height:900px; margin-bottom:36px;")
        with ui.element('div').style('overflow-x:auto; width:100%;'):
            ui.table.from_pandas(
                df[df["Answer"].isin(["Partial", "No"])]
                [["Control Title", "Domain", "Standards", "Answer", "Recommendation", "Evidence"]]
            ).style("text-align:left;min-width:900px; max-width:100%; margin-bottom:36px;")

        def download():
            df.to_csv("assessment_results.csv", index=False)
            ui.download("assessment_results.csv")
        ui.button("Download CSV", on_click=download).props('color=secondary').classes("mr-2 mt-2")
        ui.button("Export PDF", on_click=lambda: export_pdf(session)).props('color=primary').classes("mr-2 mt-2")
        ui.button("Restart Assessment", on_click=lambda: (reset_session(), refresh())).props('color=negative').classes("mt-2")        