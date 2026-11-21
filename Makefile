PYTHON ?= python3
CONVERT ?= convert

.PHONY: all clean check hardware
all: build/visual-prototype-dev.xex build/visual-prototype-dev.json build/hardware-dev.xex

hardware: build/hardware-dev.xex

build/hardware-dev.xex: build/visual-prototype-dev.xex tools/build_hardware_xex.py tools/build_audio_revision.py tools/build_compact_xex.py tools/build_avg_late_lowram.py releases/less-i-know-demo-release-058-stereo.xex releases/less-i-know-demo-release-133-stereo.xex
	$(PYTHON) tools/build_hardware_xex.py $< $@ --replace-dev --approved-music --earlier-percussion

check: build/visual-prototype-dev.xex build/visual-prototype-dev.json build/kaleidoscope.xex
	$(PYTHON) -c "import py65"
	$(PYTHON) -m unittest discover -s tests -v

build/title.gray: tools/build_title.py
	$(PYTHON) tools/build_title.py

build/kaleidoscope.gray: assets/art/source/act5_kaleidoscope.png
	mkdir -p build
	$(CONVERT) $< -resize 160x192\! -colorspace gray -depth 8 gray:$@

build/dance-v056-0.rgb build/dance-v056-1.rgb build/dance-v056-2.rgb build/dance-v056-3.rgb &: assets/art/source/act1_cheer_dance_v056.png
	mkdir -p build
	$(CONVERT) $< -crop 2x2@ +repage -filter point -resize 48x128\! -depth 8 +adjoin rgb:build/dance-v056-%d.rgb

build/gym-v056.rgb: assets/art/source/act1_gym_dance_v056.png
	mkdir -p build
	$(CONVERT) $< -filter point -resize 160x192\! -depth 8 rgb:$@

VIDEO_INPUTS = assets/art/reference/v175/basketball.bin assets/art/reference/v175/arena-pan.bin build/kaleidoscope.gray build/gym-v056.rgb \
    build/ribbon-dancer-v136.rgb build/ribbon-side-v142.rgb build/ribbon-overhead-v145.rgb build/ribbon-inbetweens-v166.rgb build/ribbon-inbetweens-v171.rgb build/ribbon-inbetweens-v173.rgb build/arena-exterior-v151.rgb build/arena-interior-v151.rgb build/boy-floor-v145.rgb \
    $(addprefix build/dance-v056-,0.rgb 1.rgb 2.rgb 3.rgb) \
    build/school.rgb build/school-neutral.rgb build/school-front.rgb build/north-girl.rgba build/north-girl-close.rgba build/school-girl-side-v033.rgb \
    build/practice-storyboard.rgb build/crush-portraits.rgb \
    build/girl-walk-cycle-v177.rgba build/boy-whistle-v177.rgba \
    $(addprefix build/trevor-panel-,0.rgb 1.rgb 2.rgb 3.rgb) \
    $(addprefix build/trevor-pmg-,0.rgb 1.rgb) \
    $(addprefix build/trevor-polished-,0.rgb 1.rgb 2.rgb 3.rgb)

build/visual-prototype-dev.xex build/visual-prototype-dev.json &: $(wildcard tools/*.py) less-i-know-release-v035.xex $(VIDEO_INPUTS)
	$(PYTHON) tools/build_bitmap_sequence.py --replace

build/kaleidoscope.xex: less-i-know-release-v035.xex build/kaleidoscope.gray tools/build_visual_prototype.py tools/extract_music.py
	$(PYTHON) tools/build_visual_prototype.py $< build/kaleidoscope.gray $@

clean:
	rm -f build/kaleidoscope.gray build/visual-prototype-dev.xex build/visual-prototype-dev.json build/title.gray build/title.pgm build/kaleidoscope.xex

build/practice-storyboard.rgb: assets/art/source/act1_practice_storyboard_v011.png
	$(CONVERT) $< -filter point -resize 160x192\! -depth 8 rgb:$@

build/crush-portraits.rgb: assets/art/source/act2_cheer_performance_v015.png
	$(CONVERT) $< -filter point -resize 160x104\! -depth 8 rgb:$@

build/school.rgb: assets/art/source/act1_school_court_boy.png
	$(CONVERT) $< -filter point -resize 160x64\! -depth 8 rgb:$@

build/school-front.rgb: assets/art/source/act1_boy_front_v170.png
	$(CONVERT) $< -filter point -resize 160x64\! -depth 8 rgb:$@

build/north-girl.rgba: assets/art/source/act1_north_girl.png
	$(CONVERT) $< -filter point -resize 48x64\! -depth 8 rgba:$@

build/north-girl-close.rgba: assets/art/source/act1_north_girl.png
	$(CONVERT) $< -filter point -resize 96x128\! -depth 8 rgba:$@

build/school-girl-side-v033.rgb: assets/art/source/act1_girl_side_walking_v033.png
	$(CONVERT) $< -filter point -resize 160x64\! -depth 8 rgb:$@

build/girl-walk-cycle-v177.rgba build/boy-whistle-v177.rgba build/basketball-hero-v177.rgba &: tools/prepare_production_art.py assets/art/source/act1_girl_walk_cycle_v177.png assets/art/source/act1_boy_whistle_v177.png assets/art/source/act3_basketball_hero_v177.png
	$(PYTHON) tools/prepare_production_art.py

build/trevor-panel-0.rgb build/trevor-panel-1.rgb build/trevor-panel-2.rgb build/trevor-panel-3.rgb &: assets/art/source/act4_trevor_awakens_v025.png
	$(CONVERT) $< -crop 2x2@ +repage -filter point -resize 160x64\! -depth 8 +adjoin rgb:build/trevor-panel-%d.rgb

build/trevor-pmg-0.rgb build/trevor-pmg-1.rgb &: assets/art/source/act4_trevor_awakens_v025.png
	$(CONVERT) $< -crop 2x2@ +repage -delete 0,1 -trim +repage -filter point -resize 16x24\! -depth 8 +adjoin rgb:build/trevor-pmg-%d.rgb

build/trevor-polished-0.rgb build/trevor-polished-1.rgb build/trevor-polished-2.rgb build/trevor-polished-3.rgb &: assets/art/source/act4_trevor_polished_v043.png
	$(CONVERT) $< -crop 2x2@ +repage -filter point -resize 160x64\! -depth 8 +adjoin rgb:build/trevor-polished-%d.rgb

build/ribbon-dancer-v136.rgb: assets/art/source/act2_ribbon_dancer_v136.png
	$(CONVERT) $< -depth 8 rgb:$@

build/ribbon-side-v142.rgb: assets/art/source/act2_ribbon_side_v142.png
	$(CONVERT) $< -depth 8 rgb:$@

build/ribbon-overhead-v145.rgb: assets/art/source/act2_ribbon_overhead_v145.png
	$(CONVERT) $< -resize 1774x887\! -depth 8 rgb:$@

build/ribbon-inbetweens-v166.rgb: assets/art/source/act2_ribbon_inbetweens_v166.png
	$(CONVERT) $< -resize 1329x1329\! -depth 8 rgb:$@

build/ribbon-inbetweens-v171.rgb: assets/art/source/act2_ribbon_inbetweens_v171.png
	$(CONVERT) $< -resize 1329x1329\! -depth 8 rgb:$@

build/ribbon-inbetweens-v173.rgb: assets/art/source/act2_ribbon_inbetweens_v173.png
	$(CONVERT) $< -resize 1329x1329\! -depth 8 rgb:$@

build/boy-floor-v145.rgb: assets/art/source/act8_boy_floor_v145.png
	$(CONVERT) $< -filter point -resize 144x56\! -depth 8 rgb:$@


build/arena-exterior-v151.rgb: assets/art/source/act1_atari_arena_exterior_v151.png
	$(CONVERT) $< -filter point -resize 200x64\! -depth 8 rgb:$@

build/arena-interior-v151.rgb: assets/art/source/act3_atari_arena_interior_v151.png
	$(CONVERT) $< -filter point -resize 160x56\! -depth 8 rgb:$@

build/school-neutral.rgb: assets/art/source/act1_boy_front.png
	$(CONVERT) $< -filter point -resize 160x64\! -depth 8 rgb:$@
