from flask import Flask, request, jsonify
from database import db
from models import User, MealEvent, MealParticipant, Comment

app = Flask(__name__)

# 配置 PostgreSQL 数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:116096@localhost/meetbuddy_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 添加一个简单的测试路由
@app.route('/')
def index():
    return '🎉 MealBuddy backend is running!'


#用户注册
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # 先检查用户是否已存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

#用户登录
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'message': 'Login successful', 'user_id': user.id})
    return jsonify({'message': 'Invalid credentials'}), 401

#创建饭搭子活动
@app.route('/create_meal', methods=['POST'])
def create_meal():
    data = request.get_json()
    new_meal = MealEvent(
        title=data.get('title'),
        description=data.get('description'),
        restaurant=data.get('restaurant'),
        time=data.get('time'),
        max_people=data.get('max_people'),
        creator_id=data.get('creator_id')
    )
    db.session.add(new_meal)
    db.session.commit()
    return jsonify({'message': 'Meal event created', 'meal_id': new_meal.id})

#报名参加活动
@app.route('/join_meal', methods=['POST'])
def join_meal():
    data = request.get_json()
    new_participant = MealParticipant(
        meal_id=data.get('meal_id'),
        user_id=data.get('user_id')
    )
    db.session.add(new_participant)
    db.session.commit()
    return jsonify({'message': 'Joined meal successfully'})

#查看所有活动
@app.route('/meals', methods=['GET'])
def get_meals():
    meals = MealEvent.query.all()
    result = []
    for meal in meals:
        result.append({
            'id': meal.id,
            'title': meal.title,
            'description': meal.description,
            'restaurant': meal.restaurant,
            'time': meal.time,
            'max_people': meal.max_people,
            'creator_id': meal.creator_id
        })
    return jsonify(result)

#发表评论
@app.route('/comment', methods=['POST'])
def comment():
    data = request.get_json()
    new_comment = Comment(
        user_id=data.get('user_id'),
        meal_id=data.get('meal_id'),
        content=data.get('content')
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment added'})




# 启动 Flask 应用
if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(debug=True, port=5001)
