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

import hotline.database.ext
from hotline.auth import auth_required
from hotline.database import highlevel as db
from hotline.events import forms

blueprint = flask.Blueprint("events", __name__, template_folder="templates")
hotline.database.ext.init_app(blueprint)


@blueprint.route("/events")
@auth_required
def list():
    user_id = flask.g.user["user_id"]
    events = db.list_events(user_id=user_id)
    return flask.render_template("list.html", events=events)


@blueprint.route("/events/add", methods=["GET", "POST"])
@auth_required
def add():
    user_id = flask.g.user["user_id"]
    form = forms.EventEditForm(flask.request.form)

    if flask.request.method == "POST" and form.validate():
        event = db.new_event(user_id=user_id)
        form.populate_obj(event)
        event.save()
        return flask.redirect(flask.url_for(".numbers", event_slug=event.slug))

    return flask.render_template("add.html", form=form)


def _verify_access(event):
    user_id = flask.g.user["user_id"]
    if event.owner_user_id != user_id:
        flask.abort(403)


@blueprint.route("/events/<event_slug>/details", methods=["GET", "POST"])
@auth_required
def details(event_slug):
    event = db.get_event(event_slug)
    _verify_access(event)
    form = forms.EventEditForm(flask.request.form, event)

    if flask.request.method == "POST" and form.validate():
        form.populate_obj(event)
        event.save()

    return flask.render_template("edit.html", event=event, form=form)


@blueprint.route("/events/<event_slug>/numbers", methods=["GET", "POST"])
@auth_required
def numbers(event_slug):
    event = db.get_event(event_slug)
    _verify_access(event)
    members = db.get_event_members(event)
    form = forms.AddMemberForm()
    return flask.render_template(
        "numbers.html", event=event, members=members, form=form
    )


@blueprint.route("/events/<event_slug>/members", methods=["POST"])
@auth_required
def add_member(event_slug):
    _verify_access(db.get_event(event_slug))
    form = forms.AddMemberForm(flask.request.form)
    member = db.new_event_member(event_slug)
    form.populate_obj(member)
    member.save()
    return flask.redirect(flask.url_for(".numbers", event_slug=event_slug))


@blueprint.route("/events/<event_slug>/members/remove/<member_id>")
@auth_required
def remove_member(event_slug, member_id):
    _verify_access(db.get_event(event_slug))
    db.remove_event_member(event_slug, member_id)
    return flask.redirect(flask.url_for(".numbers", event_slug=event_slug))


@blueprint.route("/events/<event_slug>/release")
@auth_required
def release(event_slug):
    event = db.get_event(event_slug)
    event.primary_number = None
    event.primary_number_id = None
    event.save()
    return flask.redirect(flask.url_for(".numbers", event_slug=event_slug))


@blueprint.route("/events/<event_slug>/acquire")
@auth_required
def acquire(event_slug):
    db.acquire_number(event_slug)
    return flask.redirect(flask.url_for(".numbers", event_slug=event_slug))
