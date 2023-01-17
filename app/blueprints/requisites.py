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
from adecty_design.elements.form import Form
from adecty_design.elements.input import Input, InputTypes
from adecty_design.elements.page import Page
from adecty_design.elements.screen import Screen
from adecty_design.elements.table import Table
from adecty_design.elements.text import Text
from adecty_design.elements.url import Url
from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from app.adecty_design import config, ad
from app.models import RequisiteReceived


blueprint_requisites = Blueprint('blueprint_requisites', __name__)


@blueprint_requisites.route("/requisites", methods=['GET'])
@login_required
def bp_requisites():
    admin = current_user.admin
    requisites = []

    for requisite in RequisiteReceived.select():
        if not admin.permission_requisites and requisite.admin != admin:
            continue
        requisite: RequisiteReceived
        requisites.append([
            requisite.name,
            requisite.currency.name,
            Url(elements=[Text(text='Редактировать')], url='/requisites/{}'.format(requisite.id))
        ])

    page = Page(
        title='Реквизиты',
        screens=[
            Screen(elements=[
                Text(font=config.fonts.main, text='Список действующих реквизитов', font_size=24),
                Table(columns=['Название', 'Входящая валюта', 'Действия'], rows=requisites)
            ])
        ],
    )
    html = ad.get_page_html(page)

    return html


@blueprint_requisites.route("/requisites/<requisite_id>", methods=['GET', 'POST'])
@login_required
def bp_requisite(requisite_id):
    requisite = RequisiteReceived.get_or_none(RequisiteReceived.id == requisite_id)
    admin = current_user.admin

    if not admin.permission_requisites and requisite.admin != admin:
        return redirect('/requisites')

    if not requisite:
        return 401

    if request.method == 'POST':
        requisite.requisite = request.form['requisite']
        requisite.save()
        return redirect('/requisites')

    page = Page(
        title='Реквизиты',
        screens=[
            Screen(elements=[
                Text(font=config.fonts.main, text='Изменение реквизита {}'.format(requisite.name), font_size=24),
                Form(elements=[
                    Input(input_type=InputTypes.text, name='requisite', value=requisite.requisite),
                    Input(input_type=InputTypes.button, text='Сохранить'),
                ]),
            ])
        ],
    )
    html = ad.get_page_html(page)

    return html
