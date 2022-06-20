from flask import flash, render_template
from flask_login import current_user, login_required
from app.main import main
from app.models import User
from .forms import EditProfileForm
from app import db

@main.route('/')
@main.route('/home',methods=['GET','POST'])
@login_required
def landing():
    return render_template('landing.html')

#profile pages route
@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(username=username).first_or_404()
    return render_template('user.html',user=user)

@main.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    edit_form=EditProfileForm()
    if edit_form.validate_on_submit():
        current_user.name=edit_form.name.data
        current_user.location=edit_form.location.data
        current_user.about_me=edit_form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('You have successfully edited your profile',category='success')
        return render_template('.user',username=current_user.username)
    edit_form.name.data=current_user.name
    edit_form.location.data=current_user.location
    edit_form.about_me.data=current_user.about_me
    return render_template('edit_profile.html',edit_form=edit_form)