from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

resources = []
incidents = []

def distance(a, b):
    return math.sqrt((a['lat'] - b['lat'])**2 + (a['lon'] - b['lon'])**2)

def allocate(incident):
    available = [r for r in resources if r["available"]]
    if not available:
        return None
    closest = min(available, key=lambda r: distance(r, incident))
    closest["available"] = False
    return closest

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_resource", methods=["POST"])
def add_resource():
    data = request.json
    resource = {
        "id": len(resources) + 1,
        "type": data["type"],
        "lat": float(data["lat"]),
        "lon": float(data["lon"]),
        "available": True
    }
    resources.append(resource)
    return jsonify(resource)

@app.route("/report_incident", methods=["POST"])
def report_incident():
    data = request.json
    incident = {
        "id": len(incidents) + 1,
        "lat": float(data["lat"]),
        "lon": float(data["lon"]),
        "severity": data["severity"]
    }

    assigned = allocate(incident)
    incident["assigned"] = assigned
    incidents.append(incident)

    return jsonify(incident)

@app.route("/status")
def status():
    return jsonify({"resources": resources, "incidents": incidents})

if __name__ == "__main__":
    app.run(debug=True)
