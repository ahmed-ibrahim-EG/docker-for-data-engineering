import os
import socket
import datetime
import pymssql
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    return pymssql.connect(
        server=os.getenv("DB_HOST", "sqlserver"),
        user=os.getenv("DB_USER", "sa"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "master"),
        port=int(os.getenv("DB_PORT", 1433)),
        as_dict=True
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        IF OBJECT_ID('dbo.PipelineMetrics', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.PipelineMetrics (
                pipeline_id NVARCHAR(100) PRIMARY KEY,
                status NVARCHAR(20),
                total_records_ingested INT,
                quarantined_records INT,
                target_sink NVARCHAR(100),
                last_updated DATETIME DEFAULT GETDATE()
            );
            INSERT INTO dbo.PipelineMetrics 
                (pipeline_id, status, total_records_ingested, quarantined_records, target_sink)
            VALUES 
                ('batch-etl-daily', 'UP', 254300, 18, 'SQL_Server_SalesDB');
        END
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Data Engineering Ingestion Telemetry",
        "container_id": socket.gethostname(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200

@app.route("/health", methods=["GET"])
def health_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return jsonify({
            "status": "Healthy",
            "database_connected": True
        }), 200
    except Exception as e:
        return jsonify({
            "status": "Unhealthy",
            "database_connected": False,
            "error": str(e)
        }), 500

@app.route("/metrics", methods=["GET"])
def metrics():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM dbo.PipelineMetrics")
    row = cursor.fetchone()
    conn.close()

    if row and "last_updated" in row and isinstance(row["last_updated"], (datetime.date, datetime.datetime)):
        row["last_updated"] = row["last_updated"].isoformat()

    return jsonify(row), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)