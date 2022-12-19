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


from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, logout_user, login_user

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

    return render_template('login.html')


@blueprint_login.route("/logout", methods=['GET'])
@login_required
def admin_logout():
    logout_user()
    return redirect('/login')
