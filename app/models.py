from typing import List
from app.extentions import bcrypt, db


class Issue(db.Model):
    __tablename__ = "issue"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    def __init__(
        self, title: str, description: str, status: str, project_id: int
    ) -> None:
        self.title = title
        self.description = description
        self.status = status
        self.project_id = project_id


class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    issues = db.relationship("Issue", backref="project", lazy=True)

    def __init__(
        self, name: str, description: str, issues: List[Issue], user_id: int
    ) -> None:
        self.name = name
        self.description = description
        self.issues = issues
        self.user_id = user_id


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    projects = db.relationship("Project", backref="user", lazy=True)

    def __init__(
        self, name: str, username: str, email: str, projects: List[Project]
    ) -> None:
        self.name = name
        self.username = username
        self.email = email
        self.projects = projects

    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str):
        return bcrypt.check_password_hash(self.password_hash, password)
