from .models import UserAuth

class UserAuthBackend(object):

    def authenticate(self,username=None,password=None):
        try:
            user = UserAuth.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserAuth.DoesNotExist:
            return None

    def get_user(self,user_id):
        try:
            user = UserAuth.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except UserAuth.DoesNotExist:
            return None