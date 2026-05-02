from django.urls import path
from .views import ResultListView

app_name = 'results'

urlpatterns = [
    path(
        'submissions/<uuid:submission_id>/results/',
        ResultListView.as_view(),
        name='submission_results',
    ),
]
