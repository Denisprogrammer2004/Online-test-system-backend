import sqlalchemy
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase, orm
import sqlalchemy_serializer as sr


class Test(SqlAlchemyBase, sr.SerializerMixin):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    subject = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    group = sqlalchemy.Column(sqlalchemy.String,  nullable=False)
    teacher = orm.relation('User')
    questions = relationship("TestQuestion", back_populates='test', cascade="all, delete, delete-orphan")