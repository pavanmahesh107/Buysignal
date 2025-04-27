import os
import requests
from datetime import datetime

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def fetch_signals():
    """Fetch latest signals from Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/signals?select=title,permalink,intent_type,summary,tags,source,created_utc,category&order=created_utc.desc&limit=100"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def generate_dashboard(signals):
    """Generate colorful dashboard HTML from signals."""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    rows_html = ""

    for signal in signals:
        title = signal.get("title", "No Title")
        permalink = signal.get("permalink", "#")
        intent = signal.get("intent_type", "unknown")
        summary = signal.get("summary", "")
        tags = signal.get("tags", [])
        source = signal.get("source", "")
        created = datetime.fromisoformat(signal.get("created_utc").replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M")

        # Handle intent class
        intent_class = f"intent-{intent}" if intent else "intent-unknown"

        # Create tags HTML
        tags_html = " ".join(f'<span class="tag">{tag}</span>' for tag in tags)

        # Build a row
        rows_html += f"""
        <tr>
          <td><a href="{permalink}" target="_blank">{title}</a></td>
          <td><span class="{intent_class}">{intent.capitalize()}</span></td>
          <td>{summary}</td>
          <td>{tags_html}</td>
          <td>{source}</td>
          <td>{created}</td>
        </tr>
        """

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>🚀 BuySignal AI - Reddit Buying Intent Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css">
  <style>
    body {{ font-family: 'Inter', sans-serif; margin: 20px; background-color: #f9fafb; }}
    h1 {{ text-align: center; background: linear-gradient(90deg, #4f46e5, #6366f1); color: white; padding: 15px; border-radius: 8px; font-size: 28px; }}
    #lastUpdated {{ text-align: center; margin-top: 10px; font-size: 14px; color: #666; }}
    table {{ width: 100%; margin-top: 20px; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }}
    th {{ background-color: #4f46e5; color: white; padding: 10px; }}
    td {{ padding: 10px; font-size: 14px; }}
    tr:nth-child(even) {{ background-color: #f1f5f9; }}
    tr:hover {{ background-color: #e0e7ff; }}
    .tag {{ display: inline-block; background-color: #e5e7eb; border-radius: 20px; padding: 3px 8px; margin: 2px; font-size: 12px; color: #374151; }}
    .intent-discovery {{ background-color: #dbeafe; color: #1d4ed8; padding: 5px 8px; border-radius: 8px; }}
    .intent-decision {{ background-color: #d1fae5; color: #059669; padding: 5px 8px; border-radius: 8px; }}
    .intent-frustration {{ background-color: #fee2e2; color: #dc2626; padding: 5px 8px; border-radius: 8px; }}
    .intent-recommendation {{ background-color: #fef9c3; color: #ca8a04; padding: 5px 8px; border-radius: 8px; }}
    .intent-churn {{ background-color: #fecaca; color: #b91c1c; padding: 5px 8px; border-radius: 8px; }}
    .intent-unknown {{ background-color: #d1d5db; color: #374151; padding: 5px 8px; border-radius: 8px; }}
  </style>
</head>
<body>

<h1>🚀 BuySignal AI - Reddit Buying Intent Dashboard</h1>
<div id="lastUpdated">Last Updated: {now}</div>

<table id="dashboardTable" class="display">
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
    {rows_html}
  </tbody>
</table>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
<script>
  $(document).ready(function() {{
    $('#dashboardTable').DataTable({{
      "pageLength": 20
    }});
  }});
</script>

</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    signals = fetch_signals()
    generate_dashboard(signals)
