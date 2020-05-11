import sqlalchemy
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase, orm
import sqlalchemy_serializer as sr


class TestQuestion(SqlAlchemyBase, sr.SerializerMixin):
    __tablename__ = 'test_questions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    question_text = sqlalchemy.Column(sqlalchemy.String)
    score = sqlalchemy.Column(sqlalchemy.Integer)
    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tests.id"))
    test = relationship("Test", back_populates="questions")
    options = orm.relation("TestOption", back_populates='question', cascade="all, delete, delete-orphan")
