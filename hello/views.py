import json

import requests as requests
from django.shortcuts import render, HttpResponse, redirect

from .models import Greeting


# Create your views here.

def searchresult(request):
    try:
        rollno = request.GET["rollno"]
        d = {"status": "ok", "rollno": rollno, "result": "passed"}
        d = json.dumps(d)
        return HttpResponse(d)
    except:
        d = {"status": "error"}
        d = json.dumps(d)
        return HttpResponse(d)


def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def apiquiz(request):
    answers = request.session.get("answers")
    if answers == None:
        answers = []
    qno = 0
    if qno == 0:
        try:
            request.session.pop("answers")
        except:
            pass
    p = ''
    response = requests.get(
        'https://gist.githubusercontent.com/champaksworldcreate/320e5af5ea9dbd31597d220637885587/raw/99f8f7a4df34ae477dcceb62598aa0bdde9ef685/tfquestions.json')
    data = response.json()
    data = data.get("questions")
    p = data[qno]["question"]
    # print(len(data))
    # print(data)
    if request.GET:
        option = int(request.GET["option"])
        if option == 1:
            option = "true"
        else:
            option = "false"

        correctanswer = data[qno].get("correctanswer")
        # print(option, correctanswer)
        iscorrect = option == correctanswer  # this will give us a boolean option

        answers.append(iscorrect)
        request.session["answers"] = answers
        print((iscorrect))
        qno = int(request.GET["qno"])
        qno += 1
        if qno >= len(data):
            return render(request, "result.html", {"answer": answers})
        p = data[qno]["question"]
    # print(p)
    return render(request, "apitest.html", {"data": p, "qnumber": qno + 1, "qno": qno})


def login(request):
    title = ""
    session = request.session
    try:

        del session["answers"]
    except:
        pass
    if request.POST:
        # email = request.POST['email']
        # password = request.POST['password']
        title = request.POST['title']
        session["name"] = title
        return redirect("/quiz/")
        # return render(request, "quiz.html", {"title": title, "session": session})
    return render(request, "login.html", {"session": session})


# <<<---- Login Page Ends Here ---->>

def quiz(request):

    answers = request.session.get("answers")
    if answers == None:
        answers = []

    q1 = {"question": "What is C?", "op1": "Language", "op2": "Alphabet", "op3": "Ascii character",
          "op4": "All of these", "correct": "a"}
    q2 = {"question": "Who developed Python Programming language?", "op1": "Wick van rossum", "op2": "Dennis Ritchie",
          "op3": "Guido van Rossum", "op4": "none", "correct": "c"}
    q3 = {"question": "Which of the following is the correct extension of the python file?", "op1": ".python",
          "op2": ".pl", "op3": ".py", "op4": ".p", "correct": "c"}
    q4 = {"question": "Who developed C programming language ?", "op1": "denies ritchies", "op2": "Guido van Rossum",
          "op3": "harsh", "op4": "none", "correct": "a"}
    q5 = {"question": "Django is  a ?", "op1": "Programming Language", "op2": "Framework",
          "op3": "Python Web Framework", "op4": "None", "correct": "c"}
    questions = [q1, q2, q3, q4, q5]
    questionno = 0
    q=questionno
    givenanswer = ""
    correctanswer = ""
    result = ""
    totalmarks = 0
    if not request.POST:
        try:
            del request.session["answers"]
        except:
            pass

    if request.POST:
        questionno = int(request.POST["qno"])
        givenanswer = request.POST["option"]
        questionno = int(request.POST["qno"])
        totalmarks = int(request.POST["totalmarks"])
        correctanswer = questions[questionno].get("correct")
        questionno += 1
        totalmarks += 1
        result = "Yes"
        q=questionno

        print(questionno)
        if givenanswer != correctanswer:
            result = "No"
            totalmarks -= 1
            data = {"qno": (questionno - 1), "answer": givenanswer, "correct": correctanswer, "result": result}
            answers.append(data)
            if questionno >= len(questions):
                return render(request, 'result.html', {"totalmarks": totalmarks,
                                                   "answers": answers})
    # return httpResponse('python quiz!')
    request.session["answers"] = answers
    return render(request, "quiz.html",
                  {"question": questions[questionno],
                   "showqno": questionno + 1,
                   "qno": questionno,
                   "givenanswer": givenanswer,
                   "correctanswer": correctanswer,
                   "result": result,
                   "totalmarks": totalmarks, "answers": answers})
