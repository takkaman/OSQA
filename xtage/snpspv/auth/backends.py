
from django.conf import settings
#from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from forum.models import User
from forum.actions import UserJoinsAction

import logging

class SNPSPVBackend(ModelBackend):
    def authenticate(self, remote_user=None, password=None):
        if not remote_user:
            return

        username = remote_user
        service = getattr(settings, 'PAM_SERVICE', 'login')
        #if pam.authenticate(username, password, service=service):
        if True:
            try:
                user = User.objects.get(username=username)
            except:
                user = User(username=username, password='not stored here')
                user.set_unusable_password()

                user.email = '%s@synopsys.com' % username
                user.email_isvalid = True

                if getattr(settings, 'PAM_IS_SUPERUSER', False):
                  user.is_superuser = True

                if getattr(settings, 'PAM_IS_STAFF', user.is_superuser):
                  user.is_staff = True

                user.save()
                UserJoinsAction(user=user).save()

	    #user.is_superuser = True
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
