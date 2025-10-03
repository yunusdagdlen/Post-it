#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it
"""Utility helpers for workspace-related operations (CRUD, session helpers).
Logic is preserved; changes are cosmetic for readability and maintainability.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import bleach
from flask import current_app, request, session
from sqlalchemy.orm.attributes import flag_modified

from application import db
from application.models import Postit, WorkSpaces
from application.thirdparty.ipwhois import IPWhois


class WorkspaceUtils:
    """Namespace class for workspace utility methods."""

    @staticmethod
    def add_note(title: str, note: str, workspace_id: str, color: str = '#fff') -> bool:
        """Create a new note under a workspace.

        Returns True if created; False otherwise. Logic unchanged.
        """
        is_success = True
        unique_id = uuid.uuid4().hex
        workspace = WorkSpaces.query.filter_by(uuid=workspace_id).first()
        if workspace:
            if unique_id:  # keep shape identical to original
                extra_info = {
                    'postit_color': color,
                    'created_at': datetime.utcnow().isoformat(),
                }
                new_note = Postit(
                    title=title,
                    note=note,
                    uuid=unique_id,
                    workspace_id=workspace.id,
                    extra_info=extra_info,
                    active=True,
                )
                db.session.add(new_note)
                db.session.commit()
            else:
                is_success = False
        else:
            is_success = False
        return is_success

    @staticmethod
    def edit_note(title: str, note: str, note_id: str, workspace_id: str, color: Optional[str] = None) -> Dict[str, Any]:
        """Edit an existing note. Optionally updates color.

        Returns a dict with key 'is_success'. Logic unchanged.
        """
        response: Dict[str, Any] = {}
        workspace = WorkSpaces.query.filter_by(uuid=workspace_id, active=True).first()
        postit = Postit.query.filter_by(uuid=note_id, workspace_id=workspace.id).first()
        if not postit:
            response['is_success'] = False
            return response

        postit.title = title
        postit.note = note
        postit.active = True

        # Update color if provided
        if color is not None and color != '':
            try:
                extra = postit.extra_info or {}
                # ensure dict and preserve existing keys
                if not isinstance(extra, dict):
                    extra = {}
                extra['postit_color'] = color
                postit.extra_info = extra
                flag_modified(postit, 'extra_info')
            except Exception:
                # swallow any issues updating color to keep original flow
                pass
        try:
            db.session.commit()
            response['is_success'] = True
        except Exception:
            response['is_success'] = False
        return response

    @staticmethod
    def delete_note(id: str, workspace_uuid: str) -> Dict[str, Any]:
        """Soft-delete a note (mark as is_deleted)."""
        response: Dict[str, Any] = {'is_success': True}
        workspace = WorkSpaces.query.filter_by(uuid=workspace_uuid, active=True).first()
        if workspace:
            postit = Postit.query.filter(Postit.uuid == id, Postit.workspace_id == workspace.id).first()
            postit.is_deleted = True
            db.session.commit()
        else:
            response['is_success'] = False
        return response

    @staticmethod
    def disable_note(id: str, workspace_uuid: str) -> Dict[str, Any]:
        """Toggle note active flag (enable/disable)."""
        response: Dict[str, Any] = {'is_success': True}
        workspace = WorkSpaces.query.filter_by(uuid=workspace_uuid, active=True).first()
        if workspace:
            note = Postit.query.filter_by(uuid=id, workspace_id=workspace.id).first()
            if note.active:
                note.active = False
            else:
                note.active = True
            db.session.commit()
        else:
            response['is_success'] = False
        return response

    @staticmethod
    def get_workspace_notes(workspace_uuid: str, mode: str = 'default') -> List[Dict[str, Any]]:
        """Return notes for a workspace, filtered by mode; sorted by id desc by default.

        Supported modes: 'active', 'disabled'/'deactive', 'all', '' (default -> all).
        """
        results: List[Dict[str, Any]] = []
        mode = bleach.clean(mode)
        workspace = WorkSpaces.query.filter_by(uuid=workspace_uuid).first()
        if workspace:
            postit_query = Postit.query.filter(
                Postit.workspace_id == workspace.id,
                Postit.is_deleted.isnot(True),
            )
            # Support new and legacy mode names
            if mode == 'active':
                postit_query = postit_query.filter(Postit.active == True)
            elif mode in ('disabled', 'deactive'):
                postit_query = postit_query.filter(Postit.active == False)
            elif mode == 'all' or mode == '' or mode == 'default':
                pass  # no additional filter
            # any other mode: default to all

            for rec in postit_query.all():
                results.append({
                    'id': rec.id,
                    'workspace_id': rec.workspace_id,
                    'active': rec.active,
                    'title': rec.title,
                    'note': rec.note,
                    'notes_by_line': rec.note.splitlines(),
                    'uuid': rec.uuid,
                    'extra_info': rec.extra_info,
                })
        # Keep default sort: newest first
        results = sorted(results, key=lambda x: x['id'], reverse=True)
        return results

    @staticmethod
    def create_workspace() -> str:
        """Create a workspace and return its uuid."""
        unique_id = uuid.uuid4().hex
        requester_ip = request.access_route[0]
        ipwhois_client = IPWhois(current_app.config)
        ipwhois_info = ipwhois_client.get_iphois_info(requester_ip)

        country = ipwhois_info.get('country', {}).get('iso_code', '') if ipwhois_info else ''
        new_workspace = WorkSpaces(
            uuid=unique_id,
            insert_date=datetime.utcnow(),
            created_ip=requester_ip,
            requester_whois=ipwhois_info,
            requester_country=country,
        )
        db.session.add(new_workspace)
        db.session.commit()
        return unique_id

    @staticmethod
    def get_workspace_id(workspace_id: Optional[str] = None) -> str:
        """Return workspace_id from session; create and persist if missing."""
        wid = workspace_id or session.get('workspace_id')
        if not wid:
            wid = WorkspaceUtils.create_workspace()
            session['workspace_id'] = wid
        return wid
