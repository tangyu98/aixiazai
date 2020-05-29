from django.template.library import Library
from django.template.defaultfilters import stringfilter

register = Library()


@register.filter(is_safe=True)
def ext(value, arg=None):
    exts = ["doc", "docx", "exe", "pdf", "ppt", "rar", "txt", "xlsx", "zip"]
    return value if value in exts else "unknow"


@register.filter(is_safe=True)
@stringfilter
def sex(value, arg=None):
    sets = {"1": "男", "2": "女", "3": "保密"}
    return sets.get(value, "男")


@register.filter(is_safe=True)
def visit(value, arg):
    return "0" if value.get(arg) is None else value.get(arg).decode()
