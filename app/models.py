from typing import List
from app.extentions import bcrypt, db
from datetime import datetime


class Role:
    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    MEMBER = "member"
    DEFAULT_ROLE = MEMBER


class Issue(db.Model):
    __tablename__ = "issue"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"), nullable=False
    )
    comment = db.relationship(
        "Comment", backref="issue", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(
        self, title: str, description: str, status: str, project_id: int
    ) -> None:
        self.title = title
        self.description = description
        self.status = status
        self.project_id = project_id


project_members = db.Table(
    "project_members",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True),
)


class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    issues = db.relationship(
        "Issue", backref="project", lazy=True, cascade="all, delete-orphan"
    )
    members = db.relationship(
        "User",
        secondary=project_members,
        lazy="subquery",
        backref=db.backref("project", lazy=True),
    )

    def __init__(
        self, name: str, description: str, user_id: int, members: List = []
    ) -> None:
        self.name = name
        self.description = description
        self.issues = []
        self.user_id = user_id
        self.members = members


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=Role.DEFAULT_ROLE)
    projects = db.relationship(
        "Project", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    comments = db.relationship(
        "Comment", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    logs = db.relationship(
        "Log", backref="user", lazy=True, cascade="all, delete-orphan"
    )

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


class Log(db.Model):
    __tablename__ = "log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, user_id, action):
        self.user_id = user_id
        self.action = action


class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    issue_id = db.Column(
        db.Integer, db.ForeignKey("issue.id", ondelete="CASCADE"), nullable=False
    )
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, content, user_id, issue_id):
        self.content = content
        self.user_id = user_id
        self.issue_id = issue_id
