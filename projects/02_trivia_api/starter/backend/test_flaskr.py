import os
import unittest
import json
from flask import Flask
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
        self.database_path = "postgres://{}@{}/{}".format('postgres:61785','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question':'What year was the first model of the iPhone released?',
            'answer':'2007',
            'category': 4,
            'difficulty': 1
        }

        self.quiz_data_art = {
            'quiz_category': {
                'id': 2,
                'type': 'Science'
            },
            'previous_questions':[16]
        }

        self.quiz_data_all = {
            'quiz_category': {
                'id': 0,
                'type': 'ALL'
            },
            'previous_questions':[10]
        }
    
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'ressource not found')

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_create_new_question(self):
        res = self.client().post('/add', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
    
    def test_delete_question(self):
        res = self.client().delete('/questions/12')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 12).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 12)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)


    def test_422_question_not_found_for_delete(self):
        res = self.client().delete('/questions/140000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        
    
    def test_search_questions(self):
        res = self.client().post('/questions', json= {'searchTerm':"title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertEqual(len(data['questions']), 2)
    
    def test_list_questions_from_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertEqual(len(data['questions']), 3)
    
    def test_get_questions_for_quiz_with_category(self):
        res = self.client().post('quizzes', json = self.quiz_data_art)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['id'] not in self.quiz_data_art['previous_questions'])

    def test_get_questions_for_quiz_without_category(self):
        res = self.client().post('quizzes', json = self.quiz_data_all)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['id'] not in self.quiz_data_art['previous_questions'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()