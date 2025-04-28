from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies two numbers in Django templates."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0  # Return 0 if inputs are invalid
