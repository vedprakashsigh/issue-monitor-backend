from flask_jwt_extended import get_jwt_identity
from sqlalchemy import event
from sqlalchemy.orm import Session
from app.models import Log, db, User, Project, Issue, Comment


def after_insert_listener(mapper, connection, target):
    username = get_jwt_identity()["username"]
    user = User.query.filter_by(username=username).first()
    if not user:
        return
    user_id = user.id
    action = f"Inserted {target.__tablename__} with ID {target.id}"
    log = Log(user_id=user_id, action=action)
    with Session(connection) as session:
        session.add(log)
        session.commit()


def after_update_listener(mapper, connection, target):
    username = get_jwt_identity()["username"]
    user = User.query.filter_by(username=username).first()
    if not user:
        return
    user_id = user.id
    print(user_id)
    action = f"Updated {target.__tablename__} with ID {target.id}"
    log = Log(user_id=user_id, action=action)
    with Session(connection) as session:
        session.add(log)
        session.commit()


def after_delete_listener(mapper, connection, target):
    username = get_jwt_identity()["username"]
    user = User.query.filter_by(username=username).first()
    if not user:
        return
    user_id = user.id
    action = f"Deleted {target.__tablename__} with ID {target.id}"
    log = Log(user_id=user_id, action=action)
    with Session(connection) as session:
        session.add(log)
        session.commit()


event.listen(User, "after_insert", after_insert_listener)
event.listen(User, "after_update", after_update_listener)
event.listen(User, "after_delete", after_delete_listener)

event.listen(Project, "after_insert", after_insert_listener)
event.listen(Project, "after_update", after_update_listener)
event.listen(Project, "after_delete", after_delete_listener)

event.listen(Issue, "after_insert", after_insert_listener)
event.listen(Issue, "after_update", after_update_listener)
event.listen(Issue, "after_delete", after_delete_listener)

event.listen(Comment, "after_insert", after_insert_listener)
event.listen(Comment, "after_update", after_update_listener)
event.listen(Comment, "after_delete", after_delete_listener)
