import os
import json
import subprocess
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = "changeme"

CONFIG_DIR = "configs"
os.makedirs(CONFIG_DIR, exist_ok=True)


# -------------------------------
# HOME
# -------------------------------
@app.route("/")
def index():
    # nuovo percorso template: templates/index/index.html
    return render_template("index/index.html")


# -------------------------------
# CREAZIONE NUOVO CONFIG
# -------------------------------
@app.route("/create", methods=["GET", "POST"])
def create_config():
    if request.method == "POST":

        # dati base dal form
        active_profile = request.form.get("activeProfile")
        separator_width = int(request.form.get("separatorWidth") or 120)

        raw_team_sizes = request.form.get("teamSizes", "[]")

        try:
            team_sizes = json.loads(raw_team_sizes)
        except:
            team_sizes = []

        if not team_sizes:
            team_sizes = [1]


        # apps
        apps_raw = request.form.get("apps")   # formato: name|path\nname|path\n...
        weights_raw = request.form.get("weights")  # JSON

        try:
            weights = json.loads(weights_raw)
        except:
            flash("Errore nel parsing del campo 'weights'", "danger")
            return redirect(url_for("create_config"))

        apps = []
        if apps_raw.strip():
            for line in apps_raw.splitlines():
                if "|" in line:
                    name, path = line.split("|", 1)
                    apps.append({"name": name.strip(), "path": path.strip()})

        # costruzione config completo
        config = {
            "activeProfile": active_profile,
            "ui": {"separatorWidth": separator_width},
            "apps": apps,
            "profiles": {
                active_profile: {
                    "defaultIncludes": ["*.ts", "*.html"],
                    "palette": ["Green", "Cyan", "Yellow"],

                    # --- NEW: usa realmente i valori scelti dall'utente ---
                    "teamSizes": team_sizes,

                    "migrationTo": {"factor": float(request.form.get("migrationFactor", "1.0"))},
                    "weights": weights,
                    "complexity": None
                }
            }
        }

        # salva file
        filename = f"config-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        path = os.path.join(CONFIG_DIR, filename)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        flash(f"Config salvato come {filename}", "success")
        return redirect(url_for("list_configs"))

    # nuovo percorso template: templates/create/create.html
    return render_template("create/create.html")




# -------------------------------
# LISTA CONFIG SALVATI
# -------------------------------
@app.route("/configs")
def list_configs():
    files = [f for f in os.listdir(CONFIG_DIR) if f.endswith(".json")]
    files.sort(reverse=True)

    # nuovo percorso template: templates/list/list.html
    return render_template("list/list.html", files=files)

@app.route("/configs/<name>/json")
def get_config_json(name):
    full_path = os.path.join(CONFIG_DIR, name)
    if not os.path.exists(full_path):
        return jsonify({"error": "Config non trovato"}), 404

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Errore lettura file: {e}"}), 500

    return jsonify(data)


# -------------------------------
# SERVE REPORT HTML GENERATO
# -------------------------------
@app.route("/report")
def show_report():
    # percorso del file generato dall'estimator
    report_path = "estimator_report.html"

    if not os.path.exists(report_path):
        return "Nessun report generato.", 404

    # lo restituiamo direttamente come file HTML statico
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    return content

# -------------------------------
# ESECUZIONE ESTIMATOR
# -------------------------------
@app.route("/run/<name>")
def run_estimator(name):

    full_path = os.path.join(CONFIG_DIR, name)
    if not os.path.exists(full_path):
        flash("Config non trovato.", "danger")
        return redirect(url_for("list_configs"))

    # Esegue l'estimator come sottoprocesso
    try:
        process = subprocess.Popen(
            ["python", "-m", "estimator", full_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

    except Exception as e:
        stdout = ""
        stderr = f"Errore esecuzione: {e}"

    # Legge il report HTML generato
    html_report_path = "estimator_report.html"
    report_html = ""
    if os.path.exists(html_report_path):
        with open(html_report_path, "r", encoding="utf-8") as f:
            report_html = f.read()

    # nuovo percorso template: templates/run/run.html
    return render_template(
        "run/run.html",
        name=name,
        stdout=stdout,
        stderr=stderr,
        report_html=report_html
    )


if __name__ == "__main__":
    app.run(debug=True)
