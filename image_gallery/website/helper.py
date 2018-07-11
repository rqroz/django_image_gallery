from django.contrib.auth.models import Group

def is_user_a_manager(user):
    return user.groups.filter(name='manager').exists()
