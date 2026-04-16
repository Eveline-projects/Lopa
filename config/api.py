from ninja import NinjaAPI
from apps.problems.api import router as problems_router

api = NinjaAPI(title="Lopa API")

api.add_router('/problems', problems_router)
