# 📤 EMERGENCY EXPORT GUIDE

**Time Constraint**: Presentation TOMORROW
**Status**: TEZ_RAPORU.md (75 pages) ✅ | SUNUM.md (40 slides) ✅

---

## 🚀 FASTEST METHOD (10 minutes total)

### Step 1: Thesis → PDF (5 min)

**Option A: Dillinger.io** ⭐ RECOMMENDED
1. Open https://dillinger.io/
2. Click "Import from" → Select `docs/TEZ_RAPORU.md`
3. Click "Export as" → PDF
4. Save as `TEZ_RAPORU.pdf`

**Option B: Google Docs**
1. Open Google Docs
2. File → Import → Upload `docs/TEZ_RAPORU.md`
3. File → Download → PDF

### Step 2: Presentation → PDF/PPTX (5 min)

**Option A: Marp Web** ⭐ RECOMMENDED
1. Open https://web.marp.app/
2. Paste content from `docs/SUNUM.md`
3. Click top-right menu → Export PDF
4. Save as `SUNUM.pdf`

**Option B: PowerPoint Manual**
1. Open PowerPoint
2. Create 40 slides from `docs/SUNUM.md`
3. Each `# Slayt X:` = new slide
4. Save as `SUNUM.pptx`

---

## 🔧 LOCAL METHOD (if tools installed)

```bash
# Install (one-time, ~10 min)
sudo apt install pandoc texlive-xetex  # Linux
brew install pandoc basictex          # macOS
npm install -g @marp-team/marp-cli

# Export (2 min)
bash scripts/export_thesis_pdf.sh
bash scripts/export_presentation.sh
```

---

## ✅ VERIFICATION

After export:
- [ ] Open TEZ_RAPORU.pdf → All 75 pages readable
- [ ] Open SUNUM.pdf → All 40 slides visible
- [ ] Check tables not cut off
- [ ] Check code blocks formatted
- [ ] Page numbers correct

---

## 🚨 IF EXPORT FAILS

**Backup Plan**:
1. Print docs/TEZ_RAPORU.md directly (as Markdown)
2. Show docs/SUNUM.md on laptop during presentation
3. Focus on demo quality (more important than slides)

**Time Priority**:
- Demo preparation > Slides > Thesis formatting
