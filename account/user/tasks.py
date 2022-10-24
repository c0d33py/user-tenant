import logging
import uuid

import celery
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.core.management import call_command
from django_tenants.utils import (get_public_schema_name,
                                  get_tenant_domain_model, get_tenant_model,
                                  schema_context)

from .models import ExistsError, InactiveError

User = get_user_model()

logger = logging.getLogger(__name__)


class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


def provision_tenant(tenant_name, org, user_id):
    '''Create a tenant with default roles and permissions.

    Returns:
    The FQDN for the tenant.
    '''
    tenant = None

    UserModel = get_user_model()
    TenantModel = get_tenant_model()

    user = UserModel.objects.get(id=user_id)
    if not user.is_active:
        raise InactiveError('Inactive user passed to provision tenant')

    if hasattr(settings, 'TENANT_SUBFOLDER_PREFIX'):
        tenant_domain = tenant_name
    else:
        tenant_domain = '{0}.{1}'.format(tenant_name, settings.TENANT_USERS_DOMAIN)

    DomainModel = get_tenant_domain_model()
    if DomainModel.objects.filter(domain=tenant_domain).exists():
        raise ExistsError('Tenant URL already exists.')

    # Must be valid postgres schema characters see:
    # https://www.postgresql.org/docs/9.2/static/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS
    # We generate unique schema names each time so we can keep tenants around
    # without taking up url/schema namespace.
    gen_uuid = str(uuid.uuid4())[8]
    domain = None

    # noinspection PyBroadException
    try:
        # Wrap it in public schema context so schema consistency is maintained
        # if any error occurs
        with schema_context(get_public_schema_name()):
            tenant = TenantModel.objects.create(
                organization=org,
                name=tenant_name,
                schema_name=gen_uuid,
                owner=user,
                slug=gen_uuid
            )

            # Add one or more domains for the tenant
            domain = get_tenant_domain_model().objects.create(
                domain=gen_uuid,
                tenant=tenant,
                is_primary=True,
            )
            # Add user as a superuser inside the tenant
            tenant.add_user(user, is_superuser=True, is_staff=True)
            logger = logging.getLogger(__name__)
            # it takes a tenant model object as the argument.
            logger.info(f'Set {tenant.schema_name}')
            # The loaddata command take fixture file as a argument
            call_command(
                'loaddata',
                'groups.json',
            )

    except KeyError as e:
        if domain is not None:
            domain.delete()
        if tenant is not None:
            # Flag is set to auto-drop the schema for the tenant
            tenant.delete(True)

    return tenant_domain


@shared_task(bind=True, base=BaseTaskWithRetry)
def send_email_task(self, email_subject, email_body, email_host, to_email, template_name):
    try:

        EmailMultiAlternatives(
            email_subject,
            email_body,
            email_host,
            [to_email, ],
            alternatives=[(template_name, 'text/html')]
        ).send(fail_silently=False)

        logger.info(f'Email has been sent successfully to {to_email}.')
    except BadHeaderError as e:
        raise Exception('exception raised, it would be retry after 5 seconds')
