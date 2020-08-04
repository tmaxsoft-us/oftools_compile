init:
	pip3 install -r requirements.txt

build:
    python3 setup.py sdist

install:
	python3 setup.py bdist_wheel
	pip3 install dist/*.whl --user

uninstall:
	pip3 uninstall oftools-compile
	rm dist build oftools_compile.egg-info -r

upload:
	python3 setup.py sdist upload -r pypi

upload_test:
	python3 setup.py sdist upload -r testpypi

remove:
	echo "curl --form ":action=remove_pkg" --form "name=oftools_compile" --form "version=0.0.1" URL -u id:pass"

yapf:
	yapf3 --style='{ based_on_style: google }' *.py -ir

test:
	coverage run --source oftools_compile -m py.test -v -s
	coverage report
