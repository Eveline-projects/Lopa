from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Problem


class ProblemListView(LoginRequiredMixin, ListView):
    model = Problem
    template_name = 'problems/problem_list.html'
    context_object_name = 'problems'

    def get_queryset(self):
        return Problem.objects.filter(is_active=True)


class ProblemDetailView(LoginRequiredMixin, DetailView):
    model = Problem
    template_name = 'problems/problem_detail.html'
    context_object_name = 'problem'
    pk_url_kwarg = 'problem_id'

    def get_queryset(self):
        return Problem.objects.filter(is_active=True)
