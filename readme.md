ALP Sistem Otorisasi - Quick Start

1. Create virtualenv and install:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. (Optional) Set env vars:
   export JWT_SECRET_KEY="your_jwt_secret"
   export SECRET_KEY="your_flask_secret"
   # For Google OAuth:
   export GOOGLE_CLIENT_ID="..."
   export GOOGLE_CLIENT_SECRET="..."

3. Run:
   python app.py
   # or
   FLASK_APP=app.py flask run

4. Test (examples):
   - POST /api/login
     body: {"username":"alice","password":"alicepass"}
   - GET /api/documents
     header: Authorization: Bearer <token>
   - Create doc: POST /api/documents
     body: {"title":"...", "content":"...", "department":"Sales", "premium":false}
   - Google OAuth: visit /auth/login in browser

Seed users (from seed_data):
 - admin / adminpass  (role: admin, dept: IT)
 - manager / managerpass (role: manager, dept: Sales)
 - alice / alicepass (role: user, dept: Sales)
 - bob / bobpass (role: user, dept: IT)
