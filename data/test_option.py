import sqlalchemy
from data.db_session import SqlAlchemyBase, orm
import sqlalchemy_serializer as sr


class TestOption(SqlAlchemyBase, sr.SerializerMixin):
    __tablename__ = 'test_options'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String)
    is_correct = sqlalchemy.Column(sqlalchemy.Boolean)
    question_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("test_questions.id"))
    question = orm.relation('TestQuestion')

