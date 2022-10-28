from django import template

WORDS = ['редиска', 'спикером', 'пунктов', 'китай', ]

register = template.Library()


@register.filter()
def censor(x):
    text_1 = ''
    if isinstance(x, str):
        for i in x.split():
            if i.lower() in WORDS:
                text_1 += i.replace(i, f'  {i[0]}{"*" * (len(i) - 1)}   ')
            else:
                text_1 += '   ' + i + '   '
        text_1 = ' '.join(text_1.split())
        return text_1
