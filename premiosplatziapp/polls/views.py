from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from tomlkit import comment
from .models import Question, Choice


""" def index(request):
    latest_question_list = Question.objects.all()
    return render(request, "polls/index.html", {
        "latest_question_list": latest_question_list
    })


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {
        "question": question
    })


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request,"polls/results.html",{
        "question":question
    })
     """

""" Las Generic Views se pueden usar si:
        Cargo base de datos
        Genero template
        Muestro template
        
    Las Function Based Views se pueden usar si:
        La vista es más compleja
        Ej. Mostrar 2 formularios en una misma página"""

#Index, Detail y Result son Generic Views
class IndexView(ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published question"""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultView(DetailView):
    model = Question
    template_name = "polls/results.html"

#Vote es una Function Based View porque es una vista compleja
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "No elegiste una respuesta"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        return redirect("polls:results", question.id)