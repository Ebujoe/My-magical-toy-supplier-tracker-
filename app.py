from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///suppliers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    products = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'products': self.products,
            'created_at': self.created_at.isoformat()
        }

@app.route('/')
def home():
    return jsonify({"message": "🎉 Welcome to Toy Supplier API!", "status": "fun"})

@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([supplier.to_dict() for supplier in suppliers])

@app.route('/api/suppliers', methods=['POST'])
def add_supplier():
    data = request.get_json()
    new_supplier = Supplier(
        name=data.get('name'),
        email=data.get('email'),
        products=data.get('products')
    )
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify({"message": "🎊 New toy supplier added!", "supplier": new_supplier.to_dict()}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("🚀 Toy Store API running at http://localhost:5000")
    app.run(debug=True, port=5000)
