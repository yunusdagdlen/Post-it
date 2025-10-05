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
from application.utils.translation_utils import TranslationUtils


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
    """Return JSON list of notes for current workspace (and the workspace id).

    Be lenient with incoming query param names to support various frontend emitters.
    Accepts keys like: mode | filter[mode] | filter.mode | currentMode; similarly for rank/status and search.
    """
    # Resolve possible param name variations
    mode = (
        request.args.get('mode')
        or request.args.get('filter[mode]')
        or request.args.get('filter.mode')
        or request.args.get('currentMode')
        or ''
    )
    rank = (
        request.args.get('rank')
        or request.args.get('filter[rank]')
        or request.args.get('filter.rank')
        or request.args.get('currentRankFilter')
    )
    status = (
        request.args.get('status')
        or request.args.get('filter[status]')
        or request.args.get('filter.status')
        or request.args.get('currentStatusFilter')
    )
    search = (
        request.args.get('search')
        or request.args.get('q')
        or request.args.get('query')
        or request.args.get('filter[search]')
        or request.args.get('filter.search')
    )

    workspace_uuid = WorkspaceUtils.get_workspace_id()
    response = {
        'workspace_id': workspace_uuid,
        'postits': WorkspaceUtils.get_workspace_notes(workspace_uuid=workspace_uuid, mode=mode, rank=rank, status=status, search=search),
    }
    return jsonify(response)


@mod_pages.route('/app/add', methods=['GET'])
def add_note_app():
    """Add note endpoint (expects title and/or note via query params)."""
    title = request.args.get('title', '')
    note = request.args.get('note', '')
    color = request.args.get('color', '')
    status = request.args.get('status')  # can be int or string name
    rank = request.args.get('rank')

    workspace_id = WorkspaceUtils.get_workspace_id()

    # Require at least a title or note content
    if title or note:
        title = bleach.clean(title).replace('&amp;', '&')
        note = bleach.clean(note).replace('&amp;', '&')
        workspace_id = bleach.clean(workspace_id)
        color = bleach.clean(color)

        is_success = WorkspaceUtils.add_note(title, note, workspace_id, color, status=status, rank=rank)
        response = {'is_success': is_success, 'workspace_id': workspace_id}
        return jsonify(response)

    # If no content provided, return 400
    return abort(make_response("Bad Request: title or note required", 400))


@mod_pages.route('/app/edit-note/', methods=['GET'])
def edit_note_app():
    """AJAX edit note endpoint (JSON)."""
    # Use None as default to detect missing fields; avoid overwriting when not provided
    title = request.args.get('title')
    note = request.args.get('note')
    color = request.args.get('color', None)
    status = request.args.get('status')
    rank = request.args.get('rank')
    note_id = request.args.get('note_id')
    workspace_id = WorkspaceUtils.get_workspace_id(request.args.get('workspace_id'))
    if (title is not None) or (note is not None) or (color is not None) or (status is not None) or (rank is not None):
        if title is not None:
            title = bleach.clean(title)
        if note is not None:
            note = bleach.clean(note)
        if color is not None:
            color = bleach.clean(color)
        response = WorkspaceUtils.edit_note(title, note, note_id, workspace_id, color=color, status=status, rank=rank)

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


@mod_pages.route('/app/translate', methods=['POST'])
def translate_text():
    """Translate text using googletrans via TranslationUtils.

    Expects JSON: {"text": str, "source": str (optional, default 'auto'), "target": str}
    Returns: {"translation": str, "alternatives": list}
    """
    data = request.get_json(silent=True) or {}
    text = (data.get('text') or '').strip()
    source = (data.get('source') or 'auto').strip() or 'auto'
    target = (data.get('target') or '').strip()

    if not text or not target:
        return make_response(jsonify({
            'error': 'Missing required fields',
            'details': 'Provide text and target language code.'
        }), 400)

    try:
        result = TranslationUtils.translate(text=text, source=source, target=target)
        return jsonify(result)
    except Exception as e:
        # googletrans can fail intermittently due to network/ban issues
        return make_response(jsonify({'error': 'Translation failed', 'details': str(e)}), 502)
