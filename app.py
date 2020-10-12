from flask import Flask, request, render_template, redirect, session, flash, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretKey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def start_page():
    return render_template('main.html', survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session["responses"] = []
    return redirect("/questions/0")


@app.route('/answer', methods=["POST"])
def handle_question():
  """ save and redirect """
  choice = request.form['answer']

  responses = session["responses"]
  responses.append(choice)
  session["responses"] = responses

  if (len(responses) == len(survey.questions)):
    return redirect('/complete')
  else:
    return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def show_question(qid):
    responses = session.get("responses")

    if (responses is None):
      
        return redirect("/")

    if (len(responses) == len(survey.questions)):
  
        return redirect("/complete")

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)



@app.route("/complete")
def complete():
    return render_template("completion.html")
