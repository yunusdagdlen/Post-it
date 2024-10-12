#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it

from application import db


class Postit(db.Model):
    __tablename__ = 'postit'
    id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False, index=True)
    active = db.Column(db.Boolean, default=True)
    title = db.Column(db.String)
    note = db.Column(db.Text)
    uuid = db.Column(db.String, nullable=False)


class WorkSpaces(db.Model):
    __tablename__ = 'workspace'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_ip = db.Column(db.String)
    insert_date = db.Column(db.DateTime)
