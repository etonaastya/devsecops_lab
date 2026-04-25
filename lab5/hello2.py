
import os
import socket
from datetime import datetime
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return f"<h1>Hello, AppSec World! 🛡️</h1><p>Container: {socket.gethostname()}</p>"

@app.route('/health')
def health():
    return {"status": "ok", "ts": datetime.utcnow().isoformat() + "Z"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
