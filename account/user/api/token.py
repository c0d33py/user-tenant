import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken


class TokenGenerator(PasswordResetTokenGenerator):
    '''
    Token Generator
    We have to create token that will use in email confirmation url.
    '''

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_verified)
        )


account_activation_token = TokenGenerator()


def get_tokens_for_user(user):
    '''Creating tokens manually'''
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
