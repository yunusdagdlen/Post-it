#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Translation utilities centralized in one module.

Provides a TranslationUtils class that wraps the googletrans client so the rest
of the app can translate text without being tied to a specific provider.
"""
from typing import Dict, Any

try:
    # googletrans may have different import paths depending on version
    from googletrans import Translator  # type: ignore
except Exception:  # pragma: no cover - fallback name used by some forks
    from google_trans_new import google_translator as Translator  # type: ignore


class TranslationUtils:
    _translator = None

    @classmethod
    def _get_client(cls):
        if cls._translator is None:
            # Initialize lazily to avoid startup cost when feature not used
            try:
                cls._translator = Translator()
            except Exception as e:
                # Re-raise to be handled by the caller uniformly
                raise e
        return cls._translator

    @classmethod
    def translate(cls, text: str, source: str = 'auto', target: str = 'en') -> Dict[str, Any]:
        """Translate the given text using googletrans.

        Returns a dict with keys: translation (str) and alternatives (list).
        googletrans doesn't provide alternatives; we return an empty list for compatibility.
        """
        if not text:
            return {"translation": "", "alternatives": []}
        translator = cls._get_client()
        # googletrans uses src/dest language codes
        try:
            # Some versions return an object with .text; others may return string
            result = translator.translate(text, src=source or 'auto', dest=target)
            translated = getattr(result, 'text', None) or str(result)
            return {"translation": translated, "alternatives": []}
        except Exception as e:
            # Surface error to caller; they can map to HTTP codes/messages
            raise e
