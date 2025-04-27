import os
import requests
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def fetch_signals():
    url = f"{SUPABASE_URL}/rest/v1/signals?select=title,permalink,intent_type,summary,tags,source,created_utc,category&order=created_utc.desc&limit=100"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def intent_badge(intent):
    color_map = {
        "discovery": "#8e44ad",       # purple
        "frustration": "#e74c3c",      # red
        "recommendation": "#27ae60",   # green
        "comparison": "#f1c40f",       # yellow
        "decision": "#3498db",         # blue
        "validation": "#e67e22",       # orange
        "churn": "#2c3e50",            # dark gray
        "none": "#95a5a6"              # light gray
    }
    color = color_map.get(intent.lower(), "#7f8c8d")  # default gray
    return f'<span style="background-color:{color};color:white;padding:4px 8px;border-radius:5px;">{intent.capitalize()}</span>'

def generate_dashboard(signals):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>BuySignal AI - Reddit Insights Dashboard</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://cdn.datatables.net/1.13.5/css/jquery.dataTables.min.css">
      <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
      <script src="https://cdn.datatables.net/1.13.5/js/jquery.dataTables.min.js"></script>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f7f7f7; }}
        h1 {{ text-align: center; color: #5b2c6f; }}
        #lastUpdated {{ text-align: center; margin-bottom: 20px; font-size: 14px; color: gray; }}
        table {{ width: 100%; }}
        th {{ background-color: #4a47a3; color: white; }}
        .dataTables_wrapper .dataTables_length, 
        .dataTables_wrapper .dataTables_filter, 
        .dataTables_wrapper .dataTables_info, 
        .dataTables_wrapper .dataTables_paginate {{
            margin-bottom: 20px;
        }}
      </style>
    </head>
    <body>

    <h1>🚀 BuySignal AI - Reddit Buying Intent Dashboard</h1>
    <div id="lastUpdated">Last Updated: {now}</div>

    <table id="dashboard">
      <thead>
        <tr>
          <th>Post Title</th>
          <th>Intent Type</th>
          <th>Summary</th>
          <th>Tags</th>
          <th>Source</th>
          <th>Created At</th>
        </tr>
      </thead>
      <tbody>
    """

    for signal in signals:
        title = signal.get("title", "No Title")
        permalink = signal.get("permalink", "#")
        intent = signal.get("intent_type", "none")
        summary = signal.get("summary", "")
        tags = ", ".join(signal.get("tags", []))
        source = signal.get("source", "")
        created = datetime.fromisoformat(signal.get("created_utc").replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M")
        badge_html = intent_badge(intent)

        html += f"""
        <tr>
          <td><a href="{permalink}" target="_blank">{title}</a></td>
          <td>{badge_html}</td>
          <td>{summary}</td>
          <td>{tags}</td>
          <td>{source}</td>
          <td>{created}</td>
        </tr>
        """

    html += """
      </tbody>
    </table>

    <script>
      $(document).ready(function() {
        $('#dashboard').DataTable();
      });
    </script>

    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    signals = fetch_signals()
    generate_dashboard(signals)
