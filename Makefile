init:
	pip3 install -r requirements.txt

build:
	python3 setup.py sdist

install:
	python3 setup.py bdist_wheel
	pip3 install dist/*.whl

install_user:
	python3 setup.py bdist_wheel
	pip3 install dist/*.whl --user

uninstall:
	rm -r build dist oftools_compile.egg-info
	pip3 uninstall oftools-compile

reinstall:
	rm -r build dist oftools_compile.egg-info
	pip3 uninstall oftools-compile
	python3 setup.py bdist_wheel
	pip3 install dist/*.whl

upload_pypi:
	python3 setup.py sdist upload -r pypi

upload_testpypi:
	python3 setup.py sdist upload -r testpypi

remove:
	echo "curl --form ":action=remove_pkg" --form "name=oftools-compile" --form "version=0.0.1" URL -u id:pass

yapf:
	yapf3 --style='{ based_on_style: google }' *.py -ir

# Optional arguments:
# --maxfail = <num> : Stop test suite after n test failures
pytest_integration:
	pytest tests/integration/ -c pytest.ini --color=yes -v

pytest_unit:
	pytest tests/unit/ -c pytest.ini --color=yes -v

coverage:
	coverage run --source oftools_compile -m py.test -v -s
	coverage report
