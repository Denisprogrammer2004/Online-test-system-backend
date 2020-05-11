from flask_restful import reqparse


parser_user = reqparse.RequestParser()
parser_user.add_argument('name', required=True)
parser_user.add_argument('email', required=True)
parser_user.add_argument('hashed_password')
parser_user.add_argument('group', required=False)
parser_user.add_argument('is_teacher', required=True)