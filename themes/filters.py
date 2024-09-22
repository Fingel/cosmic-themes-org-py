from django.db.models import QuerySet

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
