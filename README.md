# Create Public Tenant #
#### 1. Creating Public Tenant (The main schema of your project)
before creating initial tenant
```python
python manage.py migrate_schemas --shared
```

tenant_users has method for this, but it doesn't give any access for admin user of public tenant. I recommend read `create_public_tenant`'s inside.
after domain you need to add username

```python
# import form custom file
from server.init_tenant import create_public_tenant

create_public_tenant("localhost","admin", "admin@test.com", "testing123@")
```

#### 2. Creating New Tenant (***peramiters***)

1. Tenant Name
2. Tenant schema name
3. Exiting Email address 

````python
from tenant_users.tenants.tasks import provision_tenant

fqdn = provision_tenant("Name", "schema", "admin@mytenant.com", True)
# Return FQDN (Fully Qualified Domain Name | eg: mytenant.example.com)
````

## Todo ##

1. Authenticate users by username
2. show tenant members images
3. Get daily visitors detail of each tenant
4. owner it'self in members list
5. if user want to change the tenant ownership. ownership switching take some while.
5. if user want to delete the tenant after the conformation celery as a service run in backgound and create a demo user without set passwd & that user take the tenant ownership and then request to database for delete the tenant. 
