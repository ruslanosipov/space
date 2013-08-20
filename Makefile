test:
	python runtests.py
	python doctests.py

clean:
	find . -name *.pyc -delete
