from django.contrib.auth.models import User
from openid.consumer.consumer import SUCCESS


class GoogleBackend:

    def authenticate(self, openid_response):
        if openid_response is None:
            return None
        if openid_response.status != SUCCESS:
            return None
        google_email = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.email')
        google_firstname = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.firstname')
        google_lastname = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.lastname')
        try:
            user = User.objects.get(username=google_email)
        except User.DoesNotExist:
            new_user = User(first_name=google_firstname, last_name=google_lastname, username=google_email, email=google_email)
            new_user.save()
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
