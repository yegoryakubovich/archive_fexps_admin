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


from os import getenv


DB_HOST = getenv('DB_HOST')
DB_PORT = int(getenv('DB_PORT'))
DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_NAME = getenv('DB_NAME')

SECRET_KEY = getenv('SECRET_KEY')
IS_DEBUG = bool(getenv('IS_DEBUG'))

DOCS_PATH = getenv('DOCS_PATH')
ADMINS_DOCS_PATH = getenv('ADMINS_DOCS_PATH')

TG_KEY = getenv('TG_KEY')
TG_BRIDGE_KEY = getenv('TG_BRIDGE_KEY')
TG_GROUP = getenv('TG_GROUP')

URL_FORM = getenv('URL_FORM')


class Texts:
    notification_order_payment_confirmed = 'Мы проверили оплату - она прошла. Ожидайте исполнения заказа!'
    notification_order_payment_rejected = 'Мы проверили оплату - она НЕ прошла. Пожалуйста, повторите попытку ' \
                                          'создания заказа и оплаты! Если нужна помощь - напишите в нашу поддержку.'

    bridge_notification_order_payment_confirmed = 'Спасибо за поддержку! Платеж принят.'
    bridge_notification_order_payment_rejected = 'К сожалению платеж не прошел. Хотите повторить попытку? Введите ' \
                                                 'сумму. '

    notification_admins_order_payment_rejected = 'Оплата по заказу №{} ОТКЛОНЕНА.'
    notification_admins_order_payment_confirmed = 'Оплата по заказу №{} ПРИНЯТА.'
