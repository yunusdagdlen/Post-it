#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it

import uuid
from application import db
from application.models import Postit
from application.models import WorkSpaces


class WorkspaceUtils:
    @staticmethod
    def add_note(title, note, workspace_id,color):
        is_success = True
        unique_id = uuid.uuid4().hex
        workspace_record = WorkSpaces.query.filter_by(uuid=workspace_id).first()
        if workspace_record:
            if unique_id:
                extra_info = {'postit_color':color}
                new_note = Postit(title=title,
                                  note=note,
                                  uuid=unique_id,
                                  workspace_id=workspace_record.id,
                                  extra_info = extra_info,
                                  active=True)
                db.session.add(new_note)
                db.session.commit()
            else:
                is_success = False
        else:
            is_success = False
        return is_success

    @staticmethod
    def edit_note(title, note, note_id, workspace_id):
        response = {}
        workspace_rec = WorkSpaces.query.filter_by(uuid=workspace_id, active=True).first()
        workspace_edit = Postit.query.filter_by(uuid=note_id, workspace_id=workspace_rec.id).first()
        workspace_edit.title = title
        workspace_edit.note = note
        try:
            db.session.commit()
            response['is_success'] = True
        except:
            response['is_success'] = False

        return response


    @staticmethod
    def delete_note(id, workspace_uuid):
        is_success = True
        workspace_rec = WorkSpaces.query.filter_by(uuid=workspace_uuid, active=True).first()
        if workspace_rec:
            note_delete = Postit.query.filter_by(id=id, workspace_id=workspace_rec.id).first()
            db.session.delete(note_delete)
            db.session.commit()
        else:
            is_success = False
        return is_success

    @staticmethod
    def get_workspace_notes(workspace_id):
        return_list = []
        workspace_rec = WorkSpaces.query.filter_by(uuid=workspace_id).first()

        if workspace_rec:
            postits_records = Postit.query.filter_by(workspace_id=workspace_rec.id).all()

            for rec in postits_records:
                return_list.append({
                    'id': rec.id,
                    'workspace_id': rec.workspace_id,
                    'active': rec.active,
                    'title': rec.title,
                    'note': rec.note,
                    'uuid': rec.uuid,
                    'extra_info': rec.extra_info,
                })
        return_list = sorted(return_list, key=lambda x: x['id'])
        return return_list

    @staticmethod
    def create_workspace():
        unique_id = uuid.uuid4().hex
        new_workspace = WorkSpaces(uuid=unique_id)
        db.session.add(new_workspace)
        db.session.commit()
        return unique_id
