import io
from pathlib import Path
import os

def main():
    out = ""
    format = "r|"
    for x in range(2, 11):
        out += f"& {x}"
        format += "r"
    out += "\\\\\n\\hline"
    for y in range(2, 26):
        out += f"{y}"
        for x in range(2, 11):
            out += f"& {x*y}"
        out += "\\\\\n"
    out = f"""
    \\begin{{tabular}}{{{format}}}
    {out}
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