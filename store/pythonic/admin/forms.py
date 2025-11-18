from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from pythonic.models import Category, Type

class TypeForm(FlaskForm):
    name = StringField('Type Name', validators=[DataRequired()])
    submit = SubmitField('Add Type')



class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=25)])
    submit = SubmitField('Add')

    def validate_name(seld, name):
        name = Category.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('Category name already exists! Please choose a diffrent one.')
    

class AddTypeCategoryForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()])
    submit = SubmitField('Add')


class DeviceForm(FlaskForm):
    name = StringField('Device Name', validators=[DataRequired(), Length(min=2, max=60)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=5, max=500)])
    category = SelectField('Category', validators=[DataRequired()])
    type = SelectField('Type', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_name(seld, name):
            name = Type.query.filter_by(name=name.data).first()
            if name:
                raise ValidationError('Type name already exists! Please choose a diffrent one.')
            
