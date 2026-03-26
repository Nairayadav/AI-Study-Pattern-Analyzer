from flask import Flask, render_template, request
import pickle
import csv

app = Flask(__name__)

model = pickle.load(open("model.pkl","rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    study_hours = float(request.form["study"])
    break_time = float(request.form["break"])
    sleep_hours = float(request.form["sleep"])

    prediction = model.predict([[study_hours, break_time, sleep_hours]])
    result = round(prediction[0],2)

    # save study history
    with open("study_history.csv","a",newline="") as f:
        writer = csv.writer(f)
        writer.writerow([study_hours,break_time,sleep_hours,result])

    # AI suggestion
    suggestion = ""

    if result < 50:
        suggestion = "Increase study hours and sleep better."
    elif result < 75:
        suggestion = "Try longer focus sessions with breaks."
    else:
        suggestion = "Excellent productivity! Keep it up."

    weekly_plan = {
        "Monday": study_hours,
        "Tuesday": study_hours + 1,
        "Wednesday": study_hours,
        "Thursday": study_hours + 1,
        "Friday": study_hours,
        "Saturday": study_hours - 1,
        "Sunday": "Rest"
    }

    return render_template(
        "index.html",
        prediction_text=f"Predicted Productivity: {result}%",
        productivity=result,
        study=study_hours,
        suggestion=suggestion,
        plan=weekly_plan
    )

if __name__ == "__main__":
    app.run(debug=True)