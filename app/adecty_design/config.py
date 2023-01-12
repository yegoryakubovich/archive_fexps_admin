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


from adecty_design.elements.config import Config

from app.adecty_design.colors import colors
from app.adecty_design.fonts import fonts
from app.adecty_design.icons import Icons


config = Config(
    colors=colors,
    fonts=fonts,
    logo=Icons.logo,
    name='Finance Express - Admin',
    rounding=6
)
