#
# (c) 2022, Yegor Yakubovich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.models import Order, Doc, AdminDoc
from config import DOCS_PATH, IS_DEBUG, ADMINS_DOCS_PATH

blueprint_orders = Blueprint('blueprint_orders', __name__, template_folder='templates')


@blueprint_orders.route("/orders", methods=['GET'])
@login_required
def bp_orders():
    return render_template('orders.html')


@blueprint_orders.route("/orders/<order_id>", methods=['GET'])
@login_required
def bp_order(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect('/orders')
    elif not order.doc or order.is_closed:
        return redirect('/orders')

    doc_path = '{}/{}.{}'.format(DOCS_PATH, order.doc.id, order.doc.extension) if not IS_DEBUG else \
        url_for('static', filename='images/{}.{}'.format(order.doc.id, order.doc.extension))
    admins_docs = ['{}/{}.{}'.format(ADMINS_DOCS_PATH, admin_doc.id, admin_doc.extension) if not IS_DEBUG else
                   url_for('static', filename='images/admins/{}.{}'.format(admin_doc.id, admin_doc.extension))
                   for admin_doc in AdminDoc.select().where(AdminDoc.order == order)]
    return render_template('order.html', order=order, doc_path=doc_path, admins_docs=admins_docs)


@blueprint_orders.route("/orders/<order_id>/confirm", methods=['POST'])
@login_required
def bp_order_confirm(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect('/orders')
    elif not order.doc or order.is_closed:
        return redirect('/orders')

    order.is_paid = True
    order.datetime_paid = datetime.now()
    order.save()

    return redirect('/orders/{}'.format(order.id))


@blueprint_orders.route("/orders/<order_id>/reject", methods=['POST'])
@login_required
def bp_order_reject(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect('/orders')
    elif not order.doc or order.is_closed:
        return redirect('/orders')

    order.is_paid = False
    order.is_closed = True
    order.datetime_paid = datetime.now()
    order.datetime_completed = datetime.now()
    order.save()

    return redirect('/orders/{}'.format(order.id))


@blueprint_orders.route("/orders/<order_id>/save", methods=['POST'])
@login_required
def bp_order_save(order_id):
    admin = current_user.admin
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect('/orders')
    elif not order.doc or order.is_closed:
        return redirect('/orders')

    file = request.files['file']
    filename = secure_filename(file.filename)

    extension = filename.split('.')[-1]
    doc = AdminDoc(admin=admin, order=order, extension=extension)
    doc.save()

    file.save('{}/{}.{}'.format(ADMINS_DOCS_PATH, doc.id, doc.extension))
    return redirect('/orders/{}'.format(order.id))
