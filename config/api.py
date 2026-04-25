from ninja import NinjaAPI
from apps.problems.api import router as problems_router
from apps.test_cases.api import router as test_cases_router
from apps.results.api import router as results_router

api = NinjaAPI(title='Lopa API')

api.add_router('/problems', problems_router)
api.add_router('', test_cases_router)
api.add_router('', results_router)
