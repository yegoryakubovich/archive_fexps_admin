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


import datetime

import requests

from config import URL_FORM


url_response = URL_FORM + '/formResponse'
url_referer = URL_FORM + '/viewform'


def form_send(name, value, datetime_paid: datetime.datetime):
    form_data = {
        'entry.338519300': datetime_paid.strftime("%Y-%m-%d, %I:%M %p"),
        'entry.620954733': 'Online payment link (ссылка на оплату)',
        'entry.1796859161_year': str(datetime_paid.year),
        'entry.1796859161_month': str(datetime_paid.month),
        'entry.1796859161_day': str(datetime_paid.day),
        'entry.622579112': 'Finance Express TEST',
        'entry.1473577004': name,
        'entry.1011239722': '{value}$'.format(value=value),
        'entry.1253902562': 'RUB'
    }
    user_agent = {
        'Referer': url_referer,
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"
    }
    requests.post(url_response, data=form_data, headers=user_agent)
