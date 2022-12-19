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


from flask import Blueprint, render_template, redirect
from flask_login import login_required

from app.models import Order


blueprint_orders = Blueprint('blueprint_orders', __name__, template_folder='templates')


@blueprint_orders.route("/orders", methods=['GET'])
@login_required
def bp_orders():
    return render_template('orders.html')


@blueprint_orders.route("/orders/<order_id>", methods=['GET', 'POST'])
@login_required
def bp_order(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect('/orders')
    elif not order.doc or order.is_closed:
        return redirect('/orders')
    return render_template('order.html', order=order)
