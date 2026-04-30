from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Result
from apps.submissions.models import Submission


class ResultListView(LoginRequiredMixin, ListView):
    model = Result
    template_name = 'results/submission_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        submission_id = self.kwargs['submission_id']
        return Result.objects.filter(submission_id=submission_id).order_by(
            'id'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submission'] = Submission.objects.get(
            id=self.kwargs['submission_id']
        )
        return context
