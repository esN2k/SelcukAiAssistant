"""
═══════════════════════════════════════════════════════════════════════════════
TEKRARLAMA TESPİT SİSTEMİ
═══════════════════════════════════════════════════════════════════════════════

Modül: repetition_detector.py
Açıklama: Streaming yanıtlarda tekrarlama döngüsü tespiti ve önleme

Özellikler:
    - Chunk bazlı tekrarlama tespiti
    - Cümle seviyesinde benzerlik analizi
    - Paragraf tekrarı kontrolü
    - Jaccard similarity algoritması

Çalışma Mantığı:
    1. Her yeni chunk alındığında window'a eklenir
    2. Son N chunk arasında benzerlik kontrolü yapılır
    3. Benzerlik eşik değerini aşarsa True döner
    4. Cümle tekrarı kontrolü (3+ benzer cümle)

Parametreler:
    - window_size: Karşılaştırılacak son chunk sayısı (varsayılan: 5)
    - similarity_threshold: Benzerlik eşiği (varsayılan: 0.8)

Kullanım:
    detector = RepetitionDetector()
    for chunk in stream:
        if detector.feed(chunk):
            break  # Tekrarlama tespit edildi, dur

Yazar: SelçukAI Ekibi
═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

from collections import deque
from typing import Optional


class RepetitionDetector:
    """
    Tekrarlama Dedektörü Sınıfı.
    
    Akış metinlerinde tekrarlayan kalıpları tespit ederek sonsuz
    döngüleri önler.
    
    Attributes:
        window_size: Karşılaştırılacak son parça sayısı
        similarity_threshold: Tekrarlama tetikleme benzerlik oranı (0-1)
        recent_chunks: Son parçaları tutan kuyruk
        full_text: Biriken tam metin
    """
    
    def __init__(self, window_size: int = 5, similarity_threshold: float = 0.8):
        """
        Tekrarlama dedektörünü başlatır.
        
        Args:
            window_size: Karşılaştırılacak son parça sayısı
            similarity_threshold: Tekrarlama tetikleme benzerlik oranı (0-1)
        """
        self.window_size = window_size
        self.similarity_threshold = similarity_threshold
        self.recent_chunks: deque[str] = deque(maxlen=window_size)
        self.full_text = ""
        
    def feed(self, chunk: str) -> bool:
        """
        Yeni parçayı besler ve tekrarlama kontrolü yapar.
        
        Args:
            chunk: Akıştan gelen yeni metin parçası
            
        Returns:
            Tekrarlama tespit edilirse True, aksi halde False
        """
        if not chunk or not chunk.strip():
            return False
            
        self.full_text += chunk
        
        # Son parçalarda tam tekrarlama kontrolü
        if chunk.strip() in self.recent_chunks:
            return True
            
        self.recent_chunks.append(chunk.strip())
        
        # Cümle düzeyinde tekrarlama kontrolü
        if self._check_sentence_repetition():
            return True
            
        # Paragraf düzeyinde tekrarlama kontrolü
        if self._check_paragraph_repetition():
            return True
            
        return False
    
    def _check_sentence_repetition(self) -> bool:
        """Aynı cümlenin son zamanlarda birden fazla kez görünüp görünmediğini kontrol eder."""
        sentences = self._extract_sentences(self.full_text)
        if len(sentences) < 3:
            return False
            
        # Son 3 cümleyi kontrol et
        recent_sentences = sentences[-3:]
        if len(recent_sentences) == 3:
            # Her 3'ü de benzerse, tekrarlamadır
            if self._are_similar(recent_sentences[0], recent_sentences[1]) and \
               self._are_similar(recent_sentences[1], recent_sentences[2]):
                return True
                
        return False
    
    def _check_paragraph_repetition(self) -> bool:
        """Aynı paragrafın birden fazla kez görünüp görünmediğini kontrol eder."""
        paragraphs = [p.strip() for p in self.full_text.split('\n\n') if p.strip()]
        if len(paragraphs) < 2:
            return False
            
        # Son paragrafın sondan bir öncekine çok benzeyip benzemediğini kontrol et
        if len(paragraphs) >= 2:
            if self._are_similar(paragraphs[-1], paragraphs[-2]):
                return True
                
        return False
    
    def _extract_sentences(self, text: str) -> list[str]:
        """Metinden cümleleri çıkarır."""
        import re
        # Basit cümle ayırma
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    def _are_similar(self, text1: str, text2: str) -> bool:
        """Basit oran kullanarak iki metnin benzer olup olmadığını kontrol eder."""
        if not text1 or not text2:
            return False
            
        # Normalize et
        t1 = text1.lower().strip()
        t2 = text2.lower().strip()
        
        # Tam eşleşme
        if t1 == t2:
            return True
            
        # Birinin diğerinin çoğunu içerip içermediğini kontrol et
        if len(t1) > len(t2):
            longer, shorter = t1, t2
        else:
            longer, shorter = t2, t1
            
        if len(shorter) == 0:
            return False
            
        # Basit içerme kontrolü
        if shorter in longer:
            return True
            
        # Basit benzerlik hesapla (Jaccard benzeri)
        words1 = set(t1.split())
        words2 = set(t2.split())
        
        if not words1 or not words2:
            return False
            
        intersection = words1 & words2
        union = words1 | words2
        
        similarity = len(intersection) / len(union) if union else 0
        
        return similarity >= self.similarity_threshold
    
    def reset(self) -> None:
        """Dedektör durumunu sıfırlar."""
        self.recent_chunks.clear()
        self.full_text = ""
