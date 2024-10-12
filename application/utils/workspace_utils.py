#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it

import uuid
from datetime import datetime

import bleach
from flask import request

from application import db
from application.models import Postit
from application.models import WorkSpaces


class WorkspaceUtils:
    @staticmethod
    def add_note(title, note, workspace_id):
        is_success = True
        unique_id = uuid.uuid4().hex
        workspace_record = WorkSpaces.query.filter_by(uuid=workspace_id).first()
        if workspace_record:
            if unique_id:
                new_note = Postit(title=title,
                                  note=note,
                                  uuid=unique_id,
                                  workspace_id=workspace_record.id,
                                  active=True)
                db.session.add(new_note)
                db.session.commit()
            else:
                is_success = False
        else:
            is_success = False
        return is_success

    @staticmethod
    def edit_note(title, note, uuid, workspace_uuid):
        workspace_rec = WorkSpaces.query.filter_by(uuid=workspace_uuid, active=True).first()
        workspace_edit = Postit.query.filter_by(uuid=uuid, workspace_id=workspace_rec.id).first()
        edited_note = note
        edited_title = title
        workspace_edit.title = edited_title
        workspace_edit.note = edited_note
        db.session.commit()

    @staticmethod
    def delete_note(id, workspace_uuid):
        is_success = True
        workspace_rec = WorkSpaces.query.filter_by(uuid=workspace_uuid, active=True).first()
        if workspace_rec:
            note_delete = Postit.query.filter_by(id=id, workspace_id=workspace_rec.id).first()
            note_delete.active = False
            db.session.commit()
        else:
            is_success = False
        return is_success

    @staticmethod
    def get_workspace_notes(workspace_uuid, mode='default'):
        postits_records = []
        mode = bleach.clean(mode)
        workspace_rec = WorkSpaces.query.filter_by(uuid=workspace_uuid).first()
        if workspace_rec:
            postit_query = Postit.query.filter_by(workspace_id=workspace_rec.id)
            if mode == 'active':
                postit_query = postit_query.filter(Postit.active == True)
            elif mode == 'deactive':
                postit_query = postit_query.filter(Postit.active == False)

            postits_records = postit_query.all()

        return postits_records

    @staticmethod
    def create_workspace():
        unique_id = uuid.uuid4().hex
        requester_ip = request.access_route[0]
        new_workspace = WorkSpaces(uuid=unique_id,
                                   insert_date=datetime.utcnow(),
                                   created_ip=requester_ip)
        db.session.add(new_workspace)
        db.session.commit()
        return unique_id
