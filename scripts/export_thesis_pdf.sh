#!/bin/bash
# EMERGENCY PDF EXPORT - THESIS
# Time: ~5 minutes execution

set -euo pipefail

echo "📄 EMERGENCY THESIS PDF EXPORT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create clean version first
echo "🧹 Preparing clean version..."
if [ -f "docs/TEZ_RAPORU.md" ]; then
    cp docs/TEZ_RAPORU.md docs/TEZ_RAPORU_FINAL.md
else
    echo "❌ Error: docs/TEZ_RAPORU.md not found!"
    exit 1
fi

# Add page breaks before chapters
# Note: This sed syntax works in GNU sed. MacOS/BSD might need adjustment.
sed -i 's/^## BÖLÜM/\newpage\n\n## BÖLÜM/g' docs/TEZ_RAPORU_FINAL.md

# Try Pandoc first (best quality)
if command -v pandoc &> /dev/null && command -v xelatex &> /dev/null; then
    echo "✅ Using Pandoc + XeLaTeX..."
    pandoc docs/TEZ_RAPORU_FINAL.md -o TEZ_RAPORU.pdf \
      --pdf-engine=xelatex \
      --toc \
      --toc-depth=3 \
      --number-sections \
      --variable documentclass=report \
      --variable geometry:margin=2.5cm \
      --variable fontsize=12pt \
      --variable lang=tr \
      --variable mainfont="DejaVu Sans" \
      --highlight-style=tango \
      --metadata title="Selçuk Üniversitesi Yapay Zeka Asistan" \
      --metadata date="18 Ocak 2026"
    
    if [ $? -eq 0 ]; then
        echo "✅ PDF created: TEZ_RAPORU.pdf"
        exit 0
    fi
fi

# Fallback: Online conversion instructions
echo ""
echo "⚠️  Pandoc not available. Use ONLINE METHOD:"

echo ""
echo "🌐 OPTION 1: Dillinger.io (FASTEST)"
echo "   1. Open: https://dillinger.io/"
echo "   2. Paste docs/TEZ_RAPORU_FINAL.md"
echo "   3. Export as PDF"

echo ""
echo "🌐 OPTION 2: Markdown to PDF"
echo "   1. Open: https://www.markdowntopdf.com/"
echo "   2. Upload docs/TEZ_RAPORU_FINAL.md"
echo "   3. Download PDF"

echo ""
echo "📋 File ready: docs/TEZ_RAPORU_FINAL.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
