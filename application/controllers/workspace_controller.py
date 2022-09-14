import uuid

import flask
import requests
from flask import render_template, request, redirect, url_for, abort, make_response

from application.controller import mod_pages
from application.models import Postit
from application.utils.workspace_utils import WorkspaceUtils
from application.models import WorkSpaces


@mod_pages.route('/')
def index():
    workspace_uuid = request.args.get('workspace_uuid')
    if not workspace_uuid:
        workspace_uuid = request.cookies.get('workspace_uuid')
    if not workspace_uuid:
        workspace_uuid = WorkspaceUtils.create_workspace()

    postits = WorkspaceUtils.get_workspace_notes(workspace_uuid=workspace_uuid)

    resp = make_response(render_template('index.html',
                                         postit_list=postits, ))
    resp.set_cookie('workspace_uuid', workspace_uuid)
    return resp


@mod_pages.route('/add', methods=['POST', 'GET'])
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')
        if title or note:
            workspace_id = request.cookies.get('workspace_uuid')
            WorkspaceUtils.add_note(title, note, workspace_id)
            return redirect((url_for('pages.index')))
        else:
            return ''
    else:
        abort(make_response("Not Found", 404))


@mod_pages.route('/edit-note/', methods=['POST', 'GET'])
def edit_note():
    if request.method == 'POST':
        title = request.form.get('edited_title')
        note = request.form.get('edited_note')
        uuid = request.form.get('hidden_uuid')
        workspace_id = request.cookies.get('workspace_uuid')
        if title or note:
            WorkspaceUtils.edit_note(title, note, uuid)
            return redirect(url_for('pages.index'))
        else:
            return 'hata sayfası'
    else:
        abort(make_response("Not Found", 404))


@mod_pages.route("/del/<string:id>", methods=['POST', 'GET'])
def delete_note(id):
    if request.method == 'POST':
        issucces = WorkspaceUtils.delete_note(id=id)
        if not issucces:
            abort(make_response("Hata", 400))
        return make_response('success', 200)

    else:
        abort(make_response("Accepted", 202))


@mod_pages.route('/back', methods=['POST', 'GET'])
def back():
    return redirect(url_for('pages.index'))
