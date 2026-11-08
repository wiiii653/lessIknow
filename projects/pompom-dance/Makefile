PYTHON ?= python3
CONVERT ?= convert

.PHONY: all check playback
all: build/pompom-dance-dev.xex build/pompom-dance-dev.json

build/dance-v056-0.rgb build/dance-v056-1.rgb build/dance-v056-2.rgb build/dance-v056-3.rgb &: assets/art/source/act1_cheer_dance_v056.png
	mkdir -p build
	$(CONVERT) $< -crop 2x2@ +repage -filter point -resize 48x128\! -depth 8 +adjoin rgb:build/dance-v056-%d.rgb

build/gym-v056.rgb: assets/art/source/act1_gym_dance_v056.png
	mkdir -p build
	$(CONVERT) $< -filter point -resize 160x192\! -depth 8 rgb:$@

build/pompom-dance-dev.xex build/pompom-dance-dev.json &: $(wildcard tools/*.py) build/gym-v056.rgb $(addprefix build/dance-v056-,0.rgb 1.rgb 2.rgb 3.rgb) player/less-i-know-release-v035.xex reference/dance_frames_v141.bin
	$(PYTHON) tools/build_pompom_demo.py --replace

check: all
	$(PYTHON) -m unittest discover -s tests -v

playback: all
	$(PYTHON) tools/check_playback.py --seconds 20
