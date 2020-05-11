from flask import Flask
from flask_restful import Api
from data import db_session
from user_resource import UserResource, UsersListResource
from test_resource import TestResource, TestsListResource
from test_result_resource  import TestResultsResource, TestResultsListResource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)


if __name__ == '__main__':
    db_session.global_init("db/school_test.db")
    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:user_id>')
    api.add_resource(TestsListResource, '/api/tests')
    api.add_resource(TestResource, '/api/tests/<int:test_id>')
    api.add_resource(TestResultsListResource, '/api/test_results')
    api.add_resource(TestResultsResource, '/api/test_results/<int:test_result_id>')
    app.debug = True
    app.run(port=8080, host='0.0.0.0')


