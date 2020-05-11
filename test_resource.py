import json

from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.test import Test
from data.test_question import TestQuestion
from data.test_option import TestOption
from test_parser import parser_test
from data.user import User


class TestResource(Resource):
    def get(self, test_id):
        abort_if_test_not_found(test_id)
        session = db_session.create_session()
        test = session.query(Test).get(test_id)
        return jsonify({'test': test.to_dict(
            only=('id', 'name', 'subject', 'teacher', 'group', 'questions.id', 'questions.question_text',
                  'questions.score', '-questions.options.question_id', 'questions.options.id',
                  'questions.options.text', 'questions.options.is_correct'))})

    def delete(self, test_id):
        abort_if_test_not_found(test_id)
        session = db_session.create_session()
        test = session.query(Test).get(test_id)
        session.delete(test)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, test_id):
        print(test_id)
        abort_if_test_not_found(test_id)
        session = db_session.create_session()
        test = session.query(Test).get(test_id)
        args = parser_test.parse_args()
        # ищем teacher_id по teacher_name из запроса
        teacher = session.query(User).filter(User.name == args['teacher_name']).first()
        if not teacher:
            abort(404, message=f"Teacher {args['teacher_name']} not found")
        test.name = args['name']
        test.subject = args['subject']
        test.group = args['group']
        test.teacher_id = teacher.id
        q_str = str(args['questions']).replace(":true", ":\"True\"").replace(":false", ":\"False\"").\
            replace(":True", ":\"True\"").replace(":False", ":\"False\"").replace(": true", ": \"True\"").\
            replace(": false", ": \"False\"").replace(": True", ": \"True\"").replace(": False", ": \"False\"").\
            replace('\'', '\"')
        print(q_str)
        questions = json.loads(q_str)
        ids = dict(map(lambda x: (x.get("id"), x), questions))
        db_questions = session.query(TestQuestion).filter(TestQuestion.id.in_(ids.keys())).all()
        for item in db_questions:
            source_item = ids[item.id]
            item.question_text = source_item['question_text']
            item.score = source_item['score']
            item.options.clear()
            for option_item in source_item["options"]:
                option = TestOption()
                option.text = option_item['text']
                if option_item['is_correct'].lower() == 'true':
                    option.is_correct = True
                else:
                    option.is_correct = False
                option.question_id = item.id
                item.options.append(option)
        for item in questions:
            if not item.get("id"):
                question = TestQuestion()
                question.question_text = item['question_text']
                question.score = item['score']
                question.test_id = test.id
                test.questions.append(question)
                for option_item in item["options"]:
                    option = TestOption()
                    option.text = option_item['text']
                    if option_item['is_correct'].lower() == 'true':
                        option.is_correct = True
                    else:
                        option.is_correct = False
                    option.question_id = question.id
                    question.options.append(option)
        session.commit()
        return jsonify({'success': 'OK'})


class TestsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        tests = session.query(Test).all()
        return jsonify({'tests': [item.to_dict(
            only=('id', 'name', 'subject', 'teacher', 'group', 'questions.id', 'questions.question_text',
                  'questions.score', '-questions.options.question_id', 'questions.options.id',
                  'questions.options.text', 'questions.options.is_correct')) for item in tests]})

    def post(self):
        args = parser_test.parse_args()
        session = db_session.create_session()
        # ищем teacher_id по teacher_name из запроса
        teacher = session.query(User).filter(User.name == args['teacher_name']).first()
        print(teacher)
        if not teacher:
            abort(404, message=f"Teacher {args['teacher_name']} not found")
        test = Test(
            name=args['name'],
            subject=args['subject'],
            group=args['group'],
            teacher_id=teacher.id
        )
        print(test)
        session.add(test)
        print('$$$')
        q_str = args["questions"]
        if q_str:
            q_str = args["questions"].replace("\'", "\"")
            questions = json.loads(q_str)
            for item in questions["question"]:
                question = TestQuestion()
                question.question_text = item['question_text']
                question.score = item['score']
                question.test_id = test.id
                test.questions.append(question)
                for option_item in item["options"]["option"]:
                    option = TestOption()
                    option.text = option_item['text']
                    if option_item['is_correct'].lower() == 'true':
                        option.is_correct = True
                    else:
                        option.is_correct = False
                    option.question_id = question.id
                    question.options.append(option)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_test_not_found(test_id):
    session = db_session.create_session()
    test = session.query(Test).get(test_id)
    if not test:
        abort(404, message=f"Test {test_id} not found")