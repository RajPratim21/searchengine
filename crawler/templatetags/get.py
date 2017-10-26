from django import template
register=template.Library()
@register.filter
def get(mapping,key):
    return mapping.get(key,'')

@register.filter
def trim(value):
    return value.replace("\r","").replace("\n","").strip()