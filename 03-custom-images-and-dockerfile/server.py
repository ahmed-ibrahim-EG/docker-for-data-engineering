import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Environment variables
ENVIRONMENT = os.getenv("APP_ENV", "Staging")
PIPELINE_NAME = os.getenv("PIPELINE_NAME", "Customer_ETL")

# 2. CLI arguments (Overriding CMD)
BATCH_MODE = sys.argv[1] if len(sys.argv) > 1 else "Standard"

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        response_text = f"""
        <html>
        <body style='font-family: Arial; padding: 30px; line-height: 1.6;'>
            <h2>🚀 Data Pipeline Status Monitor</h2>
            <p><b>Environment:</b> {ENVIRONMENT}</p>
            <p><b>Pipeline:</b> {PIPELINE_NAME}</p>
            <p><b>Batch Execution Mode:</b> {BATCH_MODE}</p>
        </body>
        </html>
        """
        self.wfile.write(response_text.encode("utf-8"))

if __name__ == "__main__":
    server_address = ("0.0.0.0", 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Service running for {PIPELINE_NAME} on port 8080...")
    httpd.serve_forever()
