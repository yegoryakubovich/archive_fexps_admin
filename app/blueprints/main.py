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
from flask import Blueprint

from app.adecty_design import config, ad

blueprint_main = Blueprint('blueprint_main', __name__, template_folder='templates')


@blueprint_main.route("/")
def home():
    page = Page(screens=[Screen(elements=[
        Text(font=config.fonts.main, text='Привет, мир!', font_size=24),
    ])], title='Main page')
    html = ad.get_page_html(page)
    return html
