build: wow-launcher-script.py
    python3 -m nuitka --standalone wow-launcher-script.py

clean:
    rm -rf ./*.dist ./*.build
