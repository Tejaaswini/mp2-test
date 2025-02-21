PYTHON = python3
PYINSTALLER = pyinstaller
SCRIPT = mp2.py
SPEC = mp2.spec
OUTPUT_DIR = dist
BUILD_DIR = build
EXECUTABLE = $(OUTPUT_DIR)/mp2

all: build

build:
	$(PYINSTALLER) --clean --onefile $(SCRIPT)

build_from_spec:
	$(PYINSTALLER) --clean $(SPEC)

clean:
	rm -rf $(BUILD_DIR) $(OUTPUT_DIR) __pycache__ *.spec

run:
	$(EXECUTABLE)

