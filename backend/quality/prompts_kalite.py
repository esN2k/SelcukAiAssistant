"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: prompts_kalite.py                                                      ║
║  AMAÇ: Yüksek kaliteli LLM cevapları için gelişmiş prompt şablonları          ║
║  KULLANIM: Detaylı, kaynaklı ve doğru cevaplar üretmek için                   ║
╚════════════════════════════════════════════════════════════════════════════════╝

AÇIKLAMA:
─────────
Bu modül, LLM'den maksimum kaliteli cevaplar almak için optimize edilmiş
prompt şablonları içerir.

ÖNCELİK SIRASI:
1. DOĞRULUK - Yanlış bilgi vermek YASAK
2. DETAY - Yüzeysel cevaplar YASAK
3. KAYNAK - Kaynaksız iddia YASAK
4. GÜNCELLİK - Eski bilgi YASAK
5. HIZ - Ama kaliteyi feda etme
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# KRİTİK KURALLAR - LLM'e her zaman bunları hatırlat
# ═══════════════════════════════════════════════════════════════════════════════

KRITIK_KURALLAR_TR = """
## 🎯 KRİTİK KURALLAR (Mutlaka Uy!)

### 1. DOĞRULUK (%100 Zorunlu)
- **SADECE** verilen CONTEXT'teki bilgileri kullan
- Context'te yoksa açıkça belirt: "Bu konuda kaynaklarda bilgi bulamadım"
- **ASLA** bilgi uydurma, tahmin etme veya varsayma
- Emin olmadığın bilgileri "muhtemelen", "olabilir" gibi kelimelerle belirt

### 2. DETAY (Kapsamlı Cevap)
- Kısa ve yetersiz cevaplar YASAK
- Her konuyu mümkün olduğunca detaylı açıkla
- Liste ve tablo kullan (okunabilirlik için)
- Tarih, sayı ve ölçü bilgilerini dahil et

### 3. KAYNAK (Her İddia Kaynaklı)
- Her önemli bilginin sonunda kaynak göster
- Format: [Kaynak: Dosya/Belge Adı]
- Birden fazla kaynak varsa hepsini belirt
- Kaynak yoksa cevap verme

### 4. GÜNCELLİK (Tarih Bilgisi)
- Verilen bilginin ne zaman güncellendiğini belirt
- Akademik yıl/dönem bilgisini ekle
- Eski bilgi kullanıyorsan uyar
"""

KRITIK_KURALLAR_EN = """
## 🎯 CRITICAL RULES (Must Follow!)

### 1. ACCURACY (100% Required)
- Use ONLY information from the provided CONTEXT
- If not in context, state clearly: "I couldn't find this information in the sources"
- NEVER fabricate, guess, or assume information
- Use "probably", "may be" for uncertain information

### 2. DETAIL (Comprehensive Answer)
- Short and insufficient answers are FORBIDDEN
- Explain each topic as detailed as possible
- Use lists and tables (for readability)
- Include dates, numbers, and measurements

### 3. CITATION (Every Claim Cited)
- Show source after every important piece of information
- Format: [Source: File/Document Name]
- If multiple sources, mention all
- No citation = No answer

### 4. FRESHNESS (Date Information)
- State when the information was updated
- Include academic year/semester info
- Warn if using old information
"""


# ═══════════════════════════════════════════════════════════════════════════════
# CEVAP FORMAT ŞABLONLARI
# ═══════════════════════════════════════════════════════════════════════════════

CEVAP_FORMAT_TR = """
## 📋 CEVAP FORMATI

Cevabını şu yapıda ver:

### 1. Direkt Cevap (İlk Cümle)
Sorunun ana cevabını ilk cümlede ver.

### 2. Detaylı Açıklama
- Konuyu detaylıca açıkla
- Liste ve maddeler kullan
- Tablo gerekiyorsa tablo yap

### 3. Ek Bilgiler (Varsa)
- İlgili diğer bilgileri ekle
- Uyarı veya notları belirt

### 4. Kaynak ve Tarih
- Kullandığın kaynakları listele
- Bilginin güncellik tarihini yaz

---

### ✅ İYİ CEVAP ÖRNEĞİ:

**Soru:** "Bilgisayar Mühendisliği zorunlu dersleri nelerdir?"

**Cevap:**
Bilgisayar Mühendisliği bölümünün zorunlu dersleri şunlardır:

**1. Yarıyıl:**
| Ders Kodu | Ders Adı | Kredi | AKTS |
|-----------|----------|-------|------|
| MAT101 | Matematik I | 4 | 6 |
| FIZ101 | Fizik I | 3 | 5 |
| BM101 | Programlamaya Giriş | 4 | 6 |

**2. Yarıyıl:**
| Ders Kodu | Ders Adı | Kredi | AKTS |
|-----------|----------|-------|------|
| MAT102 | Matematik II | 4 | 6 |
| FIZ102 | Fizik II | 3 | 5 |
| BM102 | Nesne Yönelimli Programlama | 4 | 6 |

**Önemli Notlar:**
- Tüm zorunlu derslerden geçmek mezuniyet için şarttır
- AKTS toplam kredisi 240 olmalıdır
- Staj zorunludur (40 iş günü)

📚 **Kaynak:** AKTS Kataloğu 2024-2025, Bologna Bilgi Sistemi
📅 **Güncellenme:** 15 Eylül 2024

---

### ❌ KÖTÜ CEVAP ÖRNEĞİ:

"Zorunlu dersler var, web sitesine bakın."

Bu cevap YASAKTIR çünkü:
- Detay yok
- Kaynak yok
- Faydalı bilgi yok
"""

CEVAP_FORMAT_EN = """
## 📋 ANSWER FORMAT

Structure your answer as follows:

### 1. Direct Answer (First Sentence)
Give the main answer in the first sentence.

### 2. Detailed Explanation
- Explain the topic in detail
- Use lists and bullet points
- Create tables if needed

### 3. Additional Information (If Any)
- Add related information
- Include warnings or notes

### 4. Source and Date
- List the sources you used
- Write the freshness date of information
"""


# ═══════════════════════════════════════════════════════════════════════════════
# GELİŞMİŞ SİSTEM PROMPTLARI
# ═══════════════════════════════════════════════════════════════════════════════

def sistem_promptu_olustur(
    dil: str = "tr",
    context: str = "",
    kaynaklar: Optional[List[str]] = None,
    strict_mod: bool = True,
) -> str:
    """
    Gelişmiş sistem promptu oluştur.
    
    Args:
        dil: Dil kodu ('tr' veya 'en')
        context: RAG context'i
        kaynaklar: Kaynak listesi
        strict_mod: Strict mod aktif mi?
    
    Returns:
        Gelişmiş sistem promptu
    """
    if dil.lower().startswith("en"):
        kurallar = KRITIK_KURALLAR_EN
        format_sablonu = CEVAP_FORMAT_EN
        rol = "You are Selçuk University's official AI assistant."
        context_baslik = "CONTEXT (Trusted Sources)"
        strict_uyari = "STRICT MODE: ONLY use information from the provided context!"
    else:
        kurallar = KRITIK_KURALLAR_TR
        format_sablonu = CEVAP_FORMAT_TR
        rol = "Sen Selçuk Üniversitesi'nin resmi AI asistanısın."
        context_baslik = "CONTEXT (Güvenilir Kaynaklar)"
        strict_uyari = "STRICT MOD: SADECE verilen context'teki bilgileri kullan!"
    
    prompt = f"""# {rol}

{kurallar}

{format_sablonu}

"""
    
    if strict_mod:
        prompt += f"\n⚠️ **{strict_uyari}**\n\n"
    
    if context:
        prompt += f"""
---
## 📚 {context_baslik}

{context}

---
"""
    
    if kaynaklar:
        kaynak_listesi = "\n".join([f"- {k}" for k in kaynaklar])
        kaynak_baslik = "Available Sources" if dil.lower().startswith("en") else "Mevcut Kaynaklar"
        prompt += f"\n### {kaynak_baslik}:\n{kaynak_listesi}\n"
    
    return prompt


def kullanici_sorusu_sablonu(
    soru: str,
    context: str = "",
    dil: str = "tr",
) -> str:
    """
    Kullanıcı sorusu için şablon oluştur.
    
    Args:
        soru: Kullanıcı sorusu
        context: RAG context'i
        dil: Dil kodu
    
    Returns:
        Formatlanmış kullanıcı sorusu
    """
    if dil.lower().startswith("en"):
        soru_baslik = "QUESTION"
        context_baslik = "CONTEXT (Trusted Sources)"
        talimat = "Please provide a DETAILED and CITED answer using the context above."
    else:
        soru_baslik = "SORU"
        context_baslik = "CONTEXT (Güvenilir Kaynaklar)"
        talimat = "Lütfen yukarıdaki context'i kullanarak DETAYLI ve KAYNAKLI cevap ver."
    
    if context:
        return f"""
## 📚 {context_baslik}:

{context}

---

## ❓ {soru_baslik}: {soru}

{talimat}
"""
    else:
        return f"## ❓ {soru_baslik}: {soru}"


def hata_mesaji_olustur(
    hata_tipi: str,
    dil: str = "tr",
    detay: str = "",
) -> str:
    """
    Standart hata mesajı oluştur.
    
    Args:
        hata_tipi: Hata tipi ('kaynak_yok', 'bilgi_yok', 'belirsiz')
        dil: Dil kodu
        detay: Ek detay
    
    Returns:
        Hata mesajı
    """
    mesajlar_tr = {
        "kaynak_yok": "Bu konuda kaynaklarda bilgi bulamadım. Lütfen ilgili birime (Öğrenci İşleri, Dekanlık vb.) danışınız.",
        "bilgi_yok": "Bu soruyla ilgili yeterli bilgiye sahip değilim. Güncel bilgi için Selçuk Üniversitesi resmi web sitesini ziyaret edebilirsiniz: https://www.selcuk.edu.tr",
        "belirsiz": "Bu konuda kesin bilgi veremiyorum. Doğru bilgi için ilgili akademik birime başvurmanızı öneririm.",
        "eski_bilgi": "Bu bilgi güncel olmayabilir. Güncel bilgi için resmi kaynakları kontrol ediniz.",
    }
    
    mesajlar_en = {
        "kaynak_yok": "I couldn't find information about this topic in the sources. Please consult the relevant department.",
        "bilgi_yok": "I don't have sufficient information about this question. For up-to-date information, please visit: https://www.selcuk.edu.tr",
        "belirsiz": "I cannot provide definitive information on this topic. I recommend contacting the relevant academic unit.",
        "eski_bilgi": "This information may not be current. Please check official sources for up-to-date information.",
    }
    
    mesajlar = mesajlar_en if dil.lower().startswith("en") else mesajlar_tr
    mesaj = mesajlar.get(hata_tipi, mesajlar["bilgi_yok"])
    
    if detay:
        mesaj += f"\n\n{detay}"
    
    return mesaj


# ═══════════════════════════════════════════════════════════════════════════════
# CONTEXT ZENGİNLEŞTİRME
# ═══════════════════════════════════════════════════════════════════════════════

def context_zenginlestir(
    contextler: List[Dict[str, Any]],
    dil: str = "tr",
) -> str:
    """
    Context listesini zenginleştirilmiş formata dönüştür.
    
    Args:
        contextler: Context sözlük listesi
        dil: Dil kodu
    
    Returns:
        Zenginleştirilmiş context metni
    """
    if not contextler:
        return ""
    
    kaynak_baslik = "Source" if dil.lower().startswith("en") else "Kaynak"
    tarih_baslik = "Date" if dil.lower().startswith("en") else "Tarih"
    guven_baslik = "Confidence" if dil.lower().startswith("en") else "Güven"
    
    parcalar = []
    
    for i, ctx in enumerate(contextler, 1):
        icerik = ctx.get("content") or ctx.get("text", "")
        metadata = ctx.get("metadata", {})
        skor = ctx.get("score", 0)
        
        kaynak = metadata.get("source", "Bilinmiyor")
        tarih = metadata.get("date", "")
        guven = metadata.get("confidence", skor)
        
        # Kaynak adını kısalt
        from pathlib import Path
        kaynak_kisa = Path(kaynak).stem if kaynak else "Bilinmiyor"
        
        # Format
        parca = f"""
### [{i}] {kaynak_baslik}: {kaynak_kisa}
"""
        if tarih:
            parca += f"📅 {tarih_baslik}: {tarih}\n"
        
        parca += f"📊 {guven_baslik}: {guven:.0%}\n\n"
        parca += f"{icerik}\n"
        
        parcalar.append(parca)
    
    return "\n---\n".join(parcalar)


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "KRITIK_KURALLAR_TR",
    "KRITIK_KURALLAR_EN",
    "CEVAP_FORMAT_TR",
    "CEVAP_FORMAT_EN",
    "sistem_promptu_olustur",
    "kullanici_sorusu_sablonu",
    "hata_mesaji_olustur",
    "context_zenginlestir",
]
