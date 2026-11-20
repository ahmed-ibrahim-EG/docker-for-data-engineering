import socket
import datetime
from flask import Flask, jsonify

app = Flask(__name__)

PIPELINE_STATE = {
    "pipeline_id": "batch-etl-daily",
    "status": "UP",
    "total_records_ingested": 254300,
    "quarantined_records": 18,
    "target_sink": "SQL_Server_SalesDB"
}

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Data Engineering Ingestion Telemetry",
        "container_id": socket.gethostname(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "Healthy",
        "database_connected": True
    }), 200

@app.route("/metrics", methods=["GET"])
def metrics():
    return jsonify(PIPELINE_STATE), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
