from flask import current_app
from app.models.exception_model import IdNotFoundError


def retrieve(model):
    session = current_app.db.session

    response = session.query(model).all()

    return response


def register(record):
    session = current_app.db.session

    session.add(record)
    session.commit()


def retrieve_by_id(model, id):
    session = current_app.db.session
    record = session.query(model).filter_by(id=id).first()

    if not record:
        raise IdNotFoundError()

    return record


def delete(record):
    session = current_app.db.session

    session.delete(record)
    session.commit()
