from os import name
from typing import Dict, List
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __init__(self, title:str, description:str, status:str, project_id:int) -> None:
        self.title = title
        self.description = description
        self.status = status
        self.project_id = project_id

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    issues = db.relationship('Issue', backref='project', lazy=True)

    def __init__(self,name:str, description:str,issues:List[Issue]) -> None:
        self.name = name
        self.description = description
        self.issues = issues

