from flask_restful import reqparse


parser_test_results = reqparse.RequestParser()
parser_test_results.add_argument('test_id', required=True)
parser_test_results.add_argument('student_id', required=True)
parser_test_results.add_argument('score', required=True)
