import sqlalchemy
from data.db_session import SqlAlchemyBase, orm
from flask_login import UserMixin
import sqlalchemy_serializer as sr
import werkzeug


class Teacher(SqlAlchemyBase, UserMixin, sr.SerializerMixin):
    __tablename__ = 'teachers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_password(self, password):
        self.hashed_password = werkzeug.security.generate_password_hash(password)

    def check_password(self, password):
        return werkzeug.security.check_password_hash(self.hashed_password, password)