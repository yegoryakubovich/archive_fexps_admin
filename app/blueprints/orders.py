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

from adecty_design.elements.button import Button
from adecty_design.elements.dictionary import Dictionary
from adecty_design.elements.form import Form
from adecty_design.elements.input import Input, InputTypes
from adecty_design.elements.page import Page
from adecty_design.elements.screen import Screen
from adecty_design.elements.table import Table
from adecty_design.elements.text import Text
from adecty_design.elements.url import Url
from flask import Blueprint, redirect, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.adecty_design import config, ad
from app.forms.forms import form_send
from app.models import Order, AdminDoc
from app.notifications import notification_send
from config import DOCS_PATH, ADMINS_DOCS_PATH, Texts, TG_GROUP

blueprint_orders = Blueprint('blueprint_orders', __name__, template_folder='templates')
status = {
    True: '🟩',
    False: '🟥',
}


@blueprint_orders.route('/orders', methods=['GET'])
@login_required
def bp_orders():
    admin = current_user.admin
    orders = []

    for order in Order.select():
        if order.doc is None:
            continue
        if not admin.permission_orders and (order.is_closed or not order.requisite_received.admin == admin):
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


@blueprint_orders.route('/orders/<order_id>', methods=['GET', 'POST'])
@login_required
def bp_order(order_id):
    admin = current_user.admin
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect('/orders')
    elif not admin.permission_orders and (order.is_closed or not order.requisite_received.admin == admin):
        return redirect('/orders')
    elif not order.doc:
        return redirect('/orders')

    if request.method == 'POST':
        received_usdt = request.form['received_usdt']
        file_1 = request.files['file_1']
        file_2 = request.files['file_2']

        if not received_usdt or not file_1 or not file_2:
            return redirect('/orders/{order_id}'.format(order_id=order.id))

        for f in [file_1, file_2]:
            filename = secure_filename(f.filename)

            extension = filename.split('.')[-1]
            admin_doc = AdminDoc(admin=admin, order=order, extension=extension)
            admin_doc.save()

            f.save('{}/{}.{}'.format(ADMINS_DOCS_PATH, admin_doc.id, admin_doc.extension))

        order.received_usdt = received_usdt
        order.is_completed = True
        order.is_closed = True
        order.datetime_paid = datetime.now()
        order.datetime_completed = datetime.now()
        order.save()

        return redirect('/orders/{order_id}'.format(order_id=order.id))

    doc_path = '{}/{}.{}'.format(DOCS_PATH, order.doc.id, order.doc.extension)
    admin_doc = AdminDoc.get_or_none(AdminDoc.order == order)
    admin_doc_path = '{}/{}.{}'.format(DOCS_PATH + '/admins', admin_doc.id, admin_doc.extension) if admin_doc else None
    order_status = 'Ожидает проверки оплаты'
    if order.is_completed and order.is_closed:
        order_status = 'Исполнен, закрыт'
    elif order.is_paid:
        order_status = 'В исполнении'

    keys = ['ID заказа', 'Клиент', 'Сделка на', 'Курс', 'Реквизит получения', 'Описание к реквизиту получения',
            'Реквизит оплаты', 'Прикрепленный документ', 'Комиссия в RUB', 'Отправлено в USDT',
            'Документ администратора', 'Статус заказа'] if admin.permission_orders else \
        ['Сделка на', 'Реквизит оплаты', 'Прикрепленный документ',
         'Комиссия в RUB', 'Отправлено в USDT', 'Документ администратора', 'Статус заказа']

    values_permission = [str(order.id), order.customer.name, '{}{} -> {}{}'.format(
        order.currency_exchangeable_value,
        order.direction.currency_exchangeable.name,
        order.currency_received_value,
        order.direction.currency_received.name
    ), str(order.rate), order.requisite_exchangeable.name if order.requisite_exchangeable else 'Not required',
                         order.requisite_exchangeable_value if order.requisite_exchangeable_value else 'Not required',
                         order.requisite_received.name,
                         Url(elements=[Text('Просмотреть документ от пользователя')], url=doc_path),
                         str(order.commission_rub), str(order.received_usdt),
                         Url(elements=[Text('Просмотреть документ от администратора')], url=admin_doc_path) if admin_doc
                         else 'Документ еще не прикреплен',
                         order_status]
    values = [
        '{}{} -> {}{}'.format(order.currency_exchangeable_value, order.direction.currency_exchangeable.name,
                              order.currency_received_value, order.direction.currency_received.name),
        order.requisite_received.name, Url(elements=[Text('Просмотреть документ от пользователя')], url=doc_path),
        str(order.commission_rub), str(order.received_usdt),
        Url(elements=[Text('Просмотреть документ от администратора')], url=admin_doc_path) if admin_doc
        else 'Документ еще не прикреплен',
        order_status
    ]

    elements = [
        Text(font=config.fonts.main, text='Информация о заказе №{}'.format(order.id), font_size=24),
        Dictionary(keys=keys, values=values_permission if admin.permission_orders else values),
    ]
    if not order.is_paid:
        elements.append(Button(value='Подтвердить оплату', url='{}/confirm'.format(order.id)))
        elements.append(Button(value='Отклонить оплату', url='{}/reject'.format(order.id)))
    elif not order.received_usdt or not admin_doc or admin.permission_orders:
        elements.append(
            Form(elements=[
                Text(font=config.fonts.main, text='Прикрепить файлы', font_size=18),
                Input(input_type=InputTypes.file, name='file_1',),
                Input(input_type=InputTypes.file, name='file_2', ),
                Text(font=config.fonts.main, text='Отправлено в USDT', font_size=18),
                Input(
                    input_type=InputTypes.text, name='received_usdt',
                    value=order.received_usdt if order.received_usdt else ''
                ),
                Input(input_type=InputTypes.button, text='Сохранить'),
            ]),
        )
    page = Page(
        title='Заказ',
        screens=[
            Screen(elements=elements)
        ],
    )
    html = ad.get_page_html(page)
    return html


@blueprint_orders.route('/orders/<order_id>/confirm', methods=['GET'])
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
    if order.requisite_exchangeable is None:
        notification_send(
            chat_id=order.customer.user_id,
            text=Texts.bridge_notification_order_payment_confirmed,
            is_bridge=True,
        )
        form_send(name=order.customer.name, value=order.currency_received_value, datetime_paid=order.datetime_paid)
    else:
        notification_send(
            chat_id=order.customer.user_id,
            text=Texts.notification_order_payment_confirmed,
        )
    notification_send(chat_id=TG_GROUP, text=Texts.notification_admins_order_payment_confirmed.format(order.id))

    return redirect('/orders/{}'.format(order.id))


@blueprint_orders.route('/orders/<order_id>/reject', methods=['GET'])
@login_required
def bp_order_reject(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect('/orders')
    elif not order.doc or order.is_closed or order.is_paid:
        return redirect('/orders')

    order.is_paid = False
    order.is_closed = True
    order.datetime_paid = datetime.now()
    order.datetime_completed = datetime.now()
    order.save()

    # Notification to user & admins
    if order.requisite_exchangeable is None:
        notification_send(
            chat_id=order.customer.user_id,
            text=Texts.bridge_notification_order_payment_rejected,
            is_bridge=True,
        )
    else:
        notification_send(
            chat_id=order.customer.user_id,
            text=Texts.notification_order_payment_rejected,
        )

    notification_send(chat_id=TG_GROUP, text=Texts.notification_admins_order_payment_rejected.format(order.id))

    return redirect('/orders/{}'.format(order.id))
