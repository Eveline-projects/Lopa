from django.urls import path

from .views import ProblemDetailView, ProblemListView

app_name = 'problems'

urlpatterns = [
    path('', ProblemListView.as_view(), name='problems_list'),
    path(
        '<uuid:problem_id>/',
        ProblemDetailView.as_view(),
        name='problem_detail',
    ),
]
