from flask import Blueprint, render_template, url_for, flash, redirect, request
from pythonic import db
from pythonic.models import Device, Category, Type
from pythonic.admin.forms import TypeForm, CategoryForm, AddTypeCategoryForm, DeviceForm, UpdateCategoryForm
from flask_login import login_required

admin = Blueprint('admin', __name__)



# pythonic/decorators.py
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user, login_required


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please login first.", "danger")
            return redirect(url_for('users.login'))
        if current_user.id != 1:
            flash("You are not allowed to access this page.", "danger")
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)

    return decorated_function



@admin.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin.html')


@admin.route('/admin/add/type', methods=["GET", "Post"])
@login_required
@admin_required
def add_type():
    form = TypeForm()
    if form.validate_on_submit():
        type = Type(name=form.name.data)
        db.session.add(type)
        db.session.commit()
        flash(f"Type created successfully.", "success")
        return redirect(url_for('admin.admin'))
    return render_template('add_type.html', form=form)



@admin.route('/admin/add/category', methods=["GET", "Post"])
@login_required
@admin_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash(f"Category created successfully.", "success")
        return redirect(url_for('admin.admin'))
    return render_template('add_category.html', form=form)


@admin.route('/admin/add/type/category', methods=["GET", "Post"])
@login_required
@admin_required
def add_type_category():
    form = AddTypeCategoryForm()
    if form.validate_on_submit():
        type = Category(type=form.type.data)
        db.session.add(type)
        db.session.commit()
        flash(f"Type added for category successfully.", "success")
        return redirect(url_for('admin.admin'))
    return render_template('add_type_category.html', form=form)



@admin.route('/admin/add/device', methods=["GET", "Post"])
@login_required
@admin_required
def add_type_category():
    form = DeviceForm()
    if form.validate_on_submit():
        device = Device(name=form.name.data, description=form.description.data, category=form.category.data, type=form.type)
        db.session.add(device)
        db.session.commit()
        flash(f"Device created successfully.", "success")
        return redirect(url_for('admin.admin'))
    return render_template('add_type_category.html', form=form)



@admin.route('/admin/dashboard', methods=["GET", "POST"])
@login_required
@admin_required
def admin_dashboard(category_id):
    category = Category.query.get_or_404(category_id)
    category_form = UpdateCategoryForm(category_id=category.id)
    if category_form.validate_on_submit():
        category.name = category_form.name.data
        db.session.commit()
        flash(f"This Category has been updated.", "success")
        return redirect(url_for('admin.admin_dashboard'))
    elif request.method == "GET":
        category_form.name = category.name
    image_file = url_for('static', filename=f"category_pics/{category.image_file}")
    return render_template('admin_dashboard.html', category_form=category_form)
