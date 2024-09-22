from ninja import NinjaAPI

from themes.api import router as themes_router

api = NinjaAPI(title="Cosmic Themes")
api.add_router("/themes/", themes_router)
