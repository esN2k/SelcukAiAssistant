"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA ADI: tests/test_translator.py                                          ║
║  AMAÇ: Çeviri servisi için kapsamlı test suite                                ║
║  KULLANIM: pytest tests/test_translator.py -v                                 ║
║  BAĞIMLILIKLAR: pytest, services.translator                                    ║
║  YAZAN: esN2k - Selçuk Üniversitesi                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

DETAYLI AÇIKLAMA:
─────────────────
Bu test dosyası, Helsinki-NLP Opus-MT çeviri servisinin tüm özelliklerini test eder.

TEST KATEGORİLERİ:
1. Temel Çeviri: TR↔EN basit cümleler
2. Akademik Terimler: Üniversite terimleri korunmalı
3. Batch Çeviri: Toplu çeviri performansı
4. Özel İsimler: Selçuk, Konya gibi isimler korunmalı
5. Performans: < 200ms hedefi
6. Hata Yönetimi: Geçersiz girdi, boş metin
"""
import pytest
import time
from unittest.mock import MagicMock, patch
from services.translator import Translator


class TestBasicTranslation:
    """Temel çeviri fonksiyonelliği testleri."""

    def test_turkish_to_english_simple(self):
        """
        Test: Basit Türkçe → İngilizce çeviri
        Beklenen: Doğru çeviri
        """
        translator = Translator(use_gpu=False)
        
        # Mock model çıktısı
        with patch.object(translator.tr_en_model, 'generate') as mock_gen:
            with patch.object(translator.tr_en_tokenizer, 'decode') as mock_dec:
                mock_dec.return_value = "Hello world"
                
                result = translator.translate(
                    "Merhaba dünya",
                    source_lang="tr",
                    target_lang="en"
                )
                
                assert result == "Hello world"

    def test_english_to_turkish_simple(self):
        """
        Test: Basit İngilizce → Türkçe çeviri
        Beklenen: Doğru çeviri
        """
        translator = Translator(use_gpu=False)
        
        with patch.object(translator.en_tr_model, 'generate') as mock_gen:
            with patch.object(translator.en_tr_tokenizer, 'decode') as mock_dec:
                mock_dec.return_value = "Merhaba dünya"
                
                result = translator.translate(
                    "Hello world",
                    source_lang="en",
                    target_lang="tr"
                )
                
                assert result == "Merhaba dünya"

    def test_empty_text(self):
        """
        Test: Boş metin çevirisi
        Beklenen: Boş string dönmeli
        """
        translator = Translator(use_gpu=False)
        
        result = translator.translate("", "tr", "en")
        assert result == ""
        
        result = translator.translate("   ", "tr", "en")
        assert result == ""

    def test_unsupported_language_pair(self):
        """
        Test: Desteklenmeyen dil çifti
        Beklenen: ValueError fırlatmalı
        """
        translator = Translator(use_gpu=False)
        
        with pytest.raises(ValueError):
            translator.translate("Test", "tr", "fr")  # Fransızca desteklenmiyor


class TestAcademicTerms:
    """Akademik terim sözlüğü testleri."""

    def test_university_name_preservation(self):
        """
        Test: Üniversite adı korunmalı
        Beklenen: "Selçuk Üniversitesi" → "Selcuk University"
        """
        translator = Translator(use_gpu=False)
        
        # Sözlükten direkt çeviri
        result = translator.translate(
            "Selçuk Üniversitesi",
            source_lang="tr",
            target_lang="en"
        )
        
        assert result == "Selcuk University"

    def test_faculty_name_translation(self):
        """
        Test: Fakülte adı çevirisi
        Beklenen: "Teknoloji Fakültesi" → "Faculty of Technology"
        """
        translator = Translator(use_gpu=False)
        
        result = translator.translate(
            "Teknoloji Fakültesi",
            source_lang="tr",
            target_lang="en"
        )
        
        assert result == "Faculty of Technology"

    def test_department_name_translation(self):
        """
        Test: Bölüm adı çevirisi
        Beklenen: "Bilgisayar Mühendisliği" → "Computer Engineering"
        """
        translator = Translator(use_gpu=False)
        
        result = translator.translate(
            "Bilgisayar Mühendisliği",
            source_lang="tr",
            target_lang="en"
        )
        
        assert result == "Computer Engineering"

    def test_ai_term_translation(self):
        """
        Test: Yapay zeka terimi çevirisi
        Beklenen: "Yapay Zeka" → "Artificial Intelligence"
        """
        translator = Translator(use_gpu=False)
        
        result = translator.translate(
            "Yapay Zeka",
            source_lang="tr",
            target_lang="en"
        )
        
        assert result == "Artificial Intelligence"


class TestBatchTranslation:
    """Toplu çeviri testleri."""

    def test_batch_translation_turkish_to_english(self):
        """
        Test: Toplu TR→EN çeviri
        Beklenen: Tüm cümleler çevrilmeli
        """
        translator = Translator(use_gpu=False)
        
        texts = ["Merhaba", "Nasılsın?", "İyi günler"]
        
        with patch.object(translator.tr_en_model, 'generate') as mock_gen:
            with patch.object(translator.tr_en_tokenizer, 'batch_decode') as mock_dec:
                mock_dec.return_value = ["Hello", "How are you?", "Good day"]
                
                results = translator.translate_batch(
                    texts,
                    source_lang="tr",
                    target_lang="en"
                )
                
                assert len(results) == 3
                assert results[0] == "Hello"

    def test_batch_empty_list(self):
        """
        Test: Boş liste çevirisi
        Beklenen: Boş liste dönmeli
        """
        translator = Translator(use_gpu=False)
        
        results = translator.translate_batch([], "tr", "en")
        assert results == []


class TestProperNouns:
    """Özel isim koruma testleri."""

    def test_konya_preservation(self):
        """
        Test: "Konya" özel ismi korunmalı
        Beklenen: Çeviride "Konya" değişmemeli
        """
        translator = Translator(use_gpu=False)
        
        # Sözlükten
        result = translator.translate("Konya", "tr", "en")
        assert result == "Konya"

    def test_selcuk_preservation(self):
        """
        Test: "Selçuk" özel ismi korunmalı
        Beklenen: Çeviride "Selçuk" → "Selcuk" (ç→c)
        """
        translator = Translator(use_gpu=False)
        
        # Sözlükten tam eşleşme
        result = translator.translate(
            "Selçuk Üniversitesi",
            "tr",
            "en"
        )
        assert "Selcuk" in result


class TestPerformance:
    """Performans testleri."""

    def test_single_translation_speed(self):
        """
        Test: Tek çeviri süresi
        Beklenen: < 200ms (mock ile çok hızlı olmalı)
        """
        translator = Translator(use_gpu=False)
        
        with patch.object(translator.tr_en_model, 'generate'):
            with patch.object(translator.tr_en_tokenizer, 'decode', return_value="Test"):
                start = time.time()
                translator.translate("Test metni", "tr", "en")
                elapsed = (time.time() - start) * 1000  # ms
                
                assert elapsed < 200  # Mock ile çok hızlı

    def test_cache_effectiveness(self):
        """
        Test: Önbellek çalışıyor mu?
        Beklenen: Aynı cümle 2. kez daha hızlı
        """
        translator = Translator(use_gpu=False)
        
        text = "Test cümlesi"
        
        with patch.object(translator.tr_en_model, 'generate'):
            with patch.object(translator.tr_en_tokenizer, 'decode', return_value="Test sentence"):
                # İlk çeviri
                start1 = time.time()
                result1 = translator.translate(text, "tr", "en")
                time1 = time.time() - start1
                
                # İkinci çeviri (önbellekten)
                start2 = time.time()
                result2 = translator.translate(text, "tr", "en")
                time2 = time.time() - start2
                
                assert result1 == result2
                assert time2 < time1  # Önbellekten daha hızlı

    def test_benchmark_function(self):
        """
        Test: Benchmark fonksiyonu çalışıyor mu?
        Beklenen: Metrikler dönmeli
        """
        translator = Translator(use_gpu=False)
        
        with patch.object(translator, 'translate', return_value="Test"):
            metrics = translator.benchmark(num_samples=10)
            
            assert "avg_time_ms" in metrics
            assert "min_time_ms" in metrics
            assert "max_time_ms" in metrics
            assert metrics["total_samples"] == 10


class TestErrorHandling:
    """Hata yönetimi testleri."""

    def test_model_loading_error(self):
        """
        Test: Model yükleme hatası
        Beklenen: RuntimeError fırlatmalı
        """
        with patch('services.translator.MarianMTModel.from_pretrained', side_effect=Exception("Model bulunamadı")):
            with pytest.raises(RuntimeError):
                Translator(use_gpu=False)

    def test_translation_error_fallback(self):
        """
        Test: Çeviri hatası durumunda fallback
        Beklenen: Orijinal metin dönmeli
        """
        translator = Translator(use_gpu=False)
        
        with patch.object(translator.tr_en_model, 'generate', side_effect=Exception("GPU hatası")):
            result = translator.translate("Test", "tr", "en")
            assert result == "Test"  # Hata durumunda orijinal


class TestGlossaryLoading:
    """Sözlük yükleme testleri."""

    def test_default_glossary_loaded(self):
        """
        Test: Varsayılan sözlük yükleniyor mu?
        Beklenen: Temel terimler mevcut olmalı
        """
        translator = Translator(use_gpu=False)
        
        assert "Selçuk Üniversitesi" in translator.glossary
        assert "Bilgisayar Mühendisliği" in translator.glossary
        assert "Yapay Zeka" in translator.glossary

    def test_custom_glossary_loading(self):
        """
        Test: Özel sözlük dosyası yükleme
        Beklenen: Özel terimler eklenmiş olmalı
        """
        import json
        import tempfile
        
        # Geçici sözlük dosyası oluştur
        custom_glossary = {
            "Özel Terim": {"en": "Custom Term"}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(custom_glossary, f)
            temp_path = f.name
        
        translator = Translator(use_gpu=False, glossary_path=temp_path)
        
        assert "Özel Terim" in translator.glossary
        
        # Temizlik
        import os
        os.unlink(temp_path)


class TestTurkishCharacters:
    """Türkçe özel karakter testleri."""

    def test_turkish_special_characters(self):
        """
        Test: Türkçe özel karakterler (ç, ğ, ı, ö, ş, ü)
        Beklenen: Karakterler kaybolmamalı
        """
        translator = Translator(use_gpu=False)
        
        with patch.object(translator.tr_en_model, 'generate'):
            with patch.object(translator.tr_en_tokenizer, 'decode', return_value="Turkish University"):
                result = translator.translate(
                    "Türkçe Üniversitesi",
                    "tr",
                    "en"
                )
                
                # Mock çıktısı kontrol
                assert result == "Turkish University"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
