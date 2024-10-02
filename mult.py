#!/usr/bin/env python

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
\setlength\columnsep{1.7pc}
\begin{document}
\begin{multicols}{4}
\begin{enumerate}[font=\tiny]
% {equations}
\end{enumerate}
\end{multicols}
\end{document}
"""
# allow_1 = False
allow_1 = True

def generate_triplet():
	x = randrange(1 if allow_1 else 2, 19 if allow_1 else 12)
	if x >= 10:
		x += 1
	if x > 12:
		y = 1
	elif x == 12:
		y = randrange(1 if allow_1 else 2, 4)
	else:
		y = randrange(2, 10)
	return x, y, x * y

def maybe_shuffle(x, y, z):
	if randrange(2):
		return x, y, z
	return y, x, z

def add_zeros(x, y, z):
	zx = randrange(1 if x == 1 else 0, 3)
	zy = randrange(1 if y == 1 else 0, min(3, 5 - zx - (len(str(z)) - 1)))
	return x*10**zx, y*10**zy, z*10**zx*10**zy

def generate_equation(x, y, z):
	if randrange(2):
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
	equations = generate_equations(132)
	write_files(template, equations)
	if tex:
		latex()


if __name__ == "__main__":
	main()
