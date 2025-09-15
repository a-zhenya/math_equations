#!/usr/bin/env python3

from random import shuffle;
from os import system

tex = True
filename = 'equations.tex' if tex else 'equations.txt'
template = r"""
\documentclass[a4paper,12pt]{article}
\usepackage[a4paper, total={7in, 11in}]{geometry}
\usepackage[latin1]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{euler}
\usepackage{multicol}
\usepackage{enumitem}
\pagestyle{empty}
\setlength\columnsep{3pc}
\begin{document}
\begin{multicols}{3}
\begin{enumerate}[font=\tiny]
% {equations}
\end{enumerate}
\end{multicols}
\end{document}
"""

L = 10

down = -L
up   =  L

LIMIT = None

def generate_coefs():
	for x1 in range(down, up + 1):
		if x1 == 0:
			continue
		for x2 in range(x1, up + 1):
			if x2 == 0:
				continue
			b = -(x1 + x2)
			q = x1 * x2
			yield b, q
			yield b*10, q*100

def type_eq(b, q):
	if b == 1:
		b = " + x"
	elif b == -1:
		b = " - x"
	elif b < 0:
		b = f" - {-b}x"
	elif b > 0:
		b = f" - {b}x"
	else:
		b = ""

	if q < 0:
		q = f" - {-q}"
	elif q > 0:
		q = f" + {q}"
	else:
		q = ""

	return f"x^2{b}{q} = 0"

def latex():
	system(f"pdflatex {filename}")

def main():
	equations = [type_eq(b, q) for b, q in generate_coefs()]
	shuffle(equations)
	if LIMIT:
		equations = equations[:LIMIT]

	if tex:
		with open(filename, 'w') as f:
			f.write(template.replace("% {equations}",
				"\n".join( (f"\\item ${e}$" for e in equations) ) ))
		latex()
	else:
		with open(filename, 'w') as f:
			print(len(equations), 'equations', file=f)
			print("\n".join(equations), file=f)



if __name__ == '__main__':
	main()
