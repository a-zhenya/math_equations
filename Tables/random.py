import io
from pathlib import Path
import os
import random

def main():
    out = ""
    format = ""
    for x in range(10):
        format += "r"
    for y in range(30):
        for x in range(10):
            out += "&" if x else " "
            out += f"{random.randint(1, 999)}"
        out += "\\\\\n"
    out = f"""
    \\begin{{tabular}}{{{format}}}
    \\hline
    {out}
    \\hline
    \\end{{tabular}}
    """
    
    template = Path("template.tex").read_text()
    res = template.replace("% table", out)
    Path(__file__).with_suffix(".tex").write_text(res)
    os.system(f'pdflatex {Path(__file__).with_suffix(".tex")}')
    for ext in [".log", ".aux", ".tex"]:
        os.unlink(Path(__file__).with_suffix(ext))

if __name__ == "__main__":
    main()