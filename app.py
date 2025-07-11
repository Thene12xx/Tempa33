from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

questions = [
    {
        "text": "Pilot\nWhy do you think you belong here?",
        "choices": ["A. I am a THENE", "B. Because why not", "C. I'm chosen"]
    },
    {
        "text": "Do you feel special",
        "choices": ["A. Yes", "B. No", "C. I feel depressed"]
    },
    {
        "text": "What do you think THENE stands for",
        "choices": ["A. Time he engaged never ended", "B. The end", "C. The one."]
    },
    {
        "text": "Visualise a pink horse In your head",
        "choices": ["A. I CANT", "B. I CAN", "C. I CAN BUT IF SOMEONE ELSE TELLS ME I CANT"]
    },
    {
        "text": "Spell time _____",
        "choices": None
    }
]

# Correct answers you gave:
correct_answers = [
    "C. I'm chosen",           # 1
    "A. Yes",                  # 2
    "C. The one.",             # 3
    "B. I CAN",                # 4
    None                       # 5: free text; we can accept anything or set a rule
]

submitted_results = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        answers = []
        correctness = []
        for i, q in enumerate(questions):
            answer = request.form.get(f"answer_{i}")
            answers.append(answer)
            # Compare answer to correct answer (skip for text if correct answer is None)
            if correct_answers[i]:
                is_correct = answer.strip().lower() == correct_answers[i].strip().lower()
            else:
                is_correct = True  # Accept any text input as correct
            correctness.append(is_correct)
        submitted_results.append({"answers": answers, "correctness": correctness})
        return redirect(url_for("thank_you", index=len(submitted_results)-1))
    return render_template("questions.html", questions=questions)

@app.route("/thank_you/<int:index>")
def thank_you(index):
    result = submitted_results[index]
    return render_template("thank_you.html", questions=questions,
                           answers=result["answers"], correctness=result["correctness"])

if __name__ == "__main__":
    app.run(debug=True)