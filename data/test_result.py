import sqlalchemy
from data.db_session import SqlAlchemyBase, orm
import sqlalchemy_serializer as sr


class TestResult(SqlAlchemyBase, sr.SerializerMixin):
    __tablename__ = 'test_results'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tests.id"))
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    score = sqlalchemy.Column(sqlalchemy.Integer)
    test = orm.relation('Test')
    student = orm.relation('User')
