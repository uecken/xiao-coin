# Try these alternative commands if Noto Sans CJK JP doesn't work:

# Option 1: Use system default Japanese font
pandoc cover.md xiao_coin_ebook.md -o xiao_coin_ebook.pdf \
  --pdf-engine=xelatex \
  -V CJKmainfont="Yu Gothic" \
  --toc --number-sections

# Option 2: Use DejaVu fonts (more widely available)
pandoc cover.md xiao_coin_ebook.md -o xiao_coin_ebook.pdf \
  --pdf-engine=xelatex \
  -V CJKmainfont="DejaVu Sans" \
  --toc --number-sections

# Option 3: Let XeLaTeX handle font selection automatically
pandoc cover.md xiao_coin_ebook.md -o xiao_coin_ebook.pdf \
  --pdf-engine=xelatex \
  --toc --number-sections 