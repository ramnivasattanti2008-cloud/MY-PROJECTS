from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class MessageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')


# Portfolio Data
PROJECTS = [
    {
        'id': 1,
        'title': 'E-Commerce Platform',
        'description': 'Full-stack e-commerce solution with React and Node.js',
        'category': 'Web App',
        'tech': ['React', 'Node.js', 'MongoDB'],
        'image': 'https://picsum.photos/seed/proj1/600/400'
    },
    {
        'id': 2,
        'title': 'Task Management App',
        'description': 'Collaborative task management with real-time updates',
        'category': 'Web App',
        'tech': ['Vue.js', 'Firebase', 'Tailwind'],
        'image': 'https://picsum.photos/seed/proj2/600/400'
    },
    {
        'id': 3,
        'title': 'Mobile Banking App',
        'description': 'Secure mobile banking with biometric authentication',
        'category': 'Mobile',
        'tech': ['React Native', 'Node.js', 'PostgreSQL'],
        'image': 'https://picsum.photos/seed/proj3/600/400'
    },
    {
        'id': 4,
        'title': 'AI Dashboard',
        'description': 'Analytics dashboard with machine learning insights',
        'category': 'Data',
        'tech': ['Python', 'TensorFlow', 'React'],
        'image': 'https://picsum.photos/seed/proj4/600/400'
    },
    {
        'id': 5,
        'title': 'Social Media Bot',
        'description': 'Automated social media management tool',
        'category': 'Automation',
        'tech': ['Python', 'Discord API', 'Twitter API'],
        'image': 'https://picsum.photos/seed/proj5/600/400'
    },
    {
        'id': 6,
        'title': 'Portfolio Website',
        'description': 'Personal portfolio with 3D animations',
        'category': 'Web App',
        'tech': ['Next.js', 'Three.js', 'Framer'],
        'image': 'https://picsum.photos/seed/proj6/600/400'
    }
]

SKILLS = {
    'Frontend': ['React', 'Vue.js', 'Next.js', 'TypeScript', 'Tailwind CSS'],
    'Backend': ['Node.js', 'Python', 'PostgreSQL', 'MongoDB', 'Redis'],
    'DevOps': ['Docker', 'AWS', 'CI/CD', 'Kubernetes', 'Linux'],
    'Tools': ['Git', 'Figma', 'VS Code', 'Postman', 'Vercel']
}

SKILLS_LEVELS = [
    {'name': 'React / Vue.js', 'level': 95},
    {'name': 'Node.js / Python', 'level': 90},
    {'name': 'TypeScript', 'level': 85},
    {'name': 'PostgreSQL / MongoDB', 'level': 80},
    {'name': 'Docker / AWS', 'level': 75},
    {'name': 'UI/UX Design', 'level': 70}
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html', skills=SKILLS, skills_levels=SKILLS_LEVELS)


@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)


@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = next((p for p in PROJECTS if p['id'] == project_id), None)
    if not project:
        return redirect(url_for('projects'))
    return render_template('project_detail.html', project=project)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Database initialized.')


if __name__ == '__main__':
    app.run(debug=True)
