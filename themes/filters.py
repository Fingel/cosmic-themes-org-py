from django.db.models import F, QuerySet, functions

from themes.models import Theme

ordering = {
    "POPULAR": "-downloads",
    "NEW": "-created",
    "NAME": "name",
}


def themes_order(qs: QuerySet[Theme], order: str) -> QuerySet[Theme]:
    return qs.order_by(ordering.get(order.upper(), "-downloads"))


def themes_name(qs: QuerySet[Theme], query: str) -> QuerySet[Theme]:
    return qs.filter(name__icontains=query)


def color_distance(qs: QuerySet[Theme], color: tuple[int, int, int]) -> QuerySet[Theme]:
    r, g, b = color
    qs = qs.annotate(
        color_distance=functions.Sqrt(
            (F("red") - r) ** 2 + (F("green") - g) ** 2 + (F("blue") - b) ** 2
        )
    )
    return qs.order_by("color_distance")


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    c = h.lstrip("#")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))
