from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Submission


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = 'submission_results.html'
    context_object_name = 'submission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problem'] = self.object.problem
        return context


class UserSubmissionListView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = 'submissions/user_submissions.html'
    context_object_name = 'submissions'
    paginate_by = 10

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user).order_by(
            '-created_at'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problem'] = self.object.prolem
        return context
