build: wow-launcher-script.py
	cmd.exe /C python -m nuitka --standalone --mingw64 --plugin-enable=numpy --experimental=use_pefile --experimental=use_pefile_recurse --experimental=use_pefile_fullrecurse wow-launcher-script.py
	cp -r patterns/ wow-launcher-script.dist/
	cp README.md wow-launcher-script.dist/

clean:
	rm -rf *.dist *.build

run:
	cmd.exe /C python wow-launcher-script.py
