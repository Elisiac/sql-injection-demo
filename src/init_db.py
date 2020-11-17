#!env/bin/python
from datetime import datetime

from app import db
from app.models import Record, User

# Prepare the statement to create the database
db.create_all()

# Create an admin for our application
admin = User('admin', '<insert-a-secret-password-here>')
db.session.add(admin)

# Note: user_id for Alice is 2
alice = User('alice', '1234')
db.session.add(alice)

# Add a number of records into the database
expenses_alice = [{
    'description': "Logding",
    'date': "2020/09/23",
    "amount": '-1129.99',
    "user_id": 2,
}, {
    'description': "AutoRepair AB",
    'date': "2020/09/24",
    "amount": '-699.90',
    "user_id": 2,
}, {
    'description': "Coop Cofee",
    'date': "2020/09/24",
    "amount": '-29.00',
    "user_id": 2,
}, {
    'description': "Elnetwork",
    'date': "2020/09/24",
    "amount": '-238.45',
    "user_id": 2,
}, {
    'description': "Blocket headphones",
    'date': "2020/09/25",
    "amount": '500',
    "user_id": 2,
}, {
    'description': "ICA Mat",
    'date': "2020/09/25",
    "amount": '-89.90',
    "user_id": 2,
}, {
    'description': "IKEA",
    'date': "2020/09/25",
    "amount": '-3390.45',
    "user_id": 2,
}, {
    'description': "Apotek",
    'date': "2020/09/26",
    "amount": '-36.90',
    "user_id": 2,
}]
for record_data in expenses_alice:
    record = Record(description=record_data['description'],
                    date=datetime.strptime(record_data['date'], "%Y/%m/%d").date(),
                    amount=float(record_data['amount']),
                    user_id=record_data['user_id'])
    db.session.add(record)

# Commit our changes, database is now ready.
db.session.commit()
