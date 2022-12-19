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


from app.models import Admin


class AdminLogin:
    admin = None

    def from_db(self, account_id):
        self.admin = Admin.get(Admin.id == account_id)
        return self

    def create(self, admin):
        self.admin = admin
        return self

    def is_authenticated(self):
        if self.admin:
            return True
        else:
            return False

    def is_active(self):
        if self.admin:
            return True
        else:
            return False

    def is_anonymous(self):
        if self.admin:
            return False
        else:
            return True

    def get_id(self):
        admin_id = self.admin.id
        return str(admin_id)
