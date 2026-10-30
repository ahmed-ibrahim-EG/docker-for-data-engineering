import os
import random
import time
from flask import Flask, redirect, render_template_string, url_for
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# قراءة إعدادات الاتصال بقاعدة البيانات من متغيرات البيئة
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "analytics_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "secret")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_db_connection():
  return psycopg2.connect(
      host=DB_HOST,
      database=DB_NAME,
      user=DB_USER,
      password=DB_PASS,
      port=DB_PORT,
      cursor_factory=RealDictCursor,
  )


def init_db():
  """حلقة انتظار للتأكد من جاهزية قاعدة البيانات ثم إنشاء الجدول تلقائياً"""
  retries = 10
  while retries > 0:
    try:
      conn = get_db_connection()
      cur = conn.cursor()
      cur.execute("""
                CREATE TABLE IF NOT EXISTS sensor_telemetry (
                    id SERIAL PRIMARY KEY,
                    sensor_id VARCHAR(50),
                    reading_value FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
      conn.commit()
      cur.close()
      conn.close()
      print("[+] Database connected and table initialized successfully!")
      break
    except Exception as e:
      retries -= 1
      print(
          f"[-] Waiting for Postgres... retrying in 2 seconds ({retries}"
          " left)"
      )
      time.sleep(2)


# كود صفحة العرض مدمج كـ HTML String مباشرة
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Data Pipeline Dashboard</title>
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: #f8fafc; padding: 30px; margin: 0; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
        .btn { background: #2563eb; color: white; padding: 10px 18px; border: none; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; }
        .btn:hover { background: #1d4ed8; }
        .cards { display: flex; gap: 20px; margin-bottom: 25px; }
        .card { background: #1e293b; padding: 20px; border-radius: 8px; flex: 1; border-left: 5px solid #38bdf8; }
        .card h3 { margin: 0; font-size: 13px; color: #94a3b8; }
        .card p { margin: 10px 0 0 0; font-size: 26px; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 8px; overflow: hidden; }
        th, td { padding: 12px 16px; text-align: left; }
        th { background-color: #334155; color: #f8fafc; }
        tr:nth-child(even) { background-color: #172033; }
        .badge { background: #0284c7; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Data Pipeline Telemetry Monitor</h2>
        <a href="/generate" class="btn">+ Generate 50 New Rows (Ingest ETL)</a>
    </div>

    <div class="cards">
        <div class="card">
            <h3>TOTAL RECORDS IN WAREHOUSE</h3>
            <p>{{ total }}</p>
        </div>
        <div class="card">
            <h3>AVERAGE VALUE</h3>
            <p>{{ avg }}</p>
        </div>
    </div>

    <h3>Latest 15 Ingested Records</h3>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Sensor ID</th>
                <th>Reading Value</th>
                <th>Timestamp</th>
            </tr>
        </thead>
        <tbody>
            {% for row in records %}
            <tr>
                <td>{{ row.id }}</td>
                <td><span class="badge">{{ row.sensor_id }}</span></td>
                <td>{{ row.reading_value }}</td>
                <td>{{ row.created_at }}</td>
            </tr>
            {% else %}
            <tr>
                <td colspan="4" style="text-align: center; color: #94a3b8;">No records found yet. Click the button above!</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""


@app.route("/")
def index():
  records = []
  total_count = 0
  avg_val = 0
  try:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) AS count, AVG(reading_value) AS avg_val FROM"
        " sensor_telemetry;"
    )
    stats = cur.fetchone()
    if stats:
      total_count = stats["count"]
      avg_val = round(stats["avg_val"], 2) if stats["avg_val"] else 0

    cur.execute(
        "SELECT id, sensor_id, reading_value, created_at FROM sensor_telemetry"
        " ORDER BY id DESC LIMIT 15;"
    )
    records = cur.fetchall()
    cur.close()
    conn.close()
  except Exception as e:
    print(f"[-] Query Error: {e}")

  return render_template_string(
      HTML_TEMPLATE, records=records, total=total_count, avg=avg_val
  )


@app.route("/generate")
def generate_data():
  """محاكاة مهمة ETL سريعة تضخ 50 قراءة جديدة بضغطة زر"""
  try:
    conn = get_db_connection()
    cur = conn.cursor()
    sensors = ["TEMP_ROOM_1", "PRESSURE_PUMP_2", "HUMIDITY_ZONE_A"]
    for _ in range(50):
      cur.execute(
          "INSERT INTO sensor_telemetry (sensor_id, reading_value) VALUES (%s,"
          " %s);",
          (random.choice(sensors), round(random.uniform(20.0, 99.0), 2)),
      )
    conn.commit()
    cur.close()
    conn.close()
  except Exception as e:
    print(f"[-] Ingest Error: {e}")

  return redirect(url_for("index"))


if __name__ == "__main__":
  init_db()
  app.run(host="0.0.0.0", port=5000)