from random import randint
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
from django.contrib.auth.models import User
from django.db.models.aggregates import Count

from users.models import Profile


@shared_task
def choose_winner():
    count = User.objects.aggregate(count=Count('id'))['count']
    random_index = randint(0, count - 1)
    user = User.objects.all()[random_index]
    profile = Profile.objects.get(user=user)
    profile.balance += 1
    profile.save()

    channel_layer = get_channel_layer()
    data = json.dumps({'balance': profile.balance, 'show_messages': profile.show_messages})
    async_to_sync(channel_layer.group_send)(
        'render_updates_group',
        {'type': 'render', 'data': data, 'id': profile.id}
    )
    # return user
