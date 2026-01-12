"""Test accuracy guard fonksiyonlarını doğrular.

Bu testler, kritik bilgilerin doğru şekilde kontrol edildiğini
ve yanlış yanıtların düzeltildiğini doğrular.
"""
import pytest
from accuracy_guard import (
    guard_response_accuracy,
    validate_critical_answer,
    _detect_question_category,
    _contains_wrong_fact,
    _contains_correct_fact,
)


class TestQuestionDetection:
    """Soru kategorisi tespit testleri."""
    
    def test_detect_location_question_turkish(self):
        """Konum soruları tespit edilmeli."""
        questions = [
            "Selçuk Üniversitesi nerede?",
            "Selçuk Üniversitesi hangi şehirde?",
            "Selçuk Üniversitesi hangi ilde?",
            "Üniversite nerede bulunur?",
        ]
        for q in questions:
            assert _detect_question_category(q) == "konum"
    
    def test_detect_location_question_english(self):
        """İngilizce konum soruları tespit edilmeli."""
        questions = [
            "Where is Selçuk University?",
            "What city is Selçuk University in?",
            "Where is the university located?",
        ]
        for q in questions:
            assert _detect_question_category(q) == "konum"
    
    def test_detect_founding_year_question(self):
        """Kuruluş yılı soruları tespit edilmeli."""
        questions = [
            "Selçuk Üniversitesi ne zaman kuruldu?",
            "Üniversite kaç yılında kuruldu?",
            "Kuruluş yılı nedir?",
            "When was Selçuk University founded?",
        ]
        for q in questions:
            assert _detect_question_category(q) == "kuruluş_yılı"
    
    def test_ignore_unrelated_question(self):
        """İlgisiz sorular tespit edilmemeli."""
        questions = [
            "Hava durumu nasıl?",
            "Python nedir?",
            "Merhaba, nasılsın?",
        ]
        for q in questions:
            assert _detect_question_category(q) is None


class TestWrongFactDetection:
    """Yanlış bilgi tespit testleri."""
    
    def test_detect_wrong_city_izmir(self):
        """İzmir yanlış şehir olarak tespit edilmeli."""
        answer = "Selçuk Üniversitesi İzmir'de bulunmaktadır."
        wrong = _contains_wrong_fact(answer, "konum")
        assert wrong == "izmir"
    
    def test_detect_wrong_city_ankara(self):
        """Ankara yanlış şehir olarak tespit edilmeli."""
        answer = "Üniversite Ankara'da kurulmuştur."
        wrong = _contains_wrong_fact(answer, "konum")
        assert wrong == "ankara"
    
    def test_detect_wrong_year(self):
        """Yanlış kuruluş yılı tespit edilmeli."""
        answer = "Selçuk Üniversitesi 1982 yılında kuruldu."
        wrong = _contains_wrong_fact(answer, "kuruluş_yılı")
        assert wrong == "1982"
    
    def test_no_wrong_fact_in_correct_answer(self):
        """Doğru yanıtta yanlış bilgi olmamalı."""
        answer = "Selçuk Üniversitesi Konya'da bulunmaktadır."
        wrong = _contains_wrong_fact(answer, "konum")
        assert wrong is None


class TestCorrectFactDetection:
    """Doğru bilgi tespit testleri."""
    
    def test_detect_correct_city(self):
        """Konya doğru şehir olarak tespit edilmeli."""
        answer = "Selçuk Üniversitesi Konya'da bulunmaktadır."
        assert _contains_correct_fact(answer, "konum") is True
    
    def test_detect_correct_year(self):
        """1975 doğru yıl olarak tespit edilmeli."""
        answer = "Üniversite 1975 yılında kurulmuştur."
        assert _contains_correct_fact(answer, "kuruluş_yılı") is True
    
    def test_missing_correct_fact(self):
        """Eksik doğru bilgi tespit edilmeli."""
        answer = "Selçuk Üniversitesi güzel bir üniversitedir."
        assert _contains_correct_fact(answer, "konum") is False


class TestGuardResponseAccuracy:
    """Yanıt doğruluğu koruma testleri."""
    
    def test_correct_wrong_city_answer_turkish(self):
        """Yanlış şehir cevabı düzeltilmeli (Türkçe)."""
        question = "Selçuk Üniversitesi nerede?"
        wrong_answer = "Selçuk Üniversitesi İzmir'de bulunmaktadır."
        
        corrected, was_corrected = guard_response_accuracy(question, wrong_answer, "tr")
        
        assert was_corrected is True
        assert "konya" in corrected.lower()
        assert "izmir" not in corrected.lower()
    
    def test_correct_wrong_city_answer_english(self):
        """Yanlış şehir cevabı düzeltilmeli (İngilizce)."""
        question = "Where is Selçuk University?"
        wrong_answer = "Selçuk University is in Ankara."
        
        corrected, was_corrected = guard_response_accuracy(question, wrong_answer, "en")
        
        assert was_corrected is True
        assert "konya" in corrected.lower()
        assert "ankara" not in corrected.lower()
    
    def test_correct_wrong_year_answer(self):
        """Yanlış kuruluş yılı düzeltilmeli."""
        question = "Selçuk Üniversitesi ne zaman kuruldu?"
        wrong_answer = "Selçuk Üniversitesi 1982 yılında kuruldu."
        
        corrected, was_corrected = guard_response_accuracy(question, wrong_answer, "tr")
        
        assert was_corrected is True
        assert "1975" in corrected
        # Note: 1982 can be mentioned in the historical context (reorganization year)
        assert "**1975**" in corrected or "1975 yılında kurulmuştur" in corrected
    
    def test_keep_correct_answer(self):
        """Doğru cevap değiştirilmemeli."""
        question = "Selçuk Üniversitesi nerede?"
        correct_answer = "Selçuk Üniversitesi Konya'da bulunmaktadır."
        
        result, was_corrected = guard_response_accuracy(question, correct_answer, "tr")
        
        assert was_corrected is False
        assert result == correct_answer
    
    def test_add_missing_city_info(self):
        """Eksik şehir bilgisi eklenmeli."""
        question = "Selçuk Üniversitesi nerede?"
        incomplete_answer = "Selçuk Üniversitesi büyük bir devlet üniversitesidir."
        
        result, was_corrected = guard_response_accuracy(question, incomplete_answer, "tr")
        
        assert was_corrected is True
        assert "konya" in result.lower()
    
    def test_ignore_unrelated_question(self):
        """İlgisiz sorular değiştirilmemeli."""
        question = "Python nedir?"
        answer = "Python bir programlama dilidir."
        
        result, was_corrected = guard_response_accuracy(question, answer, "tr")
        
        assert was_corrected is False
        assert result == answer


class TestValidateCriticalAnswer:
    """Kritik yanıt validasyon testleri."""
    
    def test_valid_location_answer(self):
        """Geçerli konum yanıtı kabul edilmeli."""
        question = "Selçuk Üniversitesi nerede?"
        answer = "Selçuk Üniversitesi Konya'da bulunmaktadır."
        
        is_valid, error = validate_critical_answer(question, answer)
        
        assert is_valid is True
        assert error is None
    
    def test_invalid_location_answer_wrong_city(self):
        """Yanlış şehir yanıtı reddedilmeli."""
        question = "Selçuk Üniversitesi nerede?"
        answer = "Selçuk Üniversitesi İzmir'de bulunmaktadır."
        
        is_valid, error = validate_critical_answer(question, answer)
        
        assert is_valid is False
        assert error is not None
        assert "izmir" in error.lower()
    
    def test_invalid_location_answer_missing_info(self):
        """Eksik bilgi yanıtı reddedilmeli."""
        question = "Selçuk Üniversitesi nerede?"
        answer = "Selçuk Üniversitesi güzel bir üniversitedir."
        
        is_valid, error = validate_critical_answer(question, answer)
        
        assert is_valid is False
        assert error is not None
    
    def test_valid_year_answer(self):
        """Geçerli kuruluş yılı yanıtı kabul edilmeli."""
        question = "Selçuk Üniversitesi ne zaman kuruldu?"
        answer = "Selçuk Üniversitesi 1975 yılında kurulmuştur."
        
        is_valid, error = validate_critical_answer(question, answer)
        
        assert is_valid is True
        assert error is None
    
    def test_unrelated_question_passes(self):
        """İlgisiz sorular geçerli kabul edilmeli."""
        question = "Python nedir?"
        answer = "Python bir programlama dilidir."
        
        is_valid, error = validate_critical_answer(question, answer)
        
        assert is_valid is True
        assert error is None


class TestRealWorldScenarios:
    """Gerçek dünya senaryoları."""
    
    def test_complex_location_answer_with_details(self):
        """Detaylı konum yanıtı doğru işlenmeli."""
        question = "Selçuk Üniversitesi nerede?"
        answer = """Selçuk Üniversitesi Konya ilinde bulunmaktadır. 
        İki ana kampüsü vardır: 
        - Alaeddin Keykubat Kampüsü (Selçuklu/Konya)
        - Ardıçlı Kampüsü (Karatay/Konya)"""
        
        result, was_corrected = guard_response_accuracy(question, answer, "tr")
        
        assert was_corrected is False  # Doğru cevap, düzeltilmemeli
        assert "konya" in result.lower()
    
    def test_mixed_information_correct_and_wrong(self):
        """Karışık bilgi varsa yanlış tespit edilmeli."""
        question = "Selçuk Üniversitesi nerede?"
        answer = "Selçuk Üniversitesi Ankara'da bulunur ve Konya'da şubesi vardır."
        
        result, was_corrected = guard_response_accuracy(question, answer, "tr")
        
        # Ankara yanlış, düzeltilmeli
        assert was_corrected is True
        assert "konya" in result.lower()
    
    def test_case_insensitive_detection(self):
        """Büyük/küçük harf duyarsız olmalı."""
        question = "SELÇUK ÜNİVERSİTESİ NEREDE?"
        answer = "SELÇUK ÜNİVERSİTESİ KONYA'DADIR."
        
        result, was_corrected = guard_response_accuracy(question, answer, "tr")
        
        assert was_corrected is False  # Doğru, değiştirilmemeli


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
