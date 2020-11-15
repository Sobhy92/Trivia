import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def questions_pagination(request, selection):
    page_num = request.args.get('page', '1', type=int)
    start = (page_num - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    if len(questions) >= end:
        my_questions = questions[start:end]
        return my_questions
    else:
        my_questions = questions[start:]
        return my_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample
   route after completing the TODOs
  '''
    CORS(app, resources={'/': {'origins': '*'}})

    '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response

    '''
  @DONE:
  Create an endpoint to handle GET requests
  for all available categories.
  '''

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        selection = Category.query.all()
        if len(selection) == 0:
            abort(404)

        # formatting categories as dictionary -> {key(id) : value(type)}
        categories = {category.id: category.type for category in selection}

        return jsonify({
            'success': True,
            'categories': categories
        })

    '''
  @DONE:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the
   screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        selection = Question.query.all()

        # apply pagination with 10 questions per page
        paginated_questions = questions_pagination(request, selection)
        if len(paginated_questions) == 0:
            abort(404)
        categories = Category.query.all()

        # formatting categories as dictionary -> {key(id) : value(type)}
        all_categories = {category.id: category.type
                          for category in categories}
        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(selection),
            'categories': all_categories,
            'current_category': [question['category']
                                 for question in paginated_questions]
        })

    '''
  @DONE:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question,
   the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        # query the question that we need to delete
        selection = Question.query.filter(Question.id == question_id).\
            one_or_none()
        # abort 404 error if question not found
        if selection is None:
            abort(404)
        try:
            selection.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)

    '''
  @DONE:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

    @app.route("/questions", methods=['POST'])
    def insert_question():
        data = request.get_json()

        # in case POST request cis related to search
        if 'searchTerm' in data.keys():
            search_input = data.get('searchTerm')
            if search_input is None or search_input == '':
                abort(400)
            return search_question(search_input)

        for item in ['question', 'answer', 'difficulty', 'category']:
            if item not in data.keys() or data[item] is None or\
                            data[item] == '':
                abort(400)

        # in case POST request is to add new question
        try:
            question = data.get('question')
            answer = data.get('answer')
            difficulty = data.get('difficulty')
            category = data.get('category')
            my_question = Question(question=question, answer=answer,
                                   difficulty=difficulty, category=category)
            my_question.insert()
            return jsonify({
                'success': True,
                'created': my_question.id
            })
        except:
            abort(422)

    '''
  @DONE:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.
  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

    def search_question(search_input):

        # query all questions that contains the term of search
        selection = Question.query.filter(Question.question.ilike
                                          ("%{}%".format(search_input))).all()
        if len(selection) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': [question.format() for question in selection],
            'total_questions': len(selection),
            'current_category': [question.category for question in selection]
        })

    '''
  @DONE:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def getQuestions_by_category(category_id):
        selection = Question.query.filter(Question.category ==
                                          str(category_id)).all()
        if len(selection) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': [question.format() for question in selection],
            'total_questions': len(selection),
            'current_category': category_id
        })

    '''
  @DONE:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

    @app.route('/quizzes', methods=['POST'])
    def get_random_quiz_question():
        data = request.get_json()
        quiz_questions = []
        category = data.get('quiz_category')
        previous_questions = data.get('previous_questions')
        if (category is None) or (previous_questions is None):
            return abort(400)

        try:
            # query questions in case of all categories or any single category
            selection = Question.query.filter(Question.category ==
                                              category['id']).\
                all() if category['id'] != 0 else Question.query.all()

            # ensure quiz questions list doesn't contain any previous questions
            for question in selection:
                this_question = question.format()
                if this_question['id'] in previous_questions:
                    pass
                else:
                    quiz_questions.append(this_question)

            # get random question of non previous questions
            my_question = random.choice(quiz_questions) \
                if len(quiz_questions) > 0 else None
            return jsonify({
                'success': True,
                'question': my_question
            })
        except:
            abort(422)

    '''
  @DONE:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found!"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error!"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request!"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity!"
        }), 422

    return app
