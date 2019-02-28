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

import os

import nox


@nox.session(python="3.7")
def format(session):
    session.install("black", "isort")
    session.run("black", "hotline", "tests", "noxfile.py")
    session.run("isort", "-rc", "hotline", "tests", "noxfile.py")


@nox.session(python="3.7")
def lint(session):
    session.install("mypy", "flake8", "black")
    session.run("black", "--check", "hotline", "tests")
    session.run("flake8", "docuploader", "tests")
    session.run("mypy", "hotline")


@nox.session(python="3.7")
def test(session):
    session.install("-r", "requirements-test.txt")
    session.run("pytest", "tests")


@nox.session(python="3.7")
def serve(session):
    session.install("-r", "requirements.txt")
    # Workaround for https://github.com/pallets/werkzeug/issues/461
    env = {"PYTHONPATH": os.getcwd()}
    session.run("python", "-m", "hotline", env=env)


@nox.session(python="3.7")
def serve_prod(session):
    session.install("-r", "requirements.txt")
    session.run("gunicorn", "-b", ":8080", "hotline.__main__:app")


@nox.session(python="3.7")
def shell(session):
    session.install("-r", "requirements.txt")
    session.install("ipython")
    session.run("ipython")
