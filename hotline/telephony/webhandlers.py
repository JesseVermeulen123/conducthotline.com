# Copyright 2019 Alethea Katherine Flowers
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

import flask

from hotline import injector


blueprint = flask.Blueprint('telephony', __name__)


@blueprint.route("/event/inbound-sms", methods=["POST"])
@injector.needs("secrets.virtual_number")
def inbound_sms(virtual_number):
    # TODO: Probably validate this.
    message = flask.request.get_json()

    print(message)

    return "", 204
