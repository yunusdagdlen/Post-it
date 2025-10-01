#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it

import uuid
from datetime import datetime

import bleach
from flask import request, current_app, session

from application import db
from application.models import Postit
from application.models import WorkSpaces
from application.thirdparty.ipwhois import IPWhois


class WorkspaceUtils:
    @staticmethod
    def add_note(title, note, workspace_id, color='#fff'):
        is_success = True
        unique_id = uuid.uuid4().hex
        workspace_record = WorkSpaces.query.filter_by(uuid=workspace_id).first()
        if workspace_record:
            if unique_id:
                extra_info = {'postit_color': color}
                new_note = Postit(title=title,
                                  note=note,
                                  uuid=unique_id,
                                  workspace_id=workspace_record.id,
                                  extra_info=extra_info,
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
        workspace_edit.active = True
        try:
            db.session.commit()
            response['is_success'] = True
        except:
            response['is_success'] = False

        return response

    @staticmethod
    def delete_note(id, workspace_uuid):
        response = {'is_success': True}
        workspace_rec = WorkSpaces.query.filter_by(uuid=workspace_uuid, active=True).first()
        if workspace_rec:
            postit_record = Postit.query.filter(Postit.uuid == id, Postit.workspace_id == workspace_rec.id).first()
            postit_record.is_deleted = True
            db.session.commit()
        else:
            response['is_success'] = False
        return response

    @staticmethod
    def disable_note(id, workspace_uuid):
        response = {'is_success': True}
        workspace_rec = WorkSpaces.query.filter_by(uuid=workspace_uuid, active=True).first()
        if workspace_rec:
            note_delete = Postit.query.filter_by(uuid=id, workspace_id=workspace_rec.id).first()
            if note_delete.active:
                note_delete.active = False
            else:
                note_delete.active = True
            db.session.commit()
        else:
            response['is_success'] = False
        return response

    @staticmethod
    def get_workspace_notes(workspace_uuid, mode='default'):
        return_list = []
        mode = bleach.clean(mode)
        workspace_rec = WorkSpaces.query.filter_by(uuid=workspace_uuid).first()
        if workspace_rec:
            postit_query = Postit.query.filter(Postit.workspace_id==workspace_rec.id, Postit.is_deleted.isnot(True))
            if mode == 'active':
                postit_query = postit_query.filter(Postit.active == True)
            elif mode == 'deactive':
                postit_query = postit_query.filter(Postit.active == False)

            postits_records = postit_query.all()
            for rec in postits_records:
                return_list.append({
                    'id': rec.id,
                    'workspace_id': rec.workspace_id,
                    'active': rec.active,
                    'title': rec.title,
                    'note': rec.note,
                    'notes_by_line': rec.note.splitlines(),
                    'uuid': rec.uuid,
                    'extra_info': rec.extra_info,
                })
        return_list = sorted(return_list, key=lambda x: x['id'])
        return return_list

    @staticmethod
    def create_workspace():
        unique_id = uuid.uuid4().hex
        requester_ip = request.access_route[0]
        ipwhois_client = IPWhois(current_app.config)

        ipwhois_info = ipwhois_client.get_iphois_info(requester_ip)

        country = ipwhois_info.get('country', {}).get('iso_code', '') if ipwhois_info else ''
        new_workspace = WorkSpaces(uuid=unique_id,
                                   insert_date=datetime.utcnow(),
                                   created_ip=requester_ip,
                                   requester_whois=ipwhois_info,
                                   requester_country=country)
        db.session.add(new_workspace)
        db.session.commit()
        return unique_id

    @staticmethod
    def get_workspace_id():
        """Return workspace_id from session; create and persist if missing."""
        wid = session.get('workspace_id')
        if not wid:
            wid = WorkspaceUtils.create_workspace()
            session['workspace_id'] = wid
        return wid
