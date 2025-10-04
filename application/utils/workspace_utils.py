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
    def _parse_status(value: Optional[str]) -> int:
        try:
            if value is None or value == '':
                return Postit.status.default.arg if hasattr(Postit.status, 'default') else 0
            v = str(value).strip().lower()
            # allow numeric strings
            if v.isdigit():
                iv = int(v)
                return iv if iv in (0, 1, 2) else 0
            mapping = {
                'new': 0,
                'progress': 1,
                'in_progress': 1,
                'in-progress': 1,
                'done': 2,
            }
            return mapping.get(v, 0)
        except Exception:
            return 0

    @staticmethod
    def _parse_rank(value: Optional[str]) -> int:
        try:
            iv = int(value) if value is not None and value != '' else 0
        except Exception:
            iv = 0
        return max(0, min(5, iv))

    @staticmethod
    def add_note(title: str, note: str, workspace_id: str, color: str = '#fff', status: Optional[str] = None, rank: Optional[str] = None) -> bool:
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
                    status=WorkspaceUtils._parse_status(status),
                    rank=WorkspaceUtils._parse_rank(rank),
                )
                db.session.add(new_note)
                db.session.commit()
            else:
                is_success = False
        else:
            is_success = False
        return is_success

    @staticmethod
    def edit_note(title: str, note: str, note_id: str, workspace_id: str, color: Optional[str] = None, status: Optional[str] = None, rank: Optional[str] = None) -> Dict[str, Any]:
        """Edit an existing note. Optionally updates color, status and rank.

        Returns a dict with key 'is_success'. Logic unchanged.
        """
        response: Dict[str, Any] = {}
        workspace = WorkSpaces.query.filter_by(uuid=workspace_id, active=True).first()
        postit = Postit.query.filter_by(uuid=note_id, workspace_id=workspace.id).first()
        if not postit:
            response['is_success'] = False
            return response

        # Only update title/note when explicitly provided to avoid clearing them on partial updates
        if title is not None:
            postit.title = title
        if note is not None:
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

        # Update status and rank if provided
        if status is not None and status != '':
            postit.status = WorkspaceUtils._parse_status(status)
        if rank is not None and rank != '':
            postit.rank = WorkspaceUtils._parse_rank(rank)

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
    def get_workspace_notes(workspace_uuid: str, mode: str = 'default', rank: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return notes for a workspace, filtered by mode, and optionally by rank/status; sorted by id desc.

        Supported modes: 'active', 'disabled'/'deactive', 'all', '' (default -> all).
        Optional filters:
        - rank: 1–5 (ints or numeric strings). 0 or empty means no filter.
        - status: 0=new, 1=in progress, 2=done (ints or strings like 'new', 'progress', 'done').
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
            elif mode in ('all', '', 'default'):
                pass  # no additional filter
            # any other mode: default to all

            # Apply optional rank/status filters if provided
            try:
                if rank is not None and str(rank) != '':
                    parsed_rank = WorkspaceUtils._parse_rank(rank)
                    if parsed_rank > 0:
                        postit_query = postit_query.filter(Postit.rank == parsed_rank)
            except Exception:
                pass
            try:
                if status is not None and str(status) != '':
                    parsed_status = WorkspaceUtils._parse_status(status)
                    postit_query = postit_query.filter(Postit.status == parsed_status)
            except Exception:
                pass

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
                    'status': rec.status,
                    'rank': rec.rank,
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
