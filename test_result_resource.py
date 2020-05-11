import json

from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.test import Test
from data.test_question import TestQuestion
from data.test_option import TestOption
from test_parser import parser_test
from data.user import User
from data.test_result import TestResult
from test_resaults_parser import parser_test_results


class TestResultsResource(Resource):
    def get(self, test_result_id):
        abort_if_test_not_found(test_result_id)
        session = db_session.create_session()
        test_result = session.query(TestResult).get(test_result_id)
        return jsonify({'test_result': test_result.to_dict(
            only=('id', 'test_id', 'test.name', 'student_id', 'student.name', 'score'))})

    def delete(self, test_result_id):
        abort_if_test_not_found(test_result_id)
        session = db_session.create_session()
        test_result = session.query(TestResult).get(test_result_id)
        session.delete(test_result)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, test_result_id):
        abort_if_test_not_found(test_result_id)
        session = db_session.create_session()
        test_result = session.query(TestResult).get(test_result_id)
        args = parser_test_results.parse_args()
        test_result.score = args['score']
        session.commit()
        return jsonify({'success': 'OK'})


class TestResultsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        test_results = session.query(TestResult).all()
        return jsonify({'test_results': [item.to_dict(
            only=('id', 'test_id', 'test.name', 'student_id', 'student.name', 'score')) for item in test_results]})

    def post(self):
        args = parser_test_results.parse_args()
        session = db_session.create_session()
        test_results = TestResult(
            test_id=args['test_id'],
            student_id=args['student_id'],
            score=args['score'],
        )
        session.add(test_results)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_test_not_found(test_result_id):
    session = db_session.create_session()
    test_result = session.query(TestResult).get(test_result_id)
    if not test_result:
        abort(404, message=f"Test result {test_result_id} not found")