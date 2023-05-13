from flask import Flask, render_template, url_for, redirect, request, flash, session, abort,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = '123456789'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    quadrant = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('You are now logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    print('index starting')
    print(request.method)
    if current_user.is_authenticated:
        tasks_q1 = [task for task in current_user.tasks if task.quadrant == 1]
        tasks_q2 = [task for task in current_user.tasks if task.quadrant == 2]
        tasks_q3 = [task for task in current_user.tasks if task.quadrant == 3]
        tasks_q4 = [task for task in current_user.tasks if task.quadrant == 4]
        if request.method == 'POST':
            task_description = request.form['description']
            task_quadrant = int(request.form['quadrant'])
            task = Task(description=task_description, quadrant=task_quadrant, user=current_user)
            db.session.add(task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            for task in current_user.tasks:
                print(f'Task ID: {task.id}, Description: {task.description}, Quadrant: {task.quadrant}')
            return redirect(url_for('index'))
        return render_template('index.html', tasks_q1=tasks_q1, tasks_q2=tasks_q2, tasks_q3=tasks_q3, tasks_q4=tasks_q4)
    else:
        return redirect(url_for('login'))


@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted!', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login')) 
    return render_template('register.html')


@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    tasks_list = []
    for task in tasks:
        tasks_list.append({'description': task.description, 'quadrant': task.quadrant})
    return jsonify({'tasks': tasks_list})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
