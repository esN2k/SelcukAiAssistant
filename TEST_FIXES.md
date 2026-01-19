# Test Commands for SelcukAI Assistant Fixes

## 🧪 Test 1: Translation Service

### Backend Test
```bash
# Test translation endpoint directly
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Hello world\",\"source_lang\":\"en\",\"target_lang\":\"tr\"}"

# Expected response:
# {"original":"Hello world","translated":"Merhaba dünya","source_lang":"en","target_lang":"tr","metrics":{...},"model_info":{...}}
```

### Frontend Test
1. Open the app
2. Navigate to Translation screen
3. Enter text: "Hello world"
4. Select: English → Turkish
5. Click "Çevir" button
6. **Expected**: Translation appears in the result card (no error message)

---

## 🧪 Test 2: RAG Service Context Retrieval

### Backend Test
```bash
cd e:\SelcukAiAssistant\repo\backend

# Test 1: Check FAISS index
python -c "
import faiss
from pathlib import Path
index_path = Path('data/rag/index.faiss')
if index_path.exists():
    index = faiss.read_index(str(index_path))
    print(f'✓ FAISS index loaded: {index.ntotal} vectors')
else:
    print('✗ FAISS index not found')
"

# Test 2: Test RAG search with debug logging
python -c "
from rag_service import rag_service
import logging
logging.basicConfig(level=logging.INFO)

queries = [
    'Selçuk Üniversitesi nerede',
    'Sınavlar ne zaman',
    'Kayıt tarihleri',
]

for query in queries:
    print(f'\n--- Testing: {query} ---')
    context, citations = rag_service.get_context(query, top_k=3)
    print(f'Context length: {len(context)} chars')
    print(f'Citations: {len(citations)}')
    if context:
        print(f'Preview: {context[:200]}...')
    else:
        print('⚠️ No context returned')
"
```

### Check Backend Logs
After running a chat query, check the backend logs for:
```
RAG search: query='...', top_k=4, scores=[...]
RAG search returned X documents
RAG get_context: Returning X documents, Y chars of context
RAG context_relevant=True/False
```

### Frontend Test
1. Open the app
2. Go to Settings → Enable RAG
3. Go to Chat screen
4. Ask: "Selçuk Üniversitesi sınavlar ne zaman?"
5. **Expected**: Should get a response from RAG documents (not "Bu bilgi kaynaklarda yok")

---

## 🧪 Test 3: Model Selection UI

### Frontend Test
1. Open the app
2. Navigate to Settings → Diagnostics
3. Check "Model" section
4. **Expected**: 
   - Shows selected model name (e.g., "selcukaiassistant")
   - Shows "Uygun" (Available) or "Kullanılmıyor" (Unavailable) with reason
   - NOT "Seçilmedi" if a model is actually selected

### Debug
If showing "Seçilmedi":
- Check `Pref.selectedModel` is set
- Check backend `/models` endpoint returns the model
- Check model list loads successfully (no errors in diagnostics logs)

---

## 🧪 Test 4: AppWrite Connection Heartbeat

### Check Logs
Monitor Flutter console for heartbeat messages:
```
✓ Appwrite heartbeat OK
```

Should appear every 5 minutes after app starts.

### Test Long Session
1. Open the app
2. Leave it running for 10+ minutes
3. Try to use chat/translation features
4. **Expected**: No session timeout errors, features work normally

---

## 🔍 Debugging Tips

### Translation Not Working
1. Check backend logs for: `POST /api/translate HTTP/1.1" 200 OK`
2. Check frontend console for JSON parsing errors
3. Verify response contains `translated` field

### RAG Returning Empty
1. Check backend logs for RAG search scores
2. If scores are very low (< 0.1), documents may not be relevant
3. Check `is_context_relevant` returns True
4. Verify FAISS index exists and has vectors

### Model Not Showing
1. Check `/models` endpoint returns data
2. Verify model ID matches between backend and frontend
3. Check diagnostics screen for model load errors

### AppWrite Timeout
1. Check `.env` has correct APPWRITE credentials
2. Monitor heartbeat logs
3. Verify network connection to Appwrite cloud

---

## 📊 Success Criteria

✅ Translation: Result appears in UI without error  
✅ RAG: Returns relevant context for university-related questions  
✅ Model UI: Shows correct model name and availability  
✅ AppWrite: Heartbeat logs appear every 5 minutes  
✅ No backend exceptions in logs  

---

## 🐛 Known Issues (Not Fixed)

### Windows AsyncIO Error
```
OSError: [WinError 10022] Geçersiz bir değişken sağlandı
```
This is a known Windows proactor event loop issue when closing streaming connections. It's logged but doesn't affect functionality. Can be suppressed with:

```python
# In backend/main.py or providers
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*proactor.*")
```

---

## 📝 Next Steps After Testing

1. Run all tests above
2. Document any failures
3. Check backend logs for new debug output
4. Adjust RAG similarity threshold if needed (currently using default FAISS scores)
5. Monitor AppWrite heartbeat over longer sessions
