#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it
import bleach
from flask import render_template, request, redirect, url_for, abort, make_response, jsonify
from application.controller import mod_pages
from application.utils.notes_utils import SingleNoteUtils
from application.utils.workspace_utils import WorkspaceUtils


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
        title = request.form.get('title', '')
        note = request.form.get('note', '')
        if title or note:
            title = bleach.clean(title)
            note = bleach.clean(note)
            workspace_id = request.cookies.get('workspace_uuid')
            WorkspaceUtils.add_note(title, note, workspace_id)
            return redirect((url_for('pages.index')))
        else:
            return render_template('404_page.html')
    else:
        abort(make_response("Not Found", 404))


@mod_pages.route('/edit-note/', methods=['POST', 'GET'])
def edit_note():
    if request.method == 'POST':
        title = request.form.get('edited_title', '')
        note = request.form.get('edited_note', '')
        uuid = request.form.get('hidden_uuid')
        workspace_uuid = request.cookies.get('workspace_uuid')
        if title or note:
            title = bleach.clean(title)
            note = bleach.clean(note)
            WorkspaceUtils.edit_note(title, note, uuid, workspace_uuid)
            return redirect(url_for('pages.index'))
        else:
            return 'hata sayfası'
    else:
        abort(make_response("Not Found", 404))


@mod_pages.route("/del/<string:id>", methods=['POST', 'GET'])
def delete_note(id):
    if request.method == 'POST':
        workspace_uuid = request.cookies.get('workspace_uuid')
        issucces = WorkspaceUtils.delete_note(id=id, workspace_uuid=workspace_uuid)
        if not issucces:
            abort(make_response("Hata", 400))
        return make_response('success', 200)

    else:
        abort(make_response("Accepted", 202))


@mod_pages.route('/back', methods=['POST', 'GET'])
def back():
    return redirect(url_for('pages.index'))


@mod_pages.route('/list_postits', methods=['GET'])
def list_postits():
    workspace_uuid = request.args.get('workspace_uuid')
    if not workspace_uuid:
        workspace_uuid = request.cookies.get('workspace_uuid')

    notes_list = []
    if workspace_uuid:
        postits = WorkspaceUtils.get_workspace_notes(workspace_uuid=workspace_uuid)
        for postit in postits:
            notes_list.append({
                'title': postit.title,
                'note_list': postit.note.splitlines()[:3],
                'uuid': postit.uuid
            })

    return jsonify(notes_list)


@mod_pages.route('/get_note_text/<uuid>', methods=['GET'])
def get_single_note_detail(uuid):
    postit_rec = SingleNoteUtils.get_single_note(uuid)

    note = {}
    if postit_rec:
        note = {
                'title': postit_rec.title,
                'note': postit_rec.note,
                'uuid': postit_rec.uuid
            }

    return jsonify(note)
