from django.contrib import messages
from django.db.models import F, Sum
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# def index(request):
#         latest_question_list = Question.objects.order_by('-pub_date')[:5]
#         context = {'latest_question_list': latest_question_list}
#         return render(request, 'index.html', context)

def index(request):
        latest_question_list = Question.objects.annotate(
        latest_votes=Sum("choice__votes")
        ).order_by("-pub_date")[:5]
        context = {"latest_question_list": latest_question_list}
        return render(request, "index.html", context)


def detail(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'detail.html', {'question': question })

def vote (request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
                selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesMotExist):
                return render(request, "detail.html", {
                      "question":  question,
                      "error_message": "Сначала выберите вариант ответа!"
                })
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        messages.success(request, "Спасибо! Ваш голос учтён.")
        return HttpResponseRedirect(reverse("results", aegs=(question.id,)))

def results(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        choices = list(question.choice_set.all())
        total = sum(choice.votes for choice in choices)
        for choice in choices:
                choice.percent = round(choice.votes * 100 / total) if total else 0
        context = {"question": question, "choices": choices, "total": total}
        return render(request, "results.html", context)
