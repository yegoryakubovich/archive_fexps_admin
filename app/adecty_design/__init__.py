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


from adecty_design.adecty_design import AdectyDesign
from adecty_design.elements.footer import Footer
from adecty_design.elements.header import Header
from adecty_design.elements.header_navigation_item import HeaderNavigationItem

from app.adecty_design.config import config
from app.adecty_design.icons import Icons

header = Header(
    config=config,
    navigation_items=[
        HeaderNavigationItem(
            name='Orders', url='/orders',
            icon=Icons.orders
        ),
        HeaderNavigationItem(
            name='Requisites', url='/requisites',
            icon=Icons.orders
        ),
        HeaderNavigationItem(
            name='Sign in', url='/login',
            icon=Icons.orders
        ),
        HeaderNavigationItem(
            name='Log out', url='/logout',
            icon=Icons.orders
        )
    ]
)
footer = Footer(config=config)

ad = AdectyDesign(config=config, header=header, footer=footer)
