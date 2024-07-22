import logging
from sqlalchemy.orm import Session
from sqlalchemy import event
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Log, User, Project, Issue, Comment


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_entity_name(session, entity_type, entity_id):
    """
    Fetch the name or relevant details of an entity from the database.

    Args:
        session: SQLAlchemy session.
        entity_type: Type of the entity (e.g., 'project', 'issue', 'comment', 'user').
        entity_id: ID of the entity.

    Returns:
        The name of the entity if found, otherwise 'N/A'.
    """
    model_map = {"project": Project, "issue": Issue, "comment": Comment, "user": User}
    model = model_map.get(entity_type.lower())
    if not model:
        return "N/A"

    entity = session.query(model).filter_by(id=entity_id).first()

    if not entity:
        return "N/A"
    name = getattr(entity, "name", "N/A")
    if name == "N/A":
        name = getattr(entity, "title", "N/A")
    elif name == "N/A":
        name = getattr(entity, "content", "N/A")
    return name


def log_action(mapper, connection, target, action_type):
    """
    General function to log actions (insert, update, delete).

    Args:
        mapper: SQLAlchemy mapper.
        connection: SQLAlchemy connection.
        target: The SQLAlchemy target entity.
        action_type: Type of action ('insert', 'update', 'delete').
    """
    username = get_jwt_identity().get("username")
    user = User.query.filter_by(username=username).first()
    if not user:
        logger.warning(f"User {username} not found for {action_type} action.")
        return

    user_id = user.id
    entity_type = target.__tablename__.lower()
    target_id = target.id

    with Session(connection) as session:
        target_name = fetch_entity_name(session, entity_type, target_id)

    action = f"{action_type.capitalize()}d {entity_type.capitalize()} with ID {target_id} (Name: {target_name}) by {username}"
    logger.info(f"Log entry: {action}")

    log = Log(user_id=user_id, action=action)
    with Session(connection) as session:
        session.add(log)
        session.commit()
    logger.info(
        f"Log entry committed for {entity_type.capitalize()} ID {target_id} (Name: {target_name})."
    )


@jwt_required()
def after_insert_listener(mapper, connection, target):
    log_action(mapper, connection, target, "inserte")


@jwt_required()
def after_update_listener(mapper, connection, target):
    log_action(mapper, connection, target, "update")


@jwt_required()
def after_delete_listener(mapper, connection, target):
    log_action(mapper, connection, target, "delete")


# Event listeners
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
