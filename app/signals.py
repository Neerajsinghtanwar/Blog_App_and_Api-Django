from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.cache import cache

@receiver(user_logged_in, sender=User)
def login_success(sender, request, user, **kwargs):
    print("-----------------------------------")
    print("Logged-in Signal..Run Intro")
    
    ip = request.META.get('REMOTE_ADDR')
    print("Client IP:", ip)
    request.session['ip'] = ip

    login_count = cache.get('count', 0, version=user.pk)
    new_count = login_count + 1
    cache.set('count', new_count, 60*60*24, version=user.pk)
