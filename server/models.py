from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def check_name(self, key, name):
        if not name:
            raise ValueError('Name must not be null.')
        elif self.query.filter_by(name=name).first():
            raise ValueError(f"Name must be unique. {name} already exists.")
        return name
    
    @validates('phone_number')
    def check_number(self, key, number):
        if not number.isdigit() or len(number) != 10:
            raise ValueError('Phone number must be 10 digits.')
        return number
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def check_content(self, key, content):
        if len(content) >= 250:
            return content
        else:
            raise ValueError('Content must be at least 250 characters.')
        
    @validates('summary')
    def check_summary(self, key, summary):
        if len(summary) <= 250:
            return summary
        else:
            raise ValueError('Summary should not exceed 250 characters.')
        
    @validates('category')
    def check_category(self, key, category):
        if category == 'Fiction' or category == 'Non-Fiction':
            return category
        else:
            raise ValueError('Category must be Fiction or Non-Fiction.')

    @validates('title')
    def check_title(self, key, title):
        words = ["Won't Believe", "Secret", "Top", "Guess"]
        for w in words:
            if w in title:
                return title
        else:
            raise ValueError('Not clickbait enough.')
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
