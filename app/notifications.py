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


# noinspection PyPackageRequirements
from telebot import TeleBot

from config import TG_GROUP, TG_KEY


bot = TeleBot(TG_KEY)


def notification_send(text: str, chat_id=TG_GROUP):
    bot.send_message(chat_id, text)
