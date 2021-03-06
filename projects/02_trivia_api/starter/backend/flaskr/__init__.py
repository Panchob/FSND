import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def get_all_categories():
    selection = Category.query.all()
    return {category.id: category.type for category in selection}


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Acces-Control-Allow-Methods',
                             'GET, POST, DELETE')
        return response

    @app.route('/questions')
    def retrieve_questions():
        page = request.args.get('page', 1, type=int)
        categories = get_all_categories()

        try:
            selection = Question.query.order_by(Question.id).\
                        paginate(page, QUESTIONS_PER_PAGE).items
        except:
            abort(404)

        questions = [question.format() for question in selection]
        return jsonify({
            'success': True,
            'questions': questions,
            'currentCategory': 3,
            'categories': categories,
            'totalQuestions': len(Question.query.all())
        })

    @app.route('/categories')
    def retrieve_categories():
        categories = get_all_categories()

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories,
        })

    @app.route('/questions/add', methods=['POST'])
    def create_new_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        try:
            new_question = Question(question, answer, category, difficulty)

            db.session.add(new_question)
            db.session.commit()

            return jsonify({
                'success': True,
                'created': new_question.id
            }), 200
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.\
                       filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            db.session.delete(question)
            db.session.commit()

            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/questions', methods=['POST'])
    def search_questions():
        body = request.get_json()

        searchTerm = body.get("searchTerm", None)
        search_results = Question.query.\
            filter(Question.question.ilike("%{}%".format(searchTerm))).all()
        questions = [question.format() for question in search_results]

        return jsonify({
            'success': True,
            'questions': questions,
            'totalQuestions': len(Question.query.all()),
            'currentCategory': None  # Not used in search
        })

    @app.route('/categories/<category_id>/questions')
    def list_questions_from_category(category_id):

        selection = Question.query.\
            filter(Question.category == category_id).all()
        questions = [question.format() for question in selection]
        category = Category.query.get(category_id)

        if category is None:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'totalQuestions': len(Question.query.all()),
            'currentCategory': category.type
        })

    @app.route('/quiz/play', methods=['POST'])
    def get_questions_for_quiz():
        body = request.get_json()
        category = body.get("quiz_category", None)
        previous_questions = body.get("previous_questions", None)

        if category['id'] == 0:
            selection = db.session.query(Question.id).all()
        else:
            selection = db.session.query(Question.id).\
                filter(Question.category == category['id']).all()

        questions = [i for i, in selection]
        remaining_questions = [question for question in questions
                               if question not in previous_questions]

        # The game is over
        if len(remaining_questions) == 0:
            return jsonify({
                'success': True
            })

        question_id = random.choice(remaining_questions)
        question = Question.query.get(question_id).format()

        return jsonify({
            'success': True,
            'question': question
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "ressource not found"
        }), 404

        @app.errorhandler(422)
        def unprocessable(error):
            return jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }), 422

        @app.errorhandler(400)
        def bad_request(error):
            return jsonify({
                "success": False,
                "error": 400,
                "message": "bad request"
            }), 400

        @app.errorhandler(405)
        def bad_request(error):
            return jsonify({
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }), 405

        @app.errorhandler(500)
        def bad_request(error):
            return jsonify({
                "success": False,
                "error": 500,
                "message": "Internal Server Error"
            }), 500

    return app
