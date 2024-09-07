from django import template

register = template.Library()


@register.filter
def current_route(request, route):
    current = f"{request.resolver_match.app_name}:{request.resolver_match.url_name}"
    return "active" if route == current else ""
