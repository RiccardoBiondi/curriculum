empty = /dev/null
filename = main.tex
output_name_ita = cv_ita
output_name_eng = cv_eng


all:
	latexmk -g -synctex=1 -interaction=nonstopmode -file-line-error -pdf $(filename) -jobname=$(output_name_ita) -pdflatex="lualatex --file-line-error --shell-escape --synctex=1"