from application import db


class Postit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    note = db.Column(db.Text)
    uuid = db.Column(db.String)


class Users(db.Model):
    tableid = db.Column(db.Integer, primary_key=True)
    cookieid = db.Column(db.String)