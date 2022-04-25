from http import HTTPStatus

from flask import jsonify
from app.configs.database import db
from app.models.hello_world_model import HelloWorld
from sqlalchemy.exc import ProgrammingError
from psycopg2.errors import UndefinedTable


def hello():
    session = db.session

    try:
        hello = session.query(HelloWorld).get(1)
        
        if not hello:
            new_hello = HelloWorld(greeting="Hello Kenzinho!")
            db.session.add(new_hello)
            db.session.commit()
            return jsonify(new_hello)

        increment_visits = hello.visits + 1
        setattr(hello, "visits", increment_visits)

        db.session.add(hello)
        db.session.commit()

        return jsonify(hello)

    except ProgrammingError as e:
        if isinstance(e.orig, UndefinedTable):
            return {
                "error": "Você não criou as tabelas cara.. volta lá, dá uns 'flask db init' etc que vai dar bom..."
            }
        else:
            return "continua dando erro, agora só Deus na causa..."
