#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it

from flask import render_template, request, make_response

from application.controller import mod_pages
from application.utils.workspace_utils import WorkspaceUtils


@mod_pages.route('/workspace_table')
def workspace_table():
    workspace_uuid = request.args.get('workspace_uuid')
    if not workspace_uuid:
        workspace_uuid = request.cookies.get('workspace_uuid')
    if not workspace_uuid:
        workspace_uuid = WorkspaceUtils.create_workspace()

    notes_list = []
    if workspace_uuid:
        postits = WorkspaceUtils.get_workspace_notes(workspace_uuid=workspace_uuid)
        for postit in postits:
            notes_list.append({
                'id': postit.id,
                'title': postit.title,
                'note_list': postit.note.splitlines(),
                'note': postit.note,
                'uuid': postit.uuid
            })
    resp = make_response(render_template('workspace_table.html', notes_list=notes_list))
    resp.set_cookie('workspace_uuid', workspace_uuid)
    return resp