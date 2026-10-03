from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    subscription_tier = db.Column(db.String(20), default='free')
    subscription_end = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)


# Forms
class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    agree_terms = BooleanField('I agree to the Terms of Service')
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    company = StringField('Company Name', validators=[Length(max=100)])
    submit = SubmitField('Update Profile')


class PasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


# Routes - Auth
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please sign in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
    return render_template('auth/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Routes - Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'api_calls': 1247,
        'active_projects': 3,
        'storage_used': '2.4 GB',
        'quota_used': 24
    }
    recent_activity = [
        {'type': 'api', 'message': 'API call to /analyze', 'time': '2 min ago'},
        {'type': 'project', 'message': 'New project created', 'time': '1 hour ago'},
        {'type': 'api', 'message': 'API call to /process', 'time': '3 hours ago'},
    ]
    return render_template('dashboard/index.html', stats=stats, activity=recent_activity)


@app.route('/projects')
@login_required
def projects():
    user_projects = [
        {'id': 1, 'name': 'Production App', 'status': 'active', 'calls': 5432},
        {'id': 2, 'name': 'Development', 'status': 'active', 'calls': 1234},
        {'id': 3, 'name': 'Test Environment', 'status': 'paused', 'calls': 456},
    ]
    return render_template('dashboard/projects.html', projects=user_projects)


@app.route('/api-keys')
@login_required
def api_keys():
    user_keys = ApiKey.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/api_keys.html', api_keys=user_keys)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    profile_form = ProfileForm(obj=current_user)
    password_form = PasswordForm()

    if profile_form.submit.data and profile_form.validate():
        current_user.name = profile_form.name.data
        current_user.email = profile_form.email.data
        current_user.company = profile_form.company.data
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('settings'))

    if password_form.submit.data and password_form.validate():
        if current_user.check_password(password_form.current_password.data):
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash('Password changed successfully', 'success')
            return redirect(url_for('settings'))
        flash('Current password is incorrect', 'error')

    return render_template('dashboard/settings.html',
                          profile_form=profile_form,
                          password_form=password_form)


@app.route('/billing')
@login_required
def billing():
    plans = [
        {'id': 'free', 'name': 'Free', 'price': 0, 'features': ['100 API calls/day', '1 project', 'Community support']},
        {'id': 'pro', 'name': 'Pro', 'price': 29, 'features': ['10,000 API calls/day', '10 projects', 'Priority support', 'Advanced analytics']},
        {'id': 'enterprise', 'name': 'Enterprise', 'price': 99, 'features': ['Unlimited calls', 'Unlimited projects', '24/7 support', 'Custom integrations', 'SLA guarantee']},
    ]
    return render_template('dashboard/billing.html', plans=plans, current_plan=current_user.subscription_tier)


@app.route('/documentation')
@login_required
def documentation():
    docs = [
        {'title': 'Getting Started', 'description': 'Learn the basics of our API'},
        {'title': 'Authentication', 'description': 'API keys and authentication'},
        {'title': 'Rate Limits', 'description': 'Understanding usage limits'},
        {'title': 'Code Examples', 'description': 'Integration examples'},
    ]
    return render_template('dashboard/documentation.html', docs=docs)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    # Create demo user
    if not User.query.filter_by(email='demo@example.com').first():
        demo = User(name='Demo User', email='demo@example.com', subscription_tier='pro')
        demo.set_password('password123')
        db.session.add(demo)
        db.session.commit()
        print('Database initialized with demo user: demo@example.com / password123')


if __name__ == '__main__':
    app.run(debug=True)
