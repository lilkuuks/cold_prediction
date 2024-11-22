from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


# Rule-based condition prediction function
def predict_condition(symptoms):
    fever = symptoms.get("Fever", "No")
    cough = symptoms.get("Cough", "No")
    runny_nose = symptoms.get("Runny_Nose", "No")
    sore_throat = symptoms.get("Sore_Throat", "No")
    headache = symptoms.get("Headache", "No")
    fatigue = symptoms.get("Fatigue", "No")

    # Apply rules
    if fever == "Yes" and fatigue == "Yes" and cough == "Yes":
        return "Flu"
    elif runny_nose == "Yes" and sore_throat == "Yes" and cough == "No":
        return "Cold"
    elif all(symptom == "No" for symptom in [fever, cough, runny_nose, sore_throat, headache, fatigue]):
        return "Healthy"
    else:
        return "Unknown"


# Route for form input
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        symptoms = {
            "Fever": request.form.get("fever"),
            "Cough": request.form.get("cough"),
            "Runny_Nose": request.form.get("runny_nose"),
            "Sore_Throat": request.form.get("sore_throat"),
            "Headache": request.form.get("headache"),
            "Fatigue": request.form.get("fatigue"),
        }
        condition = predict_condition(symptoms)
        return render_template("result.html", symptoms=symptoms, condition=condition)
    return render_template("index.html")


# API route for JSON input
@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.json
    condition = predict_condition(data)
    return jsonify({"condition": condition})


if __name__ == "__main__":
    app.run()
