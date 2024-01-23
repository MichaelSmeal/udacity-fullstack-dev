import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from dotenv import load_dotenv

load_dotenv()

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.database_name = os.environ['DATABASE_TEST_NAME']
        self.database_path = "postgres://{}/{}".format(os.environ['DATABASE_PATH'], self.database_name)
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
        
        # setup_db(self.app, self.database_path)

        # binds the app to the current context
        # with self.app.app_context():
            # self.db = SQLAlchemy()
            # self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
      res = self.client().get('/questions')
      data = json.loads(res.data)

      self.assertTrue(data['questions'])
      self.assertTrue(len(data['questions']))
      self.assertTrue(data['categories'])
      self.assertEqual(data['current_category'], '')

    def test_404_get_questions(self):
      res = self.client().get('/questions?page=33')
      data = json.loads(res.data)

      self.assertEqual(data['error'], 422)

    def test_delete_question(self):
      res = self.client().delete('/questions/33')
      data = json.loads(res.data)

      question = Question.query.filter(Question.id==33).one_or_none()

      self.assertEqual(question, None)

    def test_delete_question_400(self):
      res = self.client().delete('/questions/2200')
      data = json.loads(res.data)

      self.assertEqual(data['error'], 400)
    
    def test_get_questions_by_category(self):
      res = self.client().get('/categories/5/questions')
      data = json.loads(res.data)

      questions = Question.query.filter(Question.category=='5').all()

      self.assertEqual(res.status_code, 200)
      self.assertTrue(data['current_category'])
      self.assertTrue(data['questions'])
      self.assertTrue(data['total_questions'])

    def test_get_questions_by_category_422(self):
      res = self.client().get('/categories/55/questions')

      data = json.loads(res.data)

      questions = Question.query.filter(Question.category=='55').all()

      self.assertEqual(data['error'], 422)

    def test_search_term(self):
      res = self.client().post('/search')
      
      search_term = 'title'
      questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()

      formatted_questions = [question.format() for question in questions]

      self.assertTrue(formatted_questions)
    
    def test_search_term_404(self):
      res = self.client().post('/search')

      search_term = 'woo'
      questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()

      formatted_questions = [question.format() for question in questions]

      self.assertEqual(formatted_questions, [])

    def test_add_questions(self):
      res = self.client().post('/questions')

      question = Question(
        question = 'Test new question 33',
        answer = 'Test new answer',
        category = 3,
        difficulty = 3
      )

      Question.insert(question)

      self.assertTrue(question)

    def test_add_questions_400(self):

      passed_data = {
        'question': 'test',
        'answer': 'test',
        'difficulty': '4',
        'category': '3',
      }

      res = self.client().post('/questions', json=json.dumps(passed_data))

      data = json.loads(res.data)

      self.assertEqual(data['error'], 400)

    def test_quizzes(self):

      passed_data = {
        'previous_questions': [],
        'quiz_category': {
          'id': '3'
        }
      }

      res = self.client().post('/quizzes', json=passed_data)

      data = json.loads(res.data)

      self.assertTrue(data['question'])

    def test_quizzes_400(self):
       
      passed_data = {
        'previous_questions': [],
        'quiz_category': {
          'id': ''
        }
      }

      res = self.client().post('/quizzes', json=passed_data)

      data = json.loads(res.data)

      self.assertTrue(data['question'] == '')
       

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
