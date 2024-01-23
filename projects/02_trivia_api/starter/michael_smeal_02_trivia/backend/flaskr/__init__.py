import random
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, query):
 
  page = request.args.get('page', 1, type=int)

  page_query = query.paginate(page=page, per_page=QUESTIONS_PER_PAGE)

  questions = [question.format() for question in page_query]

  return questions

def format_categories(request):
   
  categories = {}

  for category in request:
    categories[category.id] = category.type

  return categories

def create_app(test_config=None):
  # create and configure the app

  app = Flask(__name__)
  app.secret_key = "super secret key"
  setup_db(app)
  # CORS(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():

    try:

      category_query = Category.query.all()
      categories = format_categories(category_query)

      return jsonify(categories)

    except:

      abort(422)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():

    try:

      questions = paginate_questions(request, Question.query)
      categories = format_categories(Category.query.all())
      
      return jsonify({
        'questions': questions,
        'total_questions': len(questions),
        'categories': categories,
        'current_category': ''
      })

    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):

    try:

      question = Question.query.filter(Question.id==id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        'success': True,
        'deleted': id,
      })
    
    except Exception as error:
      abort(400)

    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_questions():

    data = request.get_json()

    try:

      question_data = {}

      for attr in data:
        if data[attr] != '':
          question_data[attr] = data[attr]

      if len(question_data) == 4:

        question_obj = Question(
          question = question_data['question'],
          answer = question_data['answer'],
          category = question_data['category'],
          difficulty = question_data['difficulty']
        )

        Question.insert(question_obj)

        return jsonify({
          'success': True,
          'question':  question_obj.question,
          'answer':  question_obj.answer,
          'category': question_obj.category,
          'difficulty': question_obj.difficulty,
        })
    
    except Exception as error:
      abort(400)

    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search', methods=['POST'])
  def search_questions():

    data = request.get_json('search_term')

    try:

      questions = paginate_questions(request, Question.query.filter(Question.question.ilike('%' + data['searchTerm'] + '%')))

      return jsonify({
        'search_term': data['searchTerm'],
        'questions': questions,
        'total_questions': len(questions)

      })

    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_by_category(id):

    try:
      category = Category.query.filter(Category.id==id).one_or_none()
      questions = paginate_questions(request, Question.query.filter(Question.category==str(id)))

      return jsonify({
        'questions': questions,
        'total_questions': len(questions),
        'current_category': category.type
      })

    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def quiz():

    data = request.get_json()
    category = data['quiz_category']['id']
    previous_questions = data['previous_questions']

    questions = []
    question = []

    try:

      if len(previous_questions) == 0:

        if category == 0:
          questions = Question.query.all()
        else:
          questions = Question.query.filter(Question.category==category).all()

      else:

        if category == 0:
          questions = Question.query.filter(Question.id.not_in(previous_questions)).all()
        else:
          questions = Question.query.filter(Question.id.not_in(previous_questions)).filter(Question.category==category).all()

      if questions != []:

        random.shuffle(questions)

        question = questions[0]

      # else:

      #   print('no more questions')

      return jsonify({
        'question': '' if question == [] else question.format()
      })
    
    except Exception as error:
      abort(400)

    except:
      abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False, 
      'error': 400,
      'message': 'Bad request'
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False, 
      'error': 404,
      'message': 'Not found'
      }), 404

  @app.errorhandler(415)
  def not_supported(error):
    return jsonify({
      'success': False, 
      'error': 415,
      'message': 'Unsupported media type'
      }), 415

  @app.errorhandler(422)
  def not_processed(error):
    return jsonify({
      'success': False, 
      'error': 422,
      'message': 'Unprocessable'
      }), 422
  
  return app

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
  if __name__ == '__main__':
    app.run()
