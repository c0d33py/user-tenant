from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission

from account.permissions.models import TenantPermissions


class UserBackend(ModelBackend):
    """
    Authenticates against UserProfile
    Authorizes against the TenantPermissions.
    The Facade classes handle the magic of passing
    requests to the right spot.
    """

    # We override this so that it looks for the 'groups' attribute on the
    # TenantPermissions rather than from get_user_model()
    def _get_group_permissions(self, user_obj):
        user_groups_field = TenantPermissions._meta.get_field('groups')
        user_groups_query = 'group__{0}'.format(
            user_groups_field.related_query_name(),
        )
        return Permission.objects.filter(**{user_groups_query: user_obj})
