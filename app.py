from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////contacts.db'

db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False)

    def __repr__(self):
        return '<id: %r; name: %r; phone: %r>' % (self.id , self.name ,self.phone)

db.create_all()

@app.route('/myproj/contacts', methods=['GET'])
def get_contacts():
    return jsonify({'Contacts': Contact.query.all().__repr__()})

@app.route('/myproj/contacts', methods=['POST'])
def add_contact():
    to_add = Contact(name = request.get_json()['name'], phone = request.get_json()['phone'])
    db.session.add(to_add)
    db.session.commit()

    return jsonify({'to_add': to_add.__repr__()})

@app.route('/myproj/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    update = Contact.query.get_or_404(id)

    update.name = (request.get_json()).get('name', update.name)
    update.phone = (request.get_json()).get('phone', update.phone)

    db.session.commit()

    return jsonify({'update': update.__repr__()})

@app.route('/myproj/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    db.session.delete(Contact.query.get_or_404(id))
    db.session.commit()

    return jsonify({'result': True})
