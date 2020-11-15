import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".\
            format('postgres', '0000', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation
     and for expected errors.
    """
    def test_retrieve_categories(self):

        # get response and loading data
        res = self.client().get('/categories')
        data = json.loads(res.data.decode('utf-8'))

        # check status code is 200 and success message and categories data
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_404_browse_wrong_categories_route(self):

        # get response and loading data
        res = self.client().get('/categories/12345')
        data = json.loads(res.data.decode('utf-8'))

        # check status code 404 and failure message and success equal to false
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found!')

    def test_retrieve_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check questions , total_questions data
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

        # check categories and current_category
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['current_category'])

    def test_404_requesting_beyond_pages_range(self):

        # make get request with page number out of range
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data.decode('utf-8'))

        # check that status code is 404 and failure message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found!')

    def test_deleting_question(self):

        # create new object of Question class to be inserted and then deleted
        question = Question(question="Where do you live?", answer="Egypt",
                            category="3", difficulty=1)
        question.insert()
        question_id = question.id

        # get count of all questions before deleting the question
        count_before = len(Question.query.all())

        # get response and loading data with deleting question
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data.decode('utf-8'))

        # query question after delete to check it's data later
        question_after_delete = Question.query.\
            filter(Question.id == question_id).one_or_none()

        # get count of all questions after deleting question
        count_after = len(Question.query.all())

        # check status code is 200 and success message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check deleted is the id of deleted question
        self.assertEqual(data['deleted'], question_id)

        # check count of all questions is one less than before deletion
        self.assertEqual(count_after, count_before - 1)

        # check question query is None after deleting it
        self.assertEqual(question_after_delete, None)

    def test_404_deleting_wrong_question(self):
        question_id = 0

        # questions count before deletion
        count_before = len(Question.query.all())
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data.decode('utf-8'))

        # questions count after deletion
        count_after = len(Question.query.all())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found!')

        # check count is the same before and after deletion
        self.assertEqual(count_after, count_before)

    def test_inserting_question(self):

        # create question json to be used in question POST request
        question = {'question': "Where do you live?", 'answer': "Egypt",
                    'category': "3", 'difficulty': 1}
        count_before = len(Question.query.all())
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data.decode('utf-8'))

        # query inserted question from db
        question_after_insertion = Question.query.filter(Question.question ==
                                                         question['question'])
        count_after = len(Question.query.all())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check questions count is increased y 1 after insertion
        self.assertEqual(count_after, count_before + 1)

        # check question is not None
        self.assertNotEqual(question_after_insertion, None)

    def test_400_inserting_missing_question_parts(self):
        count_before = len(Question.query.all())
        res = self.client().post('/questions', json={})
        data = json.loads(res.data.decode('utf-8'))
        count_after = len(Question.query.all())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request!')

        # check questions count didn't change
        self.assertEqual(count_after, count_before)

    def test_search_question(self):

        # create search_term to be used as json
        search_term = {'searchTerm': "Where"}
        res = self.client().post('/questions', json=search_term)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check that search operation return true data
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_search_wrong_question(self):

        # create search_term to be used as json
        search_term = {'searchTerm': "xxxxx"}

        res = self.client().post('/questions', json=search_term)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found!')

    def test_400_search_missing_term(self):

        # create search_term with blank string to be used as json
        search_term = {'searchTerm': ""}

        res = self.client().post('/questions', json=search_term)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request!')

    def test_retrieve_questions_by_category(self):

        # assume category_id =1 to e used in testing
        category_id = 1
        res = self.client().get('/categories/{}/questions'.format(category_id))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check questions and total_questions return data
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

        # check that current_category equal to category id
        self.assertEqual(data['current_category'], category_id)

    def test_404_requesting_questions_of_wrong_category(self):

        # assume category_id = 0(value not found in db) to e used in testing
        category_id = 0
        res = self.client().get('/categories/{}/questions'.format(category_id))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found!')

    def test_get_questions_to_play(self):

        # create my_json to be passed to the client post json
        my_json = {'previous_questions': [],
                   "quiz_category": {'type': 'Science', 'id': '1'}}
        res = self.client().post('/quizzes', json=my_json)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check questions and total_questions return data
        self.assertTrue(data['question'])

    def test_400_get_questions_to_play_missing_json(self):

        # create my_json with missing 'quiz_category' item
        my_json = {'previous_questions': []}
        res = self.client().post('/quizzes', json=my_json)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request!')

    def test_422_get_questions_to_play_wrong_json(self):

        # create my_json with blank 'quiz_category' value
        my_json = {'previous_questions': [], "quiz_category": ""}
        res = self.client().post('/quizzes', json=my_json)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity!')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
