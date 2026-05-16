from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Article, Blog, Story, Book, Chapter, Question, Course
import os
from datetime import datetime
import markdown
import pandas as pd
from io import StringIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kushwaha_user:kushwaha123@localhost:5432/kushwaha_academy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Handle profile image
        profile_img = 'default.png'
        if 'profile_img' in request.files:
            file = request.files['profile_img']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_img = filename
        
        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, profile_img=profile_img, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Article routes
@app.route('/articles')
def articles():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    language = request.args.get('language', 'all')
    
    query = Article.query
    if category != 'all':
        query = query.filter_by(category=category)
    if language != 'all':
        query = query.filter_by(language=language)
    
    articles = query.order_by(Article.created_at.desc()).paginate(page=page, per_page=10)
    categories = ['finance', 'tech', 'education', 'AI', 'other']
    languages = ['hindi', 'english']
    
    return render_template('articles.html', articles=articles, categories=categories, 
                         languages=languages, current_category=category, current_language=language)

@app.route('/article/<int:id>')
def article_detail(id):
    article = Article.query.get_or_404(id)
    article.html_content = markdown.markdown(article.content)
    return render_template('article_detail.html', article=article)

# Blog routes
@app.route('/blogs')
def blogs():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    language = request.args.get('language', 'all')
    
    query = Blog.query
    if category != 'all':
        query = query.filter_by(category=category)
    if language != 'all':
        query = query.filter_by(language=language)
    
    blogs = query.order_by(Blog.created_at.desc()).paginate(page=page, per_page=10)
    categories = ['finance', 'tech', 'education', 'AI', 'other']
    languages = ['hindi', 'english']
    
    return render_template('blogs.html', blogs=blogs, categories=categories,
                         languages=languages, current_category=category, current_language=language)

@app.route('/blog/<int:id>')
def blog_detail(id):
    blog = Blog.query.get_or_404(id)
    blog.html_content = markdown.markdown(blog.content)
    return render_template('blog_detail.html', blog=blog)

# Story routes
@app.route('/stories')
def stories():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    language = request.args.get('language', 'all')
    
    query = Story.query
    if category != 'all':
        query = query.filter_by(category=category)
    if language != 'all':
        query = query.filter_by(language=language)
    
    stories = query.order_by(Story.created_at.desc()).paginate(page=page, per_page=10)
    categories = ['finance', 'tech', 'education', 'AI', 'other']
    languages = ['hindi', 'english']
    
    return render_template('stories.html', stories=stories, categories=categories,
                         languages=languages, current_category=category, current_language=language)

@app.route('/story/<int:id>')
def story_detail(id):
    story = Story.query.get_or_404(id)
    story.html_content = markdown.markdown(story.content)
    return render_template('story_detail.html', story=story)

# NISM Mock Test routes
@app.route('/nism')
def nism_home():
    books = Book.query.all()
    return render_template('nism_home.html', books=books)

@app.route('/nism/book/<int:book_id>')
def nism_chapters(book_id):
    book = Book.query.get_or_404(book_id)
    chapters = Chapter.query.filter_by(book_id=book_id).all()
    return render_template('nism_chapters.html', book=book, chapters=chapters)

@app.route('/nism/chapter/<int:chapter_id>')
def nism_test(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    questions = Question.query.filter_by(chapter_id=chapter_id).all()
    return render_template('nism_test.html', chapter=chapter, questions=questions)

@app.route('/submit_test/<int:chapter_id>', methods=['POST'])
def submit_test(chapter_id):
    questions = Question.query.filter_by(chapter_id=chapter_id).all()
    score = 0
    total = len(questions)
    
    for question in questions:
        user_answer = request.form.get(f'question_{question.id}')
        if user_answer and user_answer.upper() == question.correct_answer:
            score += 1
    
    percentage = (score / total) * 100 if total > 0 else 0
    flash(f'Your score: {score}/{total} ({percentage:.1f}%)', 'info')
    return redirect(url_for('nism_chapters', book_id=questions[0].chapter.book_id if questions else 0))

# Courses routes
@app.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)