from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# -------------------------------
# ML LOGIC (UNCHANGED)
# -------------------------------
def predict_risk(X):
    silent_score = (
        0.1 * X["Medicine_Refill_Delay_days"] +
        2.0 * X["Missed_Lab_Tests"] +
        0.1 * X["Days_Late_Follow_Up"]
    )

    score = round(silent_score.iloc[0], 2)

    if score > 9:
        risk = "HIGH"
        action = "Immediate intervention required"
    elif score >= 4:
        risk = "MEDIUM"
        action = "Monitor closely"
    else:
        risk = "LOW"
        action = "Patient engagement healthy"

    return score, risk, action


# -------------------------------
# HOME / LANDING PAGE
# -------------------------------
@app.route("/")
def home():
    return render_template("home.html")


# -------------------------------
# PREDICTION PAGE
# -------------------------------
@app.route("/predict-page")
def predict_page():
    return render_template("index.html")


# -------------------------------
# API (UNCHANGED)
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    df = pd.DataFrame({
        "Medicine_Refill_Delay_days": [data["refill_delay"]],
        "Missed_Lab_Tests": [data["missed_labs"]],
        "Days_Late_Follow_Up": [data["days_late_followup"]]
    })

    score, risk, action = predict_risk(df)

    return jsonify({
        "refill_delay": data["refill_delay"],
        "missed_labs": data["missed_labs"],
        "days_late_followup": data["days_late_followup"],
        "days_since_contact": data["days_since_contact"],
        "score": score,
        "risk": risk,
        "action": action
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
