build:
	pipenv run python main.py

latex_dependencies:
	mkdir -p latex
	cd academic-cv/;make;cp *.sty *.cls ../latex

build_pdf: latex_dependencies
	cd latex/; latexmk -pdf resume.tex; cp resume.pdf ../output/academic/gaetan_staquet.pdf

dependencies: latex_dependencies
	pipenv --python 3.11
	pipenv install --dev

clean:
	rm -fr output

nuke: clean
	pipenv --rm
	rm -f Pipfile.lock
	rm -r latex
