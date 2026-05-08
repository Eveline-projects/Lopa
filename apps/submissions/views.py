from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Submission


class UserSubmissionListView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = 'submissions/user_submissions.html'
    context_object_name = 'submissions'
    paginate_by = 10

    def get_queryset(self):
        return (
            Submission.objects.filter(user=self.request.user)
            .select_related('problem')
            .order_by('-created_at')
        )
