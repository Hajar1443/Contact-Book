from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os 

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class ContactModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    number = db.Column(db.String(20))

    def __repr__(self):
        return self.id

class ContactSchema(ma.Schema):
  class Meta:
    fields = ('id','name', 'email', 'number')

contact_schema = ContactSchema(many=False)
contacts_schema = ContactSchema(many=True)

@app.route('/contact', methods=['POST'])
def add_contact():
  
    try:
        name = request.json['name']
        email = request.json['email']
        number = request.json['number']
  
        new_contact = ContactModel(name = name, email = email, number = number)
     
        db.session.add(new_contact)
        db.session.commit()

        return contact_schema.jsonify(new_contact)

    except Exception as e:
        return jsonify({"Error" : "Invalid request."})

@app.route("/contact", methods = ["GET"])
def get_contacts():
  contacts = ContactModel.query.all()
  result_set = contacts_schema.dump(contacts)
  return jsonify(result_set)

@app.route("/contact/<int:id>", methods = ["GET"])
def get_contact(id):
    contact = ContactModel.query.get_or_404(int(id))
    return contact_schema.jsonify(contact)

@app.route("/contact/<int:id>", methods = ["PUT"])
def update_contact(id):
  contact = ContactModel.query.get_or_404(int(id))

  name = request.json['name']
  email = request.json['email']
  number = request.json['number']

  contact.name = name
  contact.email = email 
  contact.number = number 

  db.session.commit()

  return contact_schema.jsonify(contact)

@app.route("/contact/<int:id>", methods = ["DELETE"])
def delete_contact(id):
  contact = ContactModel.query.get_or_404(int(id))
  db.session.delete(contact)
  db.session.commit()
  return jsonify({'Success' : 'Contact deleted.'})

if __name__ == '__main__':
  app.run(debug=True)