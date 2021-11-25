# install dependencies
$ pip3 install flask flask-sqlalchemy flask-marshmallow marshmallow

# Create DB
$ python3 
>> from app import db
>> db.create_all()
>> exit()

# Run Server (http://localhst:5000)
$ python3 app.py

# End points 
- POST /contact
- GET /contact
- GET /contact/id
- PUT /contact/id 
- DELETE /contact/id
