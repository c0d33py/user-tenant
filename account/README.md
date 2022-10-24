# Migrate and Create the Public Tenant

## Django Tenant User Is A Global Authentication Solution

Tenant_users has method for this, but it doesn't give any access for admin user of public tenant. I recommend read `create_public_tenant`'s inside.
after domain you need to add username Creating Public Tenant (The main schema of your project)

***Before creating initial tenant***

- Tenant domain
- Username
- Password

```python
# Django tenant schemas requires migrate_schemas
python manage.py migrate_schemas --shared

# Create public tenant user.
# import form custom file
from server.init_tenant import create_public_tenant

create_public_tenant('localhost','c0d3', 'test123@')
```

## Provisioning a Tenant

## 1. Creating New Tenant (***peramiters***)

- Tenant name
- Tenant slug
- Orgnization
- Username

```python
from tenant_users.tenants.tasks import provision_tenant

fqdn = provision_tenant('EvilCorp', 'evilcorp', 'org', 'admin')
# Return FQDN (Fully Qualified Domain Name | eg: mytenant.example.com)
```

***tenant_command***

To run any command on an individual schema, you can use the special `tenant_command`, which
creates a wrapper around your command so that it only runs on the schema you specify. For example

``` python
./manage.py tenant_command loaddata
# Also run for (All tenants) 
./manage.py tenant_command all_tenants_command

# The command clone_tenant clones a schema.
./manage.py clone_tenant
```

***rename_schema***

```python
./manage.py rename_schema
```

***create_missing_schemas***

The command create_missing_schemas checks the tenant table against the list of schemas.
If it find a schema that doesn’t exist it will create it.

````python
./manage.py create_missing_schemas
````

## 2. Separate projects for the main website and tenants ***`(optional)`***

If your projects are ran using a `WSGI` configuration, this can be done by
creating a file called `wsgi_main_website.py` [Example][10] in the same folder as wsgi.py.
If you put this in the same Django project, you can make a new `settings_public.py`
which points to a different `urls_public.py`. This has the advantage that you
can use the same apps that you use for your tenant websites.

[10]: https://django-tenants.readthedocs.io/en/latest/install.html?highlight=wsgi_main_website#separate-projects-for-the-main-website-and-tenants-optional

```python
# wsgi_main_website.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings_public')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 3. Useful information

1. Running code across every tenant
2. If you want to run some code on every tenant you can do the following

```python
from django_tenants.utils import tenant_context, get_tenant_model

for tenant in get_tenant_model().objects.all():
    with tenant_context(tenant):
        pass
        # do whatever you want in that tenant
```

## 4. PostGIS

If you want to run [PostGIS][9] add the following to your Django settings file

[9]: https://postgis.net/workshops/postgis-intro/

```python
ORIGINAL_BACKEND = 'django.contrib.gis.db.backends.postgis'
```

## Third Party Apps

- Support for Celery is available at [tenant-schemas-celery][11].

[11]: https://github.com/maciej-gol/tenant-schemas-celery

***Installation***

```shell
pip install tenant-schemas-celery
pip install django-tenants
```

***Usage***

- Define a celery app using given `CeleryApp` class.

``` python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

from django.conf import settings

from tenant_schemas_celery.app import CeleryApp as TenantAwareCeleryApp

app = TenantAwareCeleryApp()
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
```

- Replace your @task decorator with @app.task

```python
from django.db import connection
from myproject.celery import app

@app.task
def my_task():
   print(connection.schema_name)
```

## Signals

## There are number of signals

`post_schema_sync` will get called after a schema gets created from the save method on the tenant class.

`schema_needs_to_be_sync` will get called if the schema needs to be migrated. `auto_create_schema` (on the tenant model) has to be set to False for this signal to get called. This signal is very useful when tenants are created via a background process such as celery.

`schema_migrated` will get called once migrations finish running for a schema.

`schema_migrate_message` will get called after each migration with the message of the migration. This signal is very useful when for process / status bars.

Example

```pyhton
@receiver(schema_needs_to_be_sync, sender=TenantMixin)
def created_user_client_in_background(sender, **kwargs):
    client = kwargs['tenant']
    print ("created_user_client_in_background %s" % client.schema_name)
    from clients.tasks import setup_tenant
    task = setup_tenant.delay(client)
```

```pyhton
@receiver(post_schema_sync, sender=TenantMixin)
def created_user_client(sender, **kwargs):

    client = kwargs['tenant']

    # send email to client to as tenant is ready to use
```

```pyhton
@receiver(schema_migrated, sender=run_migrations)
def handle_schema_migrated(sender, **kwargs):
    schema_name = kwargs['schema_name']

    # recreate materialized views in the schema
```

```pyhton
@receiver(schema_migrate_message, sender=run_migrations)
def handle_schema_migrate_message(**kwargs):
    message = kwargs['message']

    # recreate materialized views in the schema
```
