import os
from flask import Flask, jsonify, request, render_template
from models import db, seed_data, User, Document
from auth import init_jwt, jwt_required, create_access_token_local, current_user, init_google

app = Flask(__name__, template_folder='templates')
app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'devsecret'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///alp.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'jwt-secret'),
)

# Initialize extensions
db.init_app(app)
init_jwt(app)
google_bp = init_google(app)
app.register_blueprint(google_bp, url_prefix='/auth')

# Setup database using app context (Flask 3.x compatible)
with app.app_context():
    db.create_all()
    seed_data(db)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def ui_login():
    return render_template('login.html')

# JWT login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg': 'username and password required'}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'invalid credentials'}), 401
    access_token = create_access_token_local(identity=user.id)
    return jsonify({'access_token': access_token, 'user': user.to_dict()})

# List documents (RBAC)
@app.route('/api/documents', methods=['GET'])
@jwt_required()
def list_documents():
    user = current_user()
    if user.role == 'admin':
        docs = Document.query.all()
    elif user.role == 'manager':
        docs = Document.query.filter_by(department=user.department).all()
    else:
        docs = Document.query.filter_by(owner_id=user.id).all()
    return jsonify([d.to_dict() for d in docs])

# Create document (ABAC)
@app.route('/api/documents', methods=['POST'])
@jwt_required()
def create_document():
    user = current_user()
    payload = request.json or {}
    title = payload.get('title')
    content = payload.get('content', '')
    department = payload.get('department', user.department)
    premium = payload.get('premium', False)

    if premium and not user.subscription_active:
        return jsonify({'msg': 'subscription required for premium content'}), 403

    if department != user.department and user.role != 'admin':
        return jsonify({'msg': 'cannot create docs for other departments'}), 403

    doc = Document(title=title, content=content, owner_id=user.id, department=department, premium=premium)
    db.session.add(doc)
    db.session.commit()
    return jsonify(doc.to_dict()), 201

# Delete document (RBAC + ABAC)
@app.route('/api/documents/<int:doc_id>', methods=['DELETE'])
@jwt_required()
def delete_document(doc_id):
    user = current_user()
    doc = Document.query.get_or_404(doc_id)

    if user.role == 'admin':
        allowed = True
    elif user.role == 'manager' and user.department == doc.department:
        allowed = True
    elif user.id == doc.owner_id:
        allowed = True
    else:
        allowed = False

    if not allowed:
        return jsonify({'msg': 'forbidden'}), 403

    if doc.premium and user.role != 'admin':
        return jsonify({'msg': 'only admin can delete premium documents'}), 403

    db.session.delete(doc)
    db.session.commit()
    return jsonify({'msg': 'deleted'})

if __name__ == '__main__':
    app.run(debug=True)
