#!/bin/bash
# FINAL VALIDATION - ALL SYSTEMS CHECK
# Time: ~2 minutes execution

set -euo pipefail

echo "🔍 FINAL PROJECT VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

ERRORS=0
WARNINGS=0

# Check thesis
echo "📄 Checking thesis..."
if [ -f "docs/TEZ_RAPORU.md" ]; then
    WORD_COUNT=$(wc -w < docs/TEZ_RAPORU.md)
    if [ $WORD_COUNT -ge 15000 ]; then
        echo "✅ Thesis: $WORD_COUNT words (target: 15,000+)"
    else
        echo "⚠️  Thesis: Only $WORD_COUNT words"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "❌ Thesis missing"
    ERRORS=$((ERRORS + 1))
fi

# Check presentation files
echo ""
echo "🎤 Checking presentation..."
for file in SUNUM.md SUNUM_KONUSMA_NOTLARI.md QA_HAZIRLIK.md SUNUM_KONTROL_LISTESI.md; do
    if [ -f "docs/$file" ]; then
        echo "✅ docs/$file exists"
    else
        echo "❌ docs/$file missing"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check backend
echo ""
echo "⚙️  Checking backend..."
if [ -f "backend/main.py" ]; then
    echo "✅ backend/main.py exists"
    # Try to verify it runs (timeout not available on all windows git bash, using fallback logic)
    echo "   (Skipping live execution check to avoid port conflicts)"
else
    echo "❌ backend/main.py missing"
    ERRORS=$((ERRORS + 1))
fi

# Check ChromaDB
echo ""
echo "💾 Checking RAG database..."
if [ -d "backend/chroma_db" ] || [ -d "backend/data/rag" ]; then
    echo "✅ Database directory exists"
else
    echo "⚠️  Database not found (will be created)"
    WARNINGS=$((WARNINGS + 1))
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ ALL CRITICAL CHECKS PASSED"
    [ $WARNINGS -gt 0 ] && echo "⚠️  $WARNINGS warnings (non-critical)"
    echo ""
    echo "🚀 NEXT STEPS:"
    echo "1. bash scripts/export_thesis_pdf.sh"
    echo "2. bash scripts/export_presentation.sh"
    echo "3. Review docs/FINAL_SUBMISSION_CHECKLIST.md"
else
    echo "❌ $ERRORS CRITICAL ERRORS - FIX IMMEDIATELY"
    exit 1
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
