from flask import Flask, redirect, url_for, request, flash
from flask_admin import Admin, BaseView, expose
from flask.ext import wtf
from wtforms.fields import TextField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'

user_view = Admin(app, name='User stuff')


class User(object):
    def __init__(self, uid):
        self.uid = uid

    def set(self, **kwargs):
        pass

    def save(self):
        pass


class ProfileForm(wtf.Form):
    username = TextField('Username', [Required()])
    name = TextField('Name', [Required()])


class Profile(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('.profile', uid=10))

    @expose('/<uid>/', methods=('GET', 'POST'))
    def profile(self, uid):
        user = User(uid) # gets the user's data from DB
        form = ProfileForm(request.form, obj=user)
        if form.validate_on_submit():
            data = form.data
            user.set(**data)
            user.save()
            flash("Your profile has been saved")
        else:
            flash("form did not validate on submit")
        return self.render('profile.html', form=form, data=user)

user_view.add_view(Profile(name='Profile', url='profile'))

app.run()