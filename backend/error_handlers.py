"""
DOSYA ADI: error_handlers.py
AMAÇ: FastAPI için merkezi hata yakalama ve yanıt üretimi sağlamak.
NE YAPAR:
  - Uygulama istisnalarını tek noktadan yakalar.
  - Türkçe ve yönlendirici hata mesajları döndürür.
BAĞIMLILIKLAR:
  - fastapi
  - api.error_messages
  - exceptions
SON DEĞİŞİKLİK: 17.01.2026
"""
from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api import error_messages as mesajlar
from exceptions import UygulamaHatasi

logger = logging.getLogger(__name__)


def _hata_cevabi(
    status_code: int,
    hata: str,
    detay: str | None = None,
    kod: str | None = None,
) -> JSONResponse:
    """Giriş: HTTP kodu, hata mesajı ve opsiyonel detay.

    Çıkış: JSONResponse.
    İşleyiş: Standart hata gövdesi oluşturur.
    """
    payload: dict[str, Any] = {"hata": hata}
    if detay:
        payload["detay"] = detay
    if kod:
        payload["kod"] = kod
    return JSONResponse(status_code=status_code, content=payload)


def _dogrulama_detayi(errors: list[dict[str, Any]]) -> str | None:
    """Giriş: Pydantic hata listesi.

    Çıkış: Özet detay metni.
    İşleyiş: Hatalı alanları Türkçe listeler.
    """
    alanlar: list[str] = []
    for error in errors:
        loc = error.get("loc") or []
        temiz = [
            str(item)
            for item in loc
            if item not in {"body", "query", "path", "header", "cookie"}
        ]
        if temiz:
            alanlar.append(".".join(temiz))
    if not alanlar:
        return None
    benzersiz = sorted(set(alanlar))
    return "Hatalı alanlar: " + ", ".join(benzersiz)


def register_error_handlers(app: FastAPI) -> None:
    """Giriş: FastAPI uygulaması.

    Çıkış: yok.
    İşleyiş: Uygulamaya hata yakalayıcılarını bağlar.
    """

    @app.exception_handler(UygulamaHatasi)
    async def handle_app_exception(
        _: Request,
        exc: UygulamaHatasi,
    ) -> JSONResponse:
        """Giriş: Request ve UygulamaHatasi.

        Çıkış: JSONResponse.
        İşleyiş: Uygulama hatasını standart yanıta çevirir.
        """
        logger.warning("Uygulama hatası: %s", exc)
        response = exc.as_response()
        return _hata_cevabi(
            status_code=exc.status_code,
            hata=response.hata,
            detay=response.detay,
            kod=response.kod,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        _: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """Giriş: Request ve doğrulama hatası.

        Çıkış: JSONResponse.
        İşleyiş: Doğrulama hatasını Türkçe döndürür.
        """
        detay = _dogrulama_detayi(exc.errors())
        logger.info("Doğrulama hatası: %s", detay or "detay yok")
        return _hata_cevabi(422, mesajlar.DOGRULAMA_HATASI, detay=detay)

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(
        _: Request,
        exc: StarletteHTTPException,
    ) -> JSONResponse:
        """Giriş: Request ve HTTP hatası.

        Çıkış: JSONResponse.
        İşleyiş: HTTPException mesajını normalize eder.
        """
        detail_raw = exc.detail
        if isinstance(detail_raw, str):
            return _hata_cevabi(exc.status_code, detail_raw)

        mesaj = _durum_kodu_mesaji(exc.status_code)
        detay = None
        if detail_raw is not None:
            try:
                detay = json.dumps(detail_raw, ensure_ascii=False)
            except TypeError:
                detay = str(detail_raw)
        return _hata_cevabi(exc.status_code, mesaj, detay=detay)

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(
        _: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Giriş: Request ve genel hata.

        Çıkış: JSONResponse.
        İşleyiş: Beklenmeyen hataları yakalar.
        """
        logger.exception("Beklenmeyen hata: %s", exc)
        return _hata_cevabi(500, mesajlar.BEKLENMEYEN_HATA)


def _durum_kodu_mesaji(status_code: int) -> str:
    """Giriş: HTTP durum kodu.

    Çıkış: Türkçe hata mesajı.
    İşleyiş: Kodlara göre kullanıcı yönlendirmesi üretir.
    """
    if status_code == 400:
        return mesajlar.DOGRULAMA_HATASI
    if status_code == 401:
        return mesajlar.YETKISIZ
    if status_code == 403:
        return mesajlar.ERISIM_ENGELLENDI
    if status_code == 404:
        return mesajlar.KAYNAK_BULUNAMADI
    if status_code == 422:
        return mesajlar.DOGRULAMA_HATASI
    if status_code == 503:
        return mesajlar.BAGLANTI_HATASI
    if status_code == 504:
        return mesajlar.ZAMAN_ASIMI
    return mesajlar.SUNUCU_HATASI
