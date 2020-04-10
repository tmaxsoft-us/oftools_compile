init:
	pip3 install -r requirements.txt

uninstall:
	pip3 uninstall oftools_compile
	rm dist build oftools_compile.egg-info -r

clean:
	rm dist build oftools_compile.egg-info -r

install:
	python3 setup.py sdist bdist_wheel
	pip3 install dist/*.tar.gz

yapf:
	yapf3 --style='{ based_on_style: google, indent_width:4 ,  column_limit:79}' *.py -ir

test:
	pytest -s -v
