from django.contrib.auth.models import Group

"""
    helper.py (Library File)
    This file should contain functions used by many other files.
"""

def is_user_a_manager(user):
    return user.groups.filter(name='manager').exists()
