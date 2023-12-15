from django import template

register = template.Library()

@register.filter
def min_bid(price):
    return (price + (price * 0.05))