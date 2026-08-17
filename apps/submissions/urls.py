from django.urls import path

from .views import UserSubmissionListView

app_name = 'submissions'

urlpatterns = [
    path(
        'user_submissions/',
        UserSubmissionListView.as_view(),
        name='user_submissions',
    )
]
