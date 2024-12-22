#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it
import bleach
from flask import render_template, request, redirect, url_for, abort, make_response, jsonify, session

from application.controller import mod_pages
from application.utils.workspace_utils import WorkspaceUtils


@mod_pages.route('/')
def index_legacy():
    return redirect('/app')

@mod_pages.route('/app') # production build initial point
def index():
    workspace_id = request.args.get('workspace_id')
    if workspace_id:
        session['workspace_id'] = workspace_id
    return render_template('app/index.html')


@mod_pages.route('/edit-note', methods=['POST', 'GET'])
def edit_note():
    if request.method == 'GET':
        title = request.args.get('title', '')
        note = request.args.get('note', '')
        uuid = request.args.get('note_id')
        workspace_uuid = request.args.get('workspace_id')
        if title or note:
            title = bleach.clean(title)
            note = bleach.clean(note)
            title = title.replace('&amp;', '&')
            note = note.replace('&amp;', '&')
            respnse = WorkspaceUtils.edit_note(title, note, uuid, workspace_uuid)
            if respnse['is_success']:
                return redirect(f'/app?workspace_id={workspace_uuid}')
            else:
                'hata sayfası'
        else:
            return 'hata sayfası'
    else:
        abort(make_response("Not Found", 404))


@mod_pages.route('/back', methods=['POST', 'GET'])
def back():
    return redirect(url_for('pages.index'))


@mod_pages.route('/app/list_postits', methods=['GET'])
def list_postits_app():
    workspace_uuid = request.args.get('workspace_id')
    mode = request.args.get('mode', '')
    response={}
    if not workspace_uuid:
        workspace_uuid = session.get('workspace_id')

    if not workspace_uuid:
        response['workspace_id'] = WorkspaceUtils.create_workspace()
    else:
        response['postits'] = WorkspaceUtils.get_workspace_notes(workspace_uuid=workspace_uuid, mode=mode)
    return jsonify(response)


@mod_pages.route('/app/add', methods=['GET'])
def add_note_app():
    title = request.args.get('title', '')
    note = request.args.get('note', '')
    workspace_id = request.args.get('workspace_id', '')
    color = request.args.get('color', '')
    if workspace_id and title or note:
        title = bleach.clean(title)
        note = bleach.clean(note)
        title = title.replace('&amp;', '&')
        note = note.replace('&amp;', '&')
        workspace_id = bleach.clean(workspace_id)
        response = WorkspaceUtils.add_note(title, note, workspace_id,color)
        return jsonify(response)

@mod_pages.route('/app/edit-note/', methods=['GET'])
def edit_note_app():
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

@mod_pages.route('/app/delete-note/', methods=['GET'])
def delete_note_app():
    note_id = request.args.get('note_id')
    workspace_id = request.args.get('workspace_id')
    if note_id and workspace_id:
        response = WorkspaceUtils.delete_note(id=note_id, workspace_uuid=workspace_id)
        if response['is_success']:
            return jsonify(response)

@mod_pages.route('/app/disable-note/', methods=['GET'])
def disable_note_app():
    note_id = request.args.get('note_id')
    workspace_id = request.args.get('workspace_id')
    if note_id and workspace_id:
        response = WorkspaceUtils.disable_note(id=note_id, workspace_uuid=workspace_id)
        if response['is_success']:
            return jsonify(response)

