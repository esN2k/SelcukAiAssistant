"""
DOSYA ADI: exceptions.py
AMAÇ: Uygulamaya özel hata sınıflarını merkezi olarak tanımlamak.
NE YAPAR:
  - Türkçe hata mesajları taşıyan exception sınıfları sağlar.
  - Hataları HTTP status kodlarıyla eşler.
BAĞIMLILIKLAR:
  - api.error_messages
SON DEĞİŞİKLİK: 17.01.2026
"""
from __future__ import annotations

from dataclasses import dataclass

from api import error_messages as mesajlar


@dataclass
class HataDetayi:
    """Giriş: Hata bilgileri.

    Çıkış: HataDetayi nesnesi.
    İşleyiş: Yanıt gövdesinde kullanılacak alanları taşır.
    """

    hata: str
    detay: str | None = None
    kod: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        """Giriş: nesne alanları.

        Çıkış: sözlük.
        İşleyiş: JSON yanıtına uygun hale getirir.
        """
        payload: dict[str, str | None] = {"hata": self.hata}
        if self.detay:
            payload["detay"] = self.detay
        if self.kod:
            payload["kod"] = self.kod
        return payload


class UygulamaHatasi(Exception):
    """Giriş: Hata mesajı ve durum kodu.

    Çıkış: Exception.
    İşleyiş: HTTP status ve hata detayını taşır.
    """

    def __init__(
        self,
        mesaj: str,
        status_code: int = 500,
        detay: str | None = None,
        kod: str | None = None,
    ) -> None:
        super().__init__(mesaj)
        self.status_code = status_code
        self.detay = detay
        self.kod = kod
        self.mesaj = mesaj

    def as_response(self) -> HataDetayi:
        """Giriş: Sınıf alanları.

        Çıkış: HataDetayi nesnesi.
        İşleyiş: Hata yanıtı için payload hazırlar.
        """
        return HataDetayi(hata=self.mesaj, detay=self.detay, kod=self.kod)


class DogrulamaHatasi(UygulamaHatasi):
    """Giriş: Detay mesajı.

    Çıkış: Doğrulama hatası.
    İşleyiş: 422 status kodu ile hata üretir.
    """

    def __init__(self, detay: str | None = None) -> None:
        super().__init__(
            mesaj=mesajlar.DOGRULAMA_HATASI,
            status_code=422,
            detay=detay,
            kod="dogrulama_hatasi",
        )


class BaglantiHatasi(UygulamaHatasi):
    """Giriş: Detay mesajı.

    Çıkış: Bağlantı hatası.
    İşleyiş: 503 status kodu ile hata üretir.
    """

    def __init__(self, detay: str | None = None) -> None:
        super().__init__(
            mesaj=mesajlar.BAGLANTI_HATASI,
            status_code=503,
            detay=detay,
            kod="baglanti_hatasi",
        )


class ZamanAsimiHatasi(UygulamaHatasi):
    """Giriş: Detay mesajı.

    Çıkış: Zaman aşımı hatası.
    İşleyiş: 504 status kodu ile hata üretir.
    """

    def __init__(self, detay: str | None = None) -> None:
        super().__init__(
            mesaj=mesajlar.ZAMAN_ASIMI,
            status_code=504,
            detay=detay,
            kod="zaman_asimi",
        )


class SunucuHatasi(UygulamaHatasi):
    """Giriş: Detay mesajı.

    Çıkış: Sunucu hatası.
    İşleyiş: 500 status kodu ile hata üretir.
    """

    def __init__(self, detay: str | None = None) -> None:
        super().__init__(
            mesaj=mesajlar.SUNUCU_HATASI,
            status_code=500,
            detay=detay,
            kod="sunucu_hatasi",
        )


class KaynakBulunamadiHatasi(UygulamaHatasi):
    """Giriş: Detay mesajı.

    Çıkış: 404 hatası.
    İşleyiş: Kaynak bulunamadı hatası üretir.
    """

    def __init__(self, detay: str | None = None) -> None:
        super().__init__(
            mesaj=mesajlar.KAYNAK_BULUNAMADI,
            status_code=404,
            detay=detay,
            kod="kaynak_bulunamadi",
        )


class YetkiHatasi(UygulamaHatasi):
    """Giriş: Detay mesajı.

    Çıkış: Yetki hatası.
    İşleyiş: 401 status kodu ile hata üretir.
    """

    def __init__(self, detay: str | None = None) -> None:
        super().__init__(
            mesaj=mesajlar.YETKISIZ,
            status_code=401,
            detay=detay,
            kod="yetkisiz",
        )


class ErisimEngellendiHatasi(UygulamaHatasi):
    """Giriş: Detay mesajı.

    Çıkış: Erişim engeli hatası.
    İşleyiş: 403 status kodu ile hata üretir.
    """

    def __init__(self, detay: str | None = None) -> None:
        super().__init__(
            mesaj=mesajlar.ERISIM_ENGELLENDI,
            status_code=403,
            detay=detay,
            kod="erisim_engellendi",
        )
