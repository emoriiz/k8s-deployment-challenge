from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Hallo von der Flask Application mit neuer Version</p>"

@app.route("/healthz")
def healthz():
    # Echtes JSON: {"status": "healthy"}
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    # Docker Container auch von außen erreichbar machen
    app.run(host="0.0.0.0", port=5000)