from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import Http404
from .models import Result
from apps.submissions.services import SubmissionService
from apps.submissions.models import Submission


class ResultListView(LoginRequiredMixin, ListView):
    model = Result
    template_name = 'results/submission_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        submission_id = self.kwargs['submission_id']
        return Result.objects.filter(
            submission_id=submission_id, submission__user=self.request.user
        ).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['submission'] = SubmissionService.get_submission_by_id(
                self.kwargs['submission_id']
            )
            if context['submission'].user != self.request.user:
                raise Http404('Access denied')
        except (Submission.DoesNotExist, AttributeError):
            raise Http404('Submission not found')

        return context


class ResultDetailView(LoginRequiredMixin, DetailView):
    model = Result
    template_name = 'results/result_detail.html'
    context_object_name = 'result'

    def get_queryset(self):
        return Result.objects.select_related('submission', 'test_case').filter(
            submission__user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submission'] = self.object.submission
        return context
