from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Exists, OuterRef
from .models import Problem
from apps.submissions.models import Submission


class ProblemListView(LoginRequiredMixin, ListView):
    model = Problem
    template_name = 'problems/problem_list.html'
    context_object_name = 'problems'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)

        if self.request.user.is_authenticated:
            solved_subquery = Submission.objects.filter(
                problem=OuterRef('pk'), user=self.request.user, status='DONE'
            )
            queryset = queryset.annotate(is_solved=Exists(solved_subquery))
        return queryset


class ProblemDetailView(LoginRequiredMixin, DetailView):
    model = Problem
    template_name = 'problems/problem_detail.html'
    context_object_name = 'problem'
    pk_url_kwarg = 'problem_id'

    def get_queryset(self):
        return Problem.objects.filter(is_active=True)
