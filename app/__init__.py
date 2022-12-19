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


from flask import Flask
from flask_login import LoginManager

from app.login import AdminLogin
from app.blueprint_login import blueprint_login
from app.blueprint_main import blueprint_main
from config import SECRET_KEY


blueprints = [blueprint_main, blueprint_login]


def blueprints_register(app):
    [app.register_blueprint(blueprint) for blueprint in blueprints]


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    login_manager = LoginManager(app)

    @login_manager.user_loader
    def account_load(account_id):
        return AdminLogin().from_db(account_id)

    blueprints_register(app=app)
    return app
