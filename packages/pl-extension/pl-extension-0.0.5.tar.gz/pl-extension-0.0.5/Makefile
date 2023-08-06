
dev:
	pip3 install -r requirements/develop.txt
	pre-commit install

build:
	python setup.py build

upload:
	@rm -rf dist
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload --repository pypi dist/* --verbose

clean:
	@rm -rf build dist *.egg-info

test:
	python /usr/bin/nosetests -s tests --verbosity=2 --rednose --nologcapture

pep8:
	autopep8 pl_extension --recursive -i

lint:
	pylint pl_extension --reports=n

lintfull:
	pylint pl_extension

install:
	python setup.py install

uninstall:
	python setup.py install --record install.log
	cat install.log | xargs rm -rf 
	@rm install.log
