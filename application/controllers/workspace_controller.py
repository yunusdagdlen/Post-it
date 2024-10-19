#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it
import bleach
from flask import render_template, request, redirect, url_for, abort, make_response, jsonify
from application.controller import mod_pages
from application.utils.workspace_utils import WorkspaceUtils


@mod_pages.route('/')
def index():
    workspace_id = request.args.get('workspace_id')
    if not workspace_id:
        workspace_id = WorkspaceUtils.create_workspace()
    response = WorkspaceUtils.get_workspace_notes(workspace_id=workspace_id)
    return jsonify(response)


@mod_pages.route('/add', methods=['GET'])
def add_note():
    title = request.args.get('title', '')
    note = request.args.get('note', '')
    workspace_id = request.args.get('workspace_id', '')
    color = request.args.get('color', '')
    if workspace_id and title or note:
        title = bleach.clean(title)
        note = bleach.clean(note)
        workspace_id = bleach.clean(workspace_id)
        response = WorkspaceUtils.add_note(title, note, workspace_id,color)
        return jsonify(response)


@mod_pages.route('/edit-note/', methods=['GET'])
def edit_note():
    title = request.args.get('title', '')
    note = request.args.get('note', '')
    note_id = request.args.get('note_id')
    workspace_id = request.args.get('workspace_id')
    if title or note:
        title = bleach.clean(title)
        note = bleach.clean(note)
        response = WorkspaceUtils.edit_note(title, note, note_id, workspace_id)

        if response['is_success']:
            return jsonify(response)



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
