from typing import Literal

from ninja import ModelSchema, Router

from themes.filters import color_distance, hex_to_rgb, themes_name, themes_order
from themes.models import Theme

router = Router()


class ThemeSchema(ModelSchema):
    class Meta:
        model = Theme
        fields = ["name", "ron", "author", "link", "downloads", "created", "updated"]


@router.get("/", response=list[ThemeSchema])
def list_themes(
    request,
    order: Literal["popular", "new", "name", ""] = "",
    search: str = "",
    color: str = "",
    limit: int = 20,
    offset: int = 0,
):
    qs = Theme.objects.filter(approved=True).order_by("-downloads")
    if order:
        qs = themes_order(qs, order)
    if search:
        qs = themes_name(qs, search)
    if color:
        try:
            r, g, b = hex_to_rgb(color)
        except ValueError:
            pass
        else:
            qs = color_distance(qs, (r, g, b))

    return qs[offset : offset + limit]
