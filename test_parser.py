from flask_restful import reqparse


parser_test = reqparse.RequestParser()
parser_test.add_argument('name', required=True)
parser_test.add_argument('subject', required=True)
parser_test.add_argument('group', required=True)
parser_test.add_argument('teacher_name', required=False)
parser_test.add_argument('questions', location='json')
