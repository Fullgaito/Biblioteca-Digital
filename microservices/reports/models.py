from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class reportCache(db.Model):
    __tablename__ = 'report_cache'

    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)
    data = db.Column(db.JSON, nullable=False)