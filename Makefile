empty = /dev/null
filename = main.tex
output_name_ita = cv_ita
output_name_eng = cv_eng


ita:
	latexmk -g -synctex=1 -interaction=nonstopmode -file-line-error -pdf $(filename) -jobname=$(output_name_ita) -pdflatex="lualatex --file-line-error --shell-escape --synctex=1"

eng:
	latexmk -g -synctex=1 -interaction=nonstopmode -file-line-error -pdf $(filename) -jobname=$(output_name_eng) -pdflatex="/usr/bin/pdflatex --file-line-error --shell-escape --synctex=1 %O '\def\eng{1}\input{$(filename)}'"

all:
	latexmk -g -synctex=1 -interaction=nonstopmode -file-line-error -pdf $(filename) -jobname=$(output_name_ita) -pdflatex="lualatex --file-line-error --shell-escape --synctex=1"
	latexmk -g -synctex=1 -interaction=nonstopmode -file-line-error -pdf $(filename) -jobname=$(output_name_eng) -pdflatex="/usr/bin/pdflatex --file-line-error --shell-escape --synctex=1 %O '\def\eng{1}\input{$(filename)}'"


.PHONY: clean
clean:
	rm -f $(output_name_ita).blg 2> $(empty)
	rm -f $(output_name_ita).log 2> $(empty)
	rm -f $(output_name_ita).out 2> $(empty)
	rm -f $(output_name_ita).fls 2> $(empty)
	rm -f $(output_name_ita).synctex.gz 2> $(empty)

	rm -f $(output_name_ita).aux 2> $(empty)
	rm -f $(output_name_ita).bbl 2> $(empty)
	rm -f $(output_name_ita).fdb_latexmk 2> $(empty)

	rm -f $(output_name_eng).blg 2> $(empty)
	rm -f $(output_name_eng).log 2> $(empty)
	rm -f $(output_name_eng).out 2> $(empty)
	rm -f $(output_name_eng).fls 2> $(empty)
	rm -f $(output_name_eng).synctex.gz 2> $(empty)

	rm -f $(output_name_eng).aux 2> $(empty)
	rm -f $(output_name_eng).bbl 2> $(empty)
	rm -f $(output_name_eng).fdb_latexmk 2> $(empty)