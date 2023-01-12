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

from adecty_design.elements.dictionary import Dictionary
from adecty_design.elements.page import Page
from adecty_design.elements.screen import Screen
from adecty_design.elements.table import Table
from adecty_design.elements.text import Text
from adecty_design.elements.url import Url
from flask import Blueprint, redirect, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.adecty_design import config, ad
from app.models import Order, AdminDoc
from app.notifications import notification_send
from config import DOCS_PATH, ADMINS_DOCS_PATH, Texts, TG_GROUP

blueprint_orders = Blueprint('blueprint_orders', __name__, template_folder='templates')
status = {
    True: '🟩',
    False: '🟥',
}


@blueprint_orders.route("/orders", methods=['GET'])
@login_required
def bp_orders():
    admin = current_user.admin
    orders = []

    for order in Order.select():
        if order.currency_received_value is None:
            continue
        if not admin.permission_orders and order.is_closed:
            continue
        orders.append([
            str(order.id),
            order.customer.name,
            '{}{} -> {}{}'.format(
                order.currency_exchangeable_value,
                order.direction.currency_exchangeable.name,
                order.currency_received_value,
                order.direction.currency_received.name
            ),
            status[order.is_paid],
            status[order.is_completed],
            status[order.is_closed],
            Url(elements=[Text(text='->')], url='/orders/{}'.format(order.id))
        ])

    page = Page(
        title='Заказы',
        screens=[
            Screen(elements=[
                Text(font=config.fonts.main, text='Список заказов', font_size=24),
                Table(columns=['ID', 'Клиент', 'Сделка', 'Оплачен', 'Исполнен', 'Закрыт', 'Действия'], rows=orders)
            ])
        ],
    )
    html = ad.get_page_html(page)

    return html


@blueprint_orders.route("/orders/<order_id>", methods=['GET'])
@login_required
def bp_order(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect('/orders')
    elif not order.doc or order.is_closed:
        return redirect('/orders')

    doc_path = '{}/{}.{}'.format(DOCS_PATH, order.doc.id, order.doc.extension)
    order_status = 'Ожидает проверки оплаты'
    if order.is_paid:
        order_status = 'Оплачен, ожидает исполнения'
    if order.is_completed and order.is_closed:
        order_status = 'Закрыт и исполнен'
    if order.is_closed:
        order_status = 'Закрыт'
    elements = [
        Text(font=config.fonts.main, text='Информация о заказе №{}'.format(order.id), font_size=24),
        Dictionary(keys=['ID заказа', 'Клиент', 'Сделка на', 'Курс', 'Реквизит получения',
                         'Описание к реквизиту получения', 'Реквизит оплаты', 'Прикрепленный документ',
                         'Статус заказа'],
                   values=[
                       str(order.id),
                       order.customer.name,
                       '{}{} -> {}{}'.format(
                           order.currency_exchangeable_value,
                           order.direction.currency_exchangeable.name,
                           order.currency_received_value,
                           order.direction.currency_received.name
                       ),
                       str(order.rate),
                       order.requisite_exchangeable.name,
                       order.requisite_exchangeable_value,
                       order.requisite_received.name,
                       Url(elements=[Text('Просмотреть документ от пользователя')], url=doc_path),
                       order_status
                   ]),
    ]
    if order.is_paid:
        for admin_doc in AdminDoc.select().where(AdminDoc.order == order):
            elements.append(Text('{}/{}.{}'.format(ADMINS_DOCS_PATH, admin_doc.id, admin_doc.extension)))
    else:
        elements.append(Url(elements=[Text('Подтвердить заказ')], url='{}/confirm'.format(order.id)))
        elements.append(Url(elements=[Text('Отклонить заказ')], url='{}/reject'.format(order.id)))
    page = Page(
        title='Авторизация',
        screens=[
            Screen(elements=elements)
        ],
    )
    html = ad.get_page_html(page)
    return html


@blueprint_orders.route("/orders/<order_id>/confirm", methods=['GET'])
@login_required
def bp_order_confirm(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect('/orders')
    elif not order.doc or order.is_closed or order.is_paid:
        return redirect('/orders')

    order.is_paid = True
    order.datetime_paid = datetime.now()
    order.save()

    # Notification to user & admins
    notification_send(chat_id=order.customer.user_id, text=Texts.notification_order_payment_confirmed)
    notification_send(chat_id=TG_GROUP, text=Texts.notification_admins_order_payment_confirmed.format(order.id))

    return redirect('/orders/{}'.format(order.id))


@blueprint_orders.route("/orders/<order_id>/reject", methods=['GET'])
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

    # Notification to user & admins
    notification_send(chat_id=order.customer.user_id, text=Texts.notification_order_payment_rejected)
    notification_send(chat_id=TG_GROUP, text=Texts.notification_admins_order_payment_rejected.format(order.id))

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

    if request.form:
        order.commission_rub = request.form['commission_rub']
        order.received_usdt = request.form['received_usdt']
        order.save()
        return redirect('/orders/{}'.format(order.id))

    file = request.files['file']
    if not file:
        return redirect('/orders/{}'.format(order.id))

    filename = secure_filename(file.filename)

    extension = filename.split('.')[-1]
    doc = AdminDoc(admin=admin, order=order, extension=extension)
    doc.save()

    file.save('{}/{}.{}'.format(ADMINS_DOCS_PATH, doc.id, doc.extension))
    return redirect('/orders/{}'.format(order.id))
