import sys
import subprocess
from pathlib import Path

TEX_TEMPLATE = "template.tex"

def main(csv_path: Path):
    with open(csv_path, "r") as f:
        f.readline()
        names = []
        for line in f:
            toks = line.strip().split(",")
            last, first = toks[1:3]
            group = toks[4]
            names.append(f"{first} {last} ({group})")
    names.sort(key=str.lower)
    outfile = csv_path.with_suffix(".tex")
    ncols = 0
    with open(TEX_TEMPLATE, "r") as tt:
        with open(outfile, "w") as out:
            for line in tt:
                if r"\begin{xltabular}" in line:
                    ncols = line.count("X")
                if r"%% NAMES %%" in line:
                    for name in names:
                        out.write(f"    {name} " + ncols*" & ◯" + "\\\\ \n")
                else:
                    out.write(line)
    
    # run pdflatex on the new file
    subprocess.run(["pdflatex", outfile.name], cwd=Path(csv_path).parent)

if __name__ == "__main__":
    main(Path(sys.argv[1]))