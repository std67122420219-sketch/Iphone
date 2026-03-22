from flask import Blueprint, render_template, request
from iphone.extensions import db
from iphone.models import Iphone, Type   # 🔥 เปลี่ยน

core_bp = Blueprint('core', __name__, template_folder='templates')

# ------------------ HOME ------------------
@core_bp.route('/')
def index():
  page = request.args.get('page', 1, type=int)   # 🔥 ใส่ default = 1

  iphones = db.paginate(
    db.select(Iphone),   # 🔥 เปลี่ยน
    per_page=4,
    page=page
  )

  return render_template('core/index.html',
                         title='Home Page',
                         iphones=iphones)   # 🔥 เปลี่ยน


# ------------------ DETAIL ------------------
@core_bp.route('/<int:id>/detail')
def detail(id):
  iphone = db.session.get(Iphone, id)   # 🔥 เปลี่ยน

  return render_template('core/iphone_detail.html',   # 🔥 เปลี่ยน path
                         title='Iphone Detail Page',
                         iphone=iphone)   # 🔥 เปลี่ยน