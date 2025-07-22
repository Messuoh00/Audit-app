Audit App
A web-based application for generating audit statistics and charts from uploaded data files.
Fully deployed at: https://audit-app-pvmp.onrender.com/

Features
Upload CSV files for instant analysis

Generate visual charts and statistical summaries

Interactive, user-friendly web interface

Runs fully in the browser (no installation required for end users)

Supports export of charts and data

How to Run Locally
Clone the repository

git clone https://github.com/yourusername/audit-app.git
cd audit-app
Install dependencies

Make sure you have Python 3.8+ and pip. Then run:

pip install -r requirements.txt

Start the app

streamlit run main-app.py
or (if using Flask or FastAPI, adjust the command accordingly).

Open in your browser
Visit http://localhost:8501 or the port shown in your terminal.

Requirements
Python 3.8+

Streamlit (or Flask/FastAPI, adjust as per your stack)

Pandas, Matplotlib, Plotly, etc. (see requirements.txt)

Deployment
The app is currently deployed for demo at:
https://audit-app-pvmp.onrender.com/

Author
Houssem Eddine Merabatte
