"""Test kritik bilgilerin system prompt'ta doğru olduğunu doğrular.

Bu test, Selçuk Üniversitesi'nin konumu, kuruluş yılı gibi
kritik bilgilerin system prompt'ta doğru şekilde yer aldığını kontrol eder.
"""
import pytest
from prompts import (
    SELCUK_CORE_FACTS,
    SELCUK_UNIVERSITY_SYSTEM_PROMPT,
    DEFAULT_SYSTEM_PROMPT_EN,
    build_default_system_prompt,
)


class TestCriticalFacts:
    """Kritik bilgilerin system prompt'ta doğru olduğunu test eder."""

    def test_core_facts_contains_konya(self):
        """System prompt'ta Konya bilgisi olmalı."""
        assert "konya" in SELCUK_CORE_FACTS.lower()
        assert "Konya" in SELCUK_CORE_FACTS or "KONYA" in SELCUK_CORE_FACTS

    def test_core_facts_not_contains_izmir(self):
        """System prompt'ta İzmir bilgisi olmamalı (yanlış bilgi)."""
        # İzmir yanlış konum, system prompt'ta olmamalı
        # Not: "İzmir değil" gibi açıklayıcı metinler olabilir
        lower_facts = SELCUK_CORE_FACTS.lower()
        if "izmir" in lower_facts:
            # Eğer İzmir geçiyorsa, "değil" veya "not" ile birlikte geçmeli
            assert "izmir değil" in lower_facts or "not izmir" in lower_facts

    def test_core_facts_contains_1975(self):
        """System prompt'ta kuruluş yılı 1975 olmalı."""
        assert "1975" in SELCUK_CORE_FACTS

    def test_core_facts_contains_teknoloji_fakultesi(self):
        """Bilgisayar Mühendisliği için Teknoloji Fakültesi belirtilmeli."""
        lower_facts = SELCUK_CORE_FACTS.lower()
        assert "teknoloji fakültesi" in lower_facts or "technology faculty" in lower_facts

    def test_core_facts_contains_alaeddin_keykubat(self):
        """Alaeddin Keykubat kampüsü belirtilmeli."""
        lower_facts = SELCUK_CORE_FACTS.lower()
        assert "alaeddin keykubat" in lower_facts

    def test_core_facts_contains_mudek(self):
        """MÜDEK akreditasyonu belirtilmeli."""
        lower_facts = SELCUK_CORE_FACTS.lower()
        assert "müdek" in lower_facts or "mudek" in lower_facts

    def test_turkish_system_prompt_includes_core_facts(self):
        """Türkçe system prompt core facts içermeli."""
        assert SELCUK_CORE_FACTS in SELCUK_UNIVERSITY_SYSTEM_PROMPT

    def test_english_system_prompt_contains_konya(self):
        """İngilizce system prompt'ta da Konya bilgisi olmalı."""
        assert "konya" in DEFAULT_SYSTEM_PROMPT_EN.lower()

    def test_english_system_prompt_not_contains_izmir(self):
        """İngilizce system prompt'ta İzmir bilgisi olmamalı."""
        lower_prompt = DEFAULT_SYSTEM_PROMPT_EN.lower()
        if "izmir" in lower_prompt:
            assert "not izmir" in lower_prompt

    def test_english_system_prompt_contains_1975(self):
        """İngilizce system prompt'ta kuruluş yılı 1975 olmalı."""
        assert "1975" in DEFAULT_SYSTEM_PROMPT_EN

    def test_build_default_system_prompt_turkish(self):
        """Türkçe için oluşturulan prompt Konya içermeli."""
        prompt = build_default_system_prompt("tr")
        assert "konya" in prompt.lower()

    def test_build_default_system_prompt_english(self):
        """İngilizce için oluşturulan prompt Konya içermeli."""
        prompt = build_default_system_prompt("en")
        assert "konya" in prompt.lower()

    def test_critical_keywords_present(self):
        """Tüm kritik anahtar kelimeler mevcut olmalı."""
        combined = SELCUK_UNIVERSITY_SYSTEM_PROMPT + DEFAULT_SYSTEM_PROMPT_EN
        combined_lower = combined.lower()
        
        critical_keywords = [
            "konya",
            "1975",
            "teknoloji fakültesi",
            "alaeddin keykubat",
            "müdek",
        ]
        
        for keyword in critical_keywords:
            assert keyword in combined_lower, f"'{keyword}' bulunamadı!"

    def test_no_wrong_location_in_prompts(self):
        """Yanlış konum bilgileri olmamalı."""
        combined = SELCUK_UNIVERSITY_SYSTEM_PROMPT + DEFAULT_SYSTEM_PROMPT_EN
        combined_lower = combined.lower()
        
        # Bu şehirler yanlış olurdu, disclaimer olmadan geçmemeli
        wrong_cities = ["ankara", "istanbul", "bursa"]
        
        for city in wrong_cities:
            if city in combined_lower:
                # Eğer geçiyorsa, bir disclaimer ile geçmeli
                pytest.fail(f"Yanlış şehir '{city}' prompt'ta bulundu!")


class TestSystemPromptQuality:
    """System prompt kalitesini test eder."""

    def test_prompt_not_empty(self):
        """System prompt boş olmamalı."""
        assert len(SELCUK_UNIVERSITY_SYSTEM_PROMPT) > 100
        assert len(DEFAULT_SYSTEM_PROMPT_EN) > 100

    def test_prompt_has_structure(self):
        """System prompt yapılandırılmış olmalı."""
        # Markdown başlıklar var mı?
        assert "##" in SELCUK_UNIVERSITY_SYSTEM_PROMPT or "#" in SELCUK_UNIVERSITY_SYSTEM_PROMPT

    def test_prompt_mentions_assistant_role(self):
        """System prompt asistan rolünü belirtmeli."""
        lower_prompt = SELCUK_UNIVERSITY_SYSTEM_PROMPT.lower()
        assert "asistan" in lower_prompt or "assistant" in lower_prompt

    def test_prompt_mentions_university_name(self):
        """System prompt üniversite adını belirtmeli."""
        lower_prompt = SELCUK_UNIVERSITY_SYSTEM_PROMPT.lower()
        assert "selçuk üniversitesi" in lower_prompt or "selcuk university" in lower_prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
