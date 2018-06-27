all: README.pdf README.html

%.pdf: %.md header.tex
	pandoc -F all.py -H header.tex -V numbersections:true $< -o $@

%.html: %.md style.css
	pandoc -F linkref.py --css style.css $< -o $@
