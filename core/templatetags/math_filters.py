from django import template

register = template.Library()

@register.filter
def vote_percentage(votes, total):
    try:
        return (votes / total) * 100 if total > 0 else 0
    except:
        return 0
