from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.user.tasks import send_email_task

User = get_user_model()


def send_activation_email(user, request):
    ''' function to send email verification email '''
    token = PasswordResetTokenGenerator().make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    domain = request.META['HTTP_HOST']
    link = reverse('email-verify', kwargs={'uidb64': uidb64, 'token': token})
    verify_url = 'http://' + domain + link
    email_subject = 'Verify your email'
    email_body = None
    context = {'link': verify_url}
    template = get_template('common/activate_account.html').render(context)
    send_email_task.delay(email_subject, email_body, settings.EMAIL_HOST_USER, user.email, template)  # type: ignore # noqa


def send_reset_password_email(user, request):
    ''' function to send reset password email '''
    token = PasswordResetTokenGenerator().make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    domain = request.META['HTTP_HOST']
    link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
    reset_url = 'http://' + domain + link
    email_subject = 'Reset your password'
    email_body = None
    context = {'reset_url': reset_url}
    template = get_template('common/password_reset.html').render(context)
    send_email_task.delay(email_subject, email_body, settings.EMAIL_HOST_USER, user.email, template)  # type: ignore # noqa


''' start celery worker '''
# celery -A server worker -l info

''' start celery beat '''
# celery -A server beat -l info -S django -E

''' start celery flower '''
# celery -A server flower

''' start celery worker and beat '''
# celery -A server worker -B -l info -E -f logs/celery.log


''' start celery worker and beat and flower '''
# celery -A server worker -B -l info -f logs/celery.log -E


''' Enable -E to monitor tasks in this worker'''
# celery -A server worker -B -l info -f logs/celery.log -E
