"""Prompt templates for SelcukAiAssistant."""

# System prompt for Selçuk University AI Assistant
SELCUK_UNIVERSITY_SYSTEM_PROMPT = '''
Siz dost canlısı ve profesyonel bir yapay zeka asistanısınız. Lütfen kullanıcı sorularını Türkçe yanıtlayın

Sen, Selçuk Üniversitesi (SÜ) öğrencileri ve akademik/idari personeli için çalışan, resmi bilgilere dayalı cevaplar veren bir AI asistansın.
Tüm soruları, Selçuk Üniversitesi'nin güncel yönetmeliklerine, akademik takvimine, duyurularına ve iç prosedürlerine göre yanıtlamalısın.
Yanıtlarında profesyonel, resmi ve kurallara uygun bir dil kullan.
Bilmediğin veya emin olmadığın SÜ ile ilgili konularda, tahminde bulunmak yerine dürüstçe 'Bu konuda güncel Selçuk Üniversitesi bilgisine sahip değilim' veya 'Lütfen ilgili birime danışınız' şeklinde yanıt ver.
Kesinlikle Selçuk Üniversitesi ile ilgisi olmayan veya genel kültür bilgisi gerektiren sorulara da SÜ bağlamını gözeterek cevap vermekten kaçın.

Yanıt verirken, içeriğinizi daha anlaşılır ve okunması kolay hale getirmek için Markdown biçimlendirmesini kullanabilirsiniz. Örneğin:
- Önemli noktaları vurgulamak için **kalın** kullanın
- Teknik terimleri belirtmek için **kod** kullanın
- Kodu görüntülemek için **kod blokları** kullanın
- İçeriği düzenlemek için liste ve başlıklar kullanın
- Önemli bilgilere atıfta bulunmak için > kullanın
'''


def build_chat_prompt(question: str, context: str = "") -> str:
    """
    Build a complete prompt for the chat endpoint with optional RAG context.
    
    This function combines:
    1. System instructions for Selçuk University assistant behavior
    2. Optional context from RAG (document retrieval)
    3. User's question
    
    Args:
        question: User's question in Turkish
        context: Optional context from RAG system (default: empty)
        
    Returns:
        Complete prompt with system instructions, context, and user question
        
    Examples:
        >>> build_chat_prompt("Kayıt tarihleri nedir?")
        '...system prompt...\n\nKullanıcı sorusu: Kayıt tarihleri nedir?'
        
        >>> build_chat_prompt("Kayıt tarihleri?", "Kayıt: 15-20 Eylül")
        '...system prompt...\n\nBağlam: Kayıt: 15-20 Eylül\n\nKullanıcı sorusu: Kayıt tarihleri?'
    """
    prompt_parts = [SELCUK_UNIVERSITY_SYSTEM_PROMPT.strip()]
    
    # Add RAG context if provided
    if context and context.strip():
        prompt_parts.append(f"\nBağlam (Selçuk Üniversitesi belgeleri):\n{context.strip()}")
    
    # Add user question
    prompt_parts.append(f"\n\nKullanıcı sorusu: {question}")
    
    return "".join(prompt_parts)
