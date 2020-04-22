import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS


from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()


# ROUTES
@app.route('/')
def index():
    return jsonify({
        'success':True
    })
@app.route('/drinks')
def view_drink():
    selection = Drink.query.all()

    if selection is None:
        abort(404)

    drinks = [drink.short() for drink in selection]
    return jsonify({
        'success': True,
        'drinks': drinks
    })


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def view_drink_detail(payload):
    selection = Drink.query.all()

    if selection is None:
        abort(404)

    drinks = [drink.long() for drink in selection]
    return jsonify({
        'success': True,
        'drinks': drinks
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    body = request.get_json()
    title = body.get('title')
    recipe = body.get('recipe')

    try:
        new_drink = Drink(title=title, recipe=json.dumps([recipe]))

        db.session.add(new_drink)
        db.session.commit()

        return jsonify({
            'success': True,
            'drinks': [new_drink.long()]
        })
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def modify_drinks(payload, drink_id):
    body = request.get_json()

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if not drink:
            abort(404)

        if 'title' in body:
            drink.title = body.get('title')

        if 'recipe' in body:
            drink.recipe = json.dumps(body.get('recipe'))

        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })

    except Exception:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if not drink:
            abort(404)

        db.session.delete(drink)
        db.session.commit()

        return jsonify({
            'success': True,
            'delete': drink.id
        })
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


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


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'code': error.status_code,
        'description': error.error['description']
    }), error.status_code
