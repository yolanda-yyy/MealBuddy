from database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    meals_created = db.relationship('MealEvent', backref='creator', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    joined_meals = db.relationship('MealParticipant', backref='participant', lazy=True)

class MealEvent(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    restaurant = db.Column(db.String(100))
    time = db.Column(db.String(100))  # 你可以日后改成 DateTime
    max_people = db.Column(db.Integer)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    participants = db.relationship('MealParticipant', backref='meal', lazy=True)
    comments = db.relationship('Comment', backref='meal', lazy=True)

class MealParticipant(db.Model):
    __tablename__ = 'meal_participants'

    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
