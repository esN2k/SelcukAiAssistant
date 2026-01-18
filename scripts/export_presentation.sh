#!/bin/bash
# EMERGENCY PRESENTATION EXPORT
# Time: ~5 minutes execution

set -euo pipefail

echo "🎤 EMERGENCY PRESENTATION EXPORT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Try Marp first
if command -v marp &> /dev/null; then
    echo "✅ Using Marp..."
    marp docs/SUNUM.md -o SUNUM.pdf --pdf --allow-local-files
    marp docs/SUNUM.md -o SUNUM.pptx --pptx --allow-local-files
    echo "✅ Created: SUNUM.pdf, SUNUM.pptx"
    exit 0
fi

# Fallback: Online
echo ""
echo "⚠️  Marp not available. Use ONLINE METHOD:"
echo ""
echo "🌐 FASTEST: Marp Web (RECOMMENDED)"
echo "   1. Open: https://web.marp.app/"
echo "   2. Paste docs/SUNUM.md"
echo "   3. Export → PDF/PPTX"
echo ""
echo "🌐 Alternative: Google Slides"
echo "   1. Create new presentation"
echo "   2. Manually copy slides from docs/SUNUM.md"
echo "   3. Each '# Slayt X:' = new slide"
echo ""
echo "📋 File ready: docs/SUNUM.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
