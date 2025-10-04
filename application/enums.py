#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it
"""Enum definitions used across the application."""

import enum


class PostStatus(enum.IntEnum):
    NEW = 0
    PROGRESS = 1
    DONE = 2
