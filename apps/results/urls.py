from django.urls import path
from .views import ResultListView, ResultDetailView

app_name = 'results'

urlpatterns = [
    path(
        'submissions/<uuid:submission_id>/results/',
        ResultListView.as_view(),
        name='submission_results',
    ),
    path(
        'result/<uuid:pk>/', ResultDetailView.as_view(), name='result_detail'
    ),
]
