import datetime as dt
import sqlalchemy as sql
import sqlalchemy.orm as orm
import passlib.hash as hash
import database as database


class User(database.Base):
    __tablename__ = "users"
    id = sql.Column(sql.Integer, primarykey=True, index=True)
    email = sql.Column(sql.String, unique=True, index=True)
    hashedpassword = sql.Column(sql.String)

    leads = orm.relationship("Lead", backpopulates="owner")

    def verifypassword(self, password: str):
        return hash.bcrypt.verify(password, self.hashedpassword)


class Lead(database.Base):
    __tablename__ = "leads"
    id = sql.Column(sql.Integer, primarykey=True, index=True)
    ownerid = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    firstname = sql.Column(sql.String, index=True)
    lastname = sql.Column(sql.String, index=True)
    email = sql.Column(sql.String, index=True)
    company = sql.Column(sql.String, index=True, default="")
    note = sql.Column(sql.String, default="")
    datecreated = sql.Column(sql.DateTime, default=dt.datetime.utcnow)
    datelastupdated = sql.Column(sql.DateTime, default=dt.datetime.utcnow)

    owner = orm.relationship("User", backpopulates="leads")
