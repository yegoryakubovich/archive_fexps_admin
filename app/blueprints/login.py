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
from adecty_design.elements.text import Text
from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, logout_user, login_user

from app.adecty_design import config, ad
from app.models import Admin
from app.login import AdminLogin

blueprint_login = Blueprint('blueprint_login', __name__, template_folder='templates')


@blueprint_login.route("/login", methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        admin = Admin.get_or_none((Admin.login == login) & (Admin.password == password))
        if admin:
            login_user(AdminLogin().create(admin))
            return redirect('/orders')

    page = Page(
        title='Авторизация',
        screens=[
            Screen(elements=[
                Form(elements=[
                    Text(color=config.colors.primary, font=config.fonts.main, text='Логин', font_size=18),
                    Input(input_type=InputTypes.text, name='login'),
                    Text(color=config.colors.primary, font=config.fonts.main, text='Пароль', font_size=18),
                    Input(input_type=InputTypes.text, name='password'),
                    Input(input_type=InputTypes.button, text='Логин'),
                ])
            ])
        ],
    )
    html = ad.get_page_html(page)

    return html


@blueprint_login.route("/logout", methods=['GET'])
@login_required
def admin_logout():
    logout_user()
    return redirect('/login')
