# make -f Makefile_pdflatex

R = paper
STY = style/*.cls

pdf: $(R).pdf

$(R).bbl: $(R).bib
	pdflatex $(R)
	bibtex $(R)
	pdflatex $(R)

$(R).pdf: *.tex $(STY) $(R).bbl
	pdflatex $(R)
	pdflatex $(R)

clean:
	rm -f $(R).log $(R).aux $(R).bbl $(R).blg $(R).out
