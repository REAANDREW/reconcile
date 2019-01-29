from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

INDEX_BLUEPRINT = Blueprint("index", __name__, template_folder="templates")


@INDEX_BLUEPRINT.route("/", defaults={"page": "index"})
@INDEX_BLUEPRINT.route("/<page>")
def show(page):
    try:
        return render_template("pages/%s.html" % page)
    except TemplateNotFound:
        abort(404)
