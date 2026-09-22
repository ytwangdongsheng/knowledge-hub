"""从 knowledge-hub 里最完整的一篇（B v3）抽取 <style> 块，
注入 STYLE.md 的规范附录，保证「规范」与「实装」逐字节一致。

用法：python build_style_spec.py
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent

# 参考实装：B v3 = 类名与组件最齐全的一篇
SOURCE = REPO / "token-embedding" / "index.html"
TARGET = REPO / "STYLE.md"
MARKER = "<!-- CANONICAL-CSS -->"

html = SOURCE.read_text(encoding="utf-8")
match = re.search(r"(?s)<style>(.*?)</style>", html)
if not match:
    raise SystemExit("找不到 <style> 块")

css = match.group(1).strip("\n")
# 规范里用 4 空格缩进保持不变；去掉行尾空白
css = "\n".join(line.rstrip() for line in css.split("\n"))

spec = TARGET.read_text(encoding="utf-8")
if MARKER not in spec:
    raise SystemExit(f"STYLE.md 里找不到标记 {MARKER}")

out = spec.replace(MARKER, "```css\n" + css + "\n```")
TARGET.write_text(out, encoding="utf-8")

print(f"source : {SOURCE.relative_to(REPO)}")
print(f"css    : {len(css)} chars / {css.count(chr(10)) + 1} lines")
print(f"spec   : {TARGET.name} written ({len(out)} chars)")
