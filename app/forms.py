from flask_wtf import Form
from wtforms import StringField, BooleanField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, InputRequired, Optional
from app.models import User

class AddUserForm(Form):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=120)], render_kw={"placeholder": "Username (email)"})
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=120)], render_kw={"placeholder": "Full Name"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=120)], render_kw={"placeholder": "Password"})
    role = IntegerField('role', validators=[InputRequired()], render_kw={"placeholder": "Role"})

    def validate(self):
        if not Form.validate(self):
            return False
        return True

class EditUserForm(Form):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=120)], render_kw={"placeholder": "Username (email)"})
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=120)], render_kw={"placeholder": "Full Name"})
    password = PasswordField('password', validators=[Optional(), Length(min=4, max=120)], render_kw={"placeholder": "Password"})
    role = IntegerField('role', validators=[InputRequired()], render_kw={"placeholder": "Role"})

    def __init__(self, o_usermame, o_name, o_password, o_role, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.o_usermame = o_usermame
        self.o_name = o_name
        self.o_password = o_password
        self.o_role = o_role

    def validate(self):
        if not Form.validate(self):
            return False
        return True

