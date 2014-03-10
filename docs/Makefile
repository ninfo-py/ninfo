all: pres.pdf pres.html

pres.html: pres.md
	pandoc -s -t slidy  pres.md -o pres.html

pres.pdf: pres.md
	pandoc -s -t beamer pres.md -o pres.pdf -V theme:Madrid -V colortheme=beaver
