PYTHON ?= python3
OUT ?= build

.PHONY: all check clean

all: $(OUT)/loader-clone-copy.xex $(OUT)/loader-clone-direct.xex

$(OUT)/loader-clone-copy.xex: build.py
	$(PYTHON) build.py --output $@

$(OUT)/loader-clone-direct.xex: build.py
	$(PYTHON) build.py --mode direct --output $@

check:
	$(PYTHON) check.py

clean:
	rm -rf $(OUT)
