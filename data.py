import pandas as pd
import os

DATA_PATH = "assessment_controls.xlsx"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

REQUIRED_COLUMNS = [
    "Control ID", "Standard", "Domain", "Clause ID",
    "Control Title", "Control Description", "Recommendation", "Comment"
]

def load_controls():
    df = pd.read_excel(DATA_PATH, engine="openpyxl")
    if not all(col in df.columns for col in REQUIRED_COLUMNS):
        raise Exception(f"Missing columns: {REQUIRED_COLUMNS}")
    df = df.drop_duplicates(subset=["Control ID", "Standard", "Domain", "Clause ID"])
    return df

controls_df = load_controls()
all_standards = sorted(controls_df["Standard"].dropna().unique())
all_domains = sorted(controls_df["Domain"].dropna().unique())
maturity_levels = ['Initial', 'Repeatable', 'Defined', 'Managed', 'Optimizing']
