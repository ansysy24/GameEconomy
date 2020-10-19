from django import template

from django_celery_beat.models import PeriodicTask

register = template.Library()


@register.simple_tag
def cron_tag():
    lottery_task = PeriodicTask.objects.get(name='lottery')
    if lottery_task:
        fields = ['_orig_minute', '_orig_hour', '_orig_day_of_week', '_orig_day_of_month', '_orig_month_of_year']
        cron_str = ''
        for field in fields:
            cron_str += getattr(lottery_task.schedule, field) + ' '
        cron_str = cron_str[:-1]
    else:
        cron_str = '* 22 * * *'
    return cron_str
