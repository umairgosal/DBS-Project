from django import template

register = template.Library()

@register.filter
def min_bid(price):
    return (price + (price * 0.05))

@register.filter
def user_not_follows():
    return True