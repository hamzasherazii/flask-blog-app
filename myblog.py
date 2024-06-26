from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.secret_key = '551df092154b9436918adc27021fd868'
bcrypt = Bcrypt()
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog_user:password@localhost/Blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
# Routes remain the same
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('view'))
        else:
            return render_template('index.html', error='Invalid username or password')
    return render_template('index.html')
@app.route('/view')
def view():
    if 'user_id' in session:
        posts = Post.query.all()
        return render_template('view.html', posts=posts)
    else:
        return redirect(url_for('index'))
@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'user_id' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            author_id = session['user_id']
            new_post = Post(title=title, content=content, author_id=author_id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('view'))
        return render_template('create.html')
    else:
        return redirect(url_for('index'))
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)