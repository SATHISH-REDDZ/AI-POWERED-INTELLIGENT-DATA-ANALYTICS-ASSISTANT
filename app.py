from flask import Flask, render_template, request

from llm_assistant import ask_ai

from visualization import (
    create_survival_chart,
    create_gender_chart,
    create_age_histogram,
    create_heatmap
)

from prediction import train_model

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

@app.route("/", methods=["GET", "POST"])
def home():

    response = ""

    if request.method == "POST":

        question = request.form["question"]

        if "chart" in question.lower():

            create_survival_chart()
            create_gender_chart()
            create_age_histogram()
            create_heatmap()

            response = "All Charts Generated Successfully"

        elif "train" in question.lower():

            accuracy = train_model()

            response = f"Model Trained Successfully. Accuracy: {accuracy}%"

        else:

            response = ask_ai(question)

    return render_template(
        "index.html",
        response=response,
        charts=True
    )

if __name__ == "__main__":
    app.run(debug=True)