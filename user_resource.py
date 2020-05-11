from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.user import User
from user_parser import parser_user


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'email', 'hashed_password', 'group', 'is_teacher'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        args = parser_user.parse_args()
        user.name = args.get('name')
        user.email = args.get('email')
        user.hashed_password = args.get('hashed_password')
        if args.get('is_teacher').lower() == 'false':
            user.is_teacher = False
        else:
            user.is_teacher = True
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'name', 'email', 'hashed_password', 'group', 'is_teacher')) for item in users]})

    def post(self):
        args = parser_user.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            email=args['email'],
            hashed_password=args.get('hashed_password'),
            group=args['group']
        )
        if args['is_teacher'].lower() == 'false':
            user.is_teacher = False
        else:
            user.is_teacher = True
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")