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

import phonenumbers
import wtforms


class EventEditForm(wtforms.Form):
    name = wtforms.StringField(
        "Event name", validators=[wtforms.validators.InputRequired()]
    )
    slug = wtforms.StringField(
        "URL Slug",
        description="Used to generate a URL for your event. For example, https://conducthotline/pycascades",
        validators=[wtforms.validators.InputRequired()],
    )
    coc_link = wtforms.StringField()
    website = wtforms.StringField()
    contact_email = wtforms.StringField()
    location = wtforms.StringField()


def validate_phone_number(form, field):
    try:
        number = phonenumbers.parse(field.data, "US")

    except phonenumbers.NumberParseException:
        raise wtforms.ValidationError(
            f"{field.data} does not appear to be a valid number."
        )

    if not phonenumbers.is_possible_number(number):
        raise wtforms.ValidationError(
            f"{field.data} does not appear to be a possible number."
        )

    field.data = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)


class AddMemberForm(wtforms.Form):
    name = wtforms.StringField("Name", validators=[wtforms.validators.InputRequired()])
    number = wtforms.StringField(
        "Number", validators=[wtforms.validators.InputRequired(), validate_phone_number]
    )
