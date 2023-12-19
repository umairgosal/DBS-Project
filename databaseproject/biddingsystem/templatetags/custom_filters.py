from django import template

register = template.Library()

@register.filter(name="bidAmt")
def min_bid(price):
    return (price + (price * 0.05))

@register.filter
def calc_topup_amt(amount):
    return int(amount) * 100