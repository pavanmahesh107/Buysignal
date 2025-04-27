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

def generate_dashboard(signals):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>BuySignal AI - Reddit Insights Dashboard</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f7f7f7; }}
        h1 {{ text-align: center; }}
        #lastUpdated {{ text-align: center; margin-bottom: 20px; font-size: 14px; color: gray; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ border: 1px solid #ccc; padding: 10px; text-align: left; }}
        th {{ background-color: #333; color: white; }}
        tr:nth-child(even) {{ background-color: #eee; }}
      </style>
    </head>
    <body>

    <h1>🚀 BuySignal AI - Reddit Buying Intent Dashboard</h1>
    <div id="lastUpdated">Last Updated: {now}</div>

    <table>
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
        intent = signal.get("intent_type", "Unknown")
        summary = signal.get("summary", "")
        tags = ", ".join(signal.get("tags", []))
        source = signal.get("source", "")
        created = datetime.strptime(signal.get("created_utc"), "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M")

        html += f"""
        <tr>
          <td><a href="{permalink}" target="_blank">{title}</a></td>
          <td>{intent}</td>
          <td>{summary}</td>
          <td>{tags}</td>
          <td>{source}</td>
          <td>{created}</td>
        </tr>
        """

    html += """
      </tbody>
    </table>

    </body>
    </html>
    """

    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    signals = fetch_signals()
    generate_dashboard(signals)
