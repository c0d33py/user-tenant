# Create Public Tenant #
#### 1. Creating Public Tenant (The main schema of your project)

tenant_users has method for this, but it doesn't give any access for admin user of public tenant. I recommend read `create_public_tenant`'s inside.

```python
# import form custom file
from server.init_tenant import create_public_tenant

create_public_tenant("localhost", "admin@test.com", "testing123@")
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
2. User custom method.
3. Need to define custom middleware for checking the tenancy permission of requested user
4. Check domain.tenant is == request.user