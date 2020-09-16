from django import template
from Main.models import Order, Coupon, Post

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].course.count()
    return 0

@register.filter
def coupon_code_count(code):
    qs = Coupon.objects.all().count()
    return qs

@register.filter
def post_counter(pk):
    qs = Post.objects.all().count()
    return qs

@register.filter
def category_count(category):
    qs = Post.objects.filter(category=category)
    if qs.exists:
        return qs.count()
    return 0