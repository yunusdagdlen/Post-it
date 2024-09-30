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

    resp = make_response(render_template('workspace_table.html'))
    resp.set_cookie('workspace_uuid', workspace_uuid)
    return resp