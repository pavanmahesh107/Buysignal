import os
import requests
from datetime import datetime

# Supabase settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def fetch_signals():
    url = f"{SUPABASE_URL}/rest/v1/signals?select=title,permalink,intent_type,summary,tags,source,created_utc&order=created_utc.desc&limit=100"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def generate_dashboard(signals):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Head HTML with design
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>BuySignal AI - Reddit Buying Intent Dashboard</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link href="https://cdn.jsdelivr.net/npm/simple-datatables@latest/dist/style.css" rel="stylesheet" />
      <style>
        body {{
          font-family: Arial, sans-serif;
          background-color: #f9f9f9;
          padding: 20px;
        }}
        h1 {{
          text-align: center;
          color: #4F46E5;
          margin-bottom: 10px;
        }}
        #lastUpdated {{
          text-align: center;
          font-size: 14px;
          color: #888;
          margin-bottom: 20px;
        }}
        table.dataTable-table {{
          width: 100%;
          border-collapse: collapse;
          margin-top: 10px;
        }}
        table.dataTable-table thead {{
          background-color: #4F46E5;
          color: white;
        }}
      </style>
    </head>
    <body>

    <h1>🚀 BuySignal AI - Reddit Buying Intent Dashboard</h1>
    <div id="lastUpdated">Last Updated: {now}</div>

    <table id="dashboardTable" class="dataTable-table">
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

    # Insert signals dynamically
    for signal in signals:
        title = signal.get("title", "No Title")
        permalink = signal.get("permalink", "#")
        intent = signal.get("intent_type", "Unknown")
        summary = signal.get("summary", "")
        tags = ", ".join(signal.get("tags", []))
        source = signal.get("source", "")
        created_utc = signal.get("created_utc", "")[:16].replace("T", " ")

        html += f"""
        <tr>
          <td><a href="{permalink}" target="_blank">{title}</a></td>
          <td>{intent}</td>
          <td>{summary}</td>
          <td>{tags}</td>
          <td>{source}</td>
          <td>{created_utc}</td>
        </tr>
        """

    # Close HTML
    html += """
      </tbody>
    </table>

    <script src="https://cdn.jsdelivr.net/npm/simple-datatables@latest" ></script>
    <script>
      const dataTable = new simpleDatatables.DataTable("#dashboardTable");
    </script>

    </body>
    </html>
    """

    # Save as index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    signals = fetch_signals()
    generate_dashboard(signals)
