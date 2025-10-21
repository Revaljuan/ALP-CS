ALP - Daftar Access Policy

1) Roles:
   - admin: full system access (create/delete any resource, manage users)
   - manager: access to resources within their department; can create non-premium docs
   - user: access to own resources; read department resources if allowed

2) JWT Authentication:
   - /api/login issues JWT with user id as identity; token lifetime default from library

3) Google OAuth2:
   - /auth/login -> Google OAuth flow; on success, local user is created/linked and JWT returned

4) RBAC rules:
   - admin: can list/create/delete all documents
   - manager: list and create documents for own department; delete docs in their department
   - user: list/modify only own documents

5) ABAC rules:
   - premium document access requires subscription_active=True
   - deletion of premium docs allowed only by admin
   - cross-department creation requires admin role

6) Combined RBAC+ABAC:
   - To delete a document: user must be (admin OR manager in same department OR owner) AND if doc.premium then only admin
