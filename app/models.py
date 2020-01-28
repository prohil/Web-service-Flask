from datetime import datetime
from app import db

site_classes = db.Table('site_classes',
                        db.Column('site_id', db.Integer, db.ForeignKey('site.id'), primary_key=True),
                        db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True))
#site: Id, title
#classes: Id, title
#site_classes: site_id, class_id

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    sites = db.relationship('Site', secondary=site_classes, backref=db.backref('classes', lazy='subquery'))

    def __repr__(self):
        return '{}'.format(self.title)

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '{}'.format(self.title)



