from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, ValidationError
from pythonic.models import Category, Type, Device

class TypeForm(FlaskForm):
    name = StringField('Type Name', validators=[DataRequired()])
    submit = SubmitField('Add Type')


    

class AddTypeCategoryForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()])
    submit = SubmitField('Add')


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=25)])
    submit = SubmitField('Add')

    def validate_name(self, name):
        category = Category.query.filter_by(name=name.data).first()
        if category:
            raise ValidationError('Category name already exists! Please choose a different one.')


class DeviceForm(FlaskForm):
    name = StringField('Device Name', validators=[DataRequired(), Length(min=2, max=60)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=5, max=500)])
    category = SelectField('Category', validators=[DataRequired()])
    type = SelectField('Type', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_name(self, name):
        device = Device.query.filter_by(name=name.data).first()
        if device:
            raise ValidationError('Device name already exists! Please choose a different one.')
            



class UpdateCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=25)])
    picture = FileField('Update Category picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def __init__(self, category_id, *args, **kwargs):
        super(UpdateCategoryForm, self).__init__(*args, **kwargs)
        self.category_id = category_id 

    def validate_name(self, name):
        category = Category.query.filter_by(name=name.data).first()
        if category and category.id != self.category_id:
            raise ValidationError('Category name already exists! Please choose a different one.')

