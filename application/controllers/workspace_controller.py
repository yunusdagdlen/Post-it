#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it
"""Flask controllers for Post-it. Cosmetic refactor only; logic unchanged."""

import bleach
from flask import (
    abort,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
)

from application.controller import mod_pages
from application.utils.workspace_utils import WorkspaceUtils


@mod_pages.route('/')
def index_legacy():
    """Legacy index: redirect to /app."""
    return redirect('/app')


@mod_pages.route('/app')  # production build initial point
def index():
    """Render SPA entry and optionally persist incoming workspace_id to session."""
    workspace_id = request.args.get('workspace_id')
    if workspace_id:
        session['workspace_id'] = workspace_id
    return render_template('app/index.html')


@mod_pages.route('/app/list_postits', methods=['GET'])
def list_postits_app():
    """Return JSON list of notes for current workspace (and the workspace id)."""
    mode = request.args.get('mode', '')
    workspace_uuid = WorkspaceUtils.get_workspace_id()
    response = {
        'workspace_id': workspace_uuid,
        'postits': WorkspaceUtils.get_workspace_notes(workspace_uuid=workspace_uuid, mode=mode),
    }
    return jsonify(response)


@mod_pages.route('/app/add', methods=['GET'])
def add_note_app():
    """Add note endpoint (expects title and/or note via query params)."""
    title = request.args.get('title', '')
    note = request.args.get('note', '')
    color = request.args.get('color', '')

    workspace_id = WorkspaceUtils.get_workspace_id()

    # Require at least a title or note content
    if title or note:
        title = bleach.clean(title).replace('&amp;', '&')
        note = bleach.clean(note).replace('&amp;', '&')
        workspace_id = bleach.clean(workspace_id)
        color = bleach.clean(color)

        is_success = WorkspaceUtils.add_note(title, note, workspace_id, color)
        response = {'is_success': is_success, 'workspace_id': workspace_id}
        return jsonify(response)

    # If no content provided, return 400
    return abort(make_response("Bad Request: title or note required", 400))


@mod_pages.route('/app/edit-note/', methods=['GET'])
def edit_note_app():
    """AJAX edit note endpoint (JSON)."""
    title = request.args.get('title', '')
    note = request.args.get('note', '')
    color = request.args.get('color', None)
    note_id = request.args.get('note_id')
    workspace_id = WorkspaceUtils.get_workspace_id(request.args.get('workspace_id'))
    if title or note or color is not None:
        title = bleach.clean(title)
        note = bleach.clean(note)
        if color is not None:
            color = bleach.clean(color)
        response = WorkspaceUtils.edit_note(title, note, note_id, workspace_id, color=color)

        if response['is_success']:
            return jsonify(response)


@mod_pages.route('/app/delete-note/', methods=['GET'])
def delete_note_app():
    """AJAX delete note endpoint (soft delete)."""
    note_id = request.args.get('note_id')
    workspace_id = WorkspaceUtils.get_workspace_id()
    if note_id:
        response = WorkspaceUtils.delete_note(id=note_id, workspace_uuid=workspace_id)
        if response['is_success']:
            return jsonify(response)


@mod_pages.route('/app/disable-note/', methods=['GET'])
def disable_note_app():
    """AJAX toggle note active endpoint."""
    note_id = request.args.get('note_id')
    workspace_id = WorkspaceUtils.get_workspace_id()
    if note_id:
        response = WorkspaceUtils.disable_note(id=note_id, workspace_uuid=workspace_id)
        if response['is_success']:
            return jsonify(response)


@mod_pages.route('/app/clear-workspace', methods=['GET', 'POST'])
def clear_workspace():
    """Clear workspace id from session."""
    session.pop('workspace_id', None)
    return jsonify({'is_success': True})
