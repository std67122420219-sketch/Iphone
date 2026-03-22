from flask import Blueprint, render_template, request, flash, redirect, url_for
from iphone.extensions import db
from iphone.models import Iphone
from flask_login import login_required, current_user

iphone_bp = Blueprint('iphone', __name__, template_folder='templates')


# 🔹 แสดงรายการ
@iphone_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    iphones = db.paginate(db.select(Iphone), per_page=4, page=page)
    return render_template('iphone/index.html',
                           title='Iphone Page',
                           iphones=iphones)


# 🔹 เพิ่มข้อมูล
@iphone_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_iphone():
    if request.method == 'POST':
        name = request.form.get('name')
        model = request.form.get('model')
        price = request.form.get('price')
        description = request.form.get('description')
        img_url = request.form.get('img_url')
        user_id = current_user.id

        query = db.select(Iphone).where(Iphone.name == name)
        iphone = db.session.scalar(query)

        if iphone:
            flash(f'Iphone "{name}" already exists!', 'warning')
            return redirect(url_for('iphone.new_iphone'))

        new_iphone = Iphone(
            name=name,
            model=model,
            price=price,
            description=description,
            img_url=img_url,
            user_id=user_id
        )

        db.session.add(new_iphone)
        db.session.commit()

        flash('New iPhone added successfully!', 'success')
        return redirect(url_for('iphone.index'))

    return render_template('iphone/new_iphone.html',
                           title='New Iphone Page')


# 🔹 แก้ไขข้อมูล (✅ ตัวที่คุณขาด)
@iphone_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_iphone(id):
    iphone = db.get_or_404(Iphone, id)

    if request.method == 'POST':
        iphone.name = request.form.get('name')
        iphone.model = request.form.get('model')
        iphone.price = request.form.get('price')
        iphone.description = request.form.get('description')
        iphone.img_url = request.form.get('img_url')

        db.session.commit()

        flash('Iphone updated successfully!', 'success')
        return redirect(url_for('iphone.index'))

    return render_template('iphone/edit.html',
                           title='Edit Iphone',
                           iphone=iphone)


# 🔹 ลบข้อมูล (✅ ป้องกัน error ล่วงหน้า)
@iphone_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_iphone(id):
    iphone = db.get_or_404(Iphone, id)

    db.session.delete(iphone)
    db.session.commit()

    flash('Iphone deleted successfully!', 'danger')
    return redirect(url_for('iphone.index'))