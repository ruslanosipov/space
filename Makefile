test:
	nosetests tests/*.py

coverage:
	nosetests tests/*.py --with-coverage --cover-branches --cover-html --cover-package=lib

clean:
	find . -name *.pyc -delete
	rm -f .coverage
	rm -rf cover/
