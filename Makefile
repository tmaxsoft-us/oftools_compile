init:
	pip3 install -r requirements.txt

uninstall:
	pip3 uninstall oftools_compile
	rm dist build oftools_compile.egg-info -r

install:
	python3 setup.py sdist bdist_wheel
	pip3 install dist/*.tar.gz

upload:
	python3 setup.py sdist upload -r master

remove:
	echo "curl --form ":action=remove_pkg" --form "name=oftools_compile" --form "version=0.0.1" URL -u id:pass"

yapf:
	yapf3 --style='{ based_on_style: google }' *.py -ir

html:
	mkdir -p build
	cp docs/README.md build/README.md
	grip build/README.md --title=oftools_compile --export

test:
	pytest -s -v
