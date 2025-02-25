from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            flash('Please enter a username')
            return redirect(url_for('auth.login'))
        
        # Get or create user
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('login.html')
