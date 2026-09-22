"""校验 STYLE.md 里的 CSS 与参考实装逐字节一致。"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

spec = (Path(__file__).resolve().parent / "STYLE.md").read_text(encoding="utf-8")
src = (Path(__file__).resolve().parent / "token-embedding" / "index.html").read_text(encoding="utf-8")

css_src = "\n".join(
    line.rstrip()
    for line in re.search(r"(?s)<style>(.*?)</style>", src).group(1).strip("\n").split("\n")
)

fence = "`" * 3
blocks = re.findall(r"(?s)" + fence + r"css\n(.*?)\n" + fence, spec)
# §6 的规范 CSS 是最大的那个代码块
css_spec = max(blocks, key=len)

print("identical  :", css_src == css_spec)
print("blocks     :", [b.count("\n") + 1 for b in blocks], "行")
print("spec lines :", css_spec.count("\n") + 1)
print("marker left:", "<!-- CANONICAL-CSS -->" in spec)
print("fences     :", spec.count(fence), "(应为偶数)")
