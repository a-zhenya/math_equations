#!/usr/bin/env python3

from random import randrange
from itertools import chain
from os import system

tex = True
filename = 'mult.tex' if tex else 'mult.txt'
template = r"""
\documentclass[a4paper,12pt]{article}
\usepackage[a4paper, total={7in, 11in}]{geometry}
\usepackage[latin1]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{euler}
\usepackage{multicol}
\usepackage{enumitem}
\pagestyle{empty}
\makeatletter
\renewcommand\@oddfoot{\vbox{\hbox to \textwidth{\hfill Printed: \today\hfill}\vspace{1pc}}}
\makeatother
\setlength\columnsep{1.7pc}
\begin{document}
\begin{multicols}{3}
\begin{enumerate}[font=\tiny]
% {equations}
\end{enumerate}
\end{multicols}
\end{document}
"""
# allow_1 = False
allow_1 = True

def generate_triplet():
	while True:
		x = randrange(21, 100)
		if x % 10 != 0 and x % 11 != 0:
			break
	while True:
		y = randrange(21, 100)
		if y % 10 != 0 and y % 11 != 0:
			break
	return x, y, x * y

def maybe_shuffle(x, y, z):
	if randrange(2):
		return x, y, z
	return y, x, z

def add_zeros(x, y, z):
	zx = randrange(1, 3)
	zy = randrange(1, 2 if zx == 2 else 3)
	return x*10**zx, y*10**zy, z*10**zx*10**zy

def generate_equation(x, y, z):
	if randrange(1) == 0:
		return str(x), '*', str(y)
	else:
		return str(z), ':', str(x)

OP_MAP = {
	'*': '\\cdot',
}
def type_equation(x, op, y):
	if tex:
		op = OP_MAP.get(op, op)
	return f"{x} {op} {y} ="

pipeline = [
	maybe_shuffle,
] +	([add_zeros] if allow_1 else []) + [
	generate_equation,
	type_equation,
]
def apply_pipeline(x, y, z):
	for f in pipeline[:-1]:
		x, y, z = f(x, y, z)
	return pipeline[-1](x, y, z)

def generate_equations(count):
	triplets = []
	while len(triplets) < count:
		eq = generate_triplet()
		if eq in triplets[-50:]:
			continue
		if any(x in set(chain.from_iterable(triplets[-2:])) for x in eq):
			continue
		triplets.append(eq)
	equations = [
		apply_pipeline(*eq)
		for eq in triplets
	]

	return equations

def write_files(template, equations):
	if tex:
		with open(filename, 'w') as eq:
			eq.write(template.replace("% {equations}",
				"\n".join( (f"\\item ${e}$" for e in equations) ) ))
	else:
		with open(filename, 'w') as eq:
			eq.write("\n".join(equations))

def latex():
	system(f"pdflatex {filename}")

def main():
	equations = generate_equations(102)
	write_files(template, equations)
	if tex:
		latex()


if __name__ == "__main__":
	main()
