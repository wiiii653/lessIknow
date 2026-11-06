PYTHON ?= python3
CONVERT ?= convert

.PHONY: all clean check
all: build/visual-prototype-v070.xex

check: build/visual-prototype-v070.xex build/kaleidoscope.xex
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

build/school.rgb: assets/art/source/act1_school_court_boy.png
	mkdir -p build
	$(CONVERT) $< -filter point -resize 160x64\! -depth 8 rgb:$@

build/school-front.rgb: assets/art/source/act1_boy_front.png
	mkdir -p build
	$(CONVERT) $< -filter point -resize 160x64\! -depth 8 rgb:$@

build/north-girl.rgba: assets/art/source/act1_north_girl.png
	mkdir -p build
	$(CONVERT) $< -filter point -resize 48x64\! -depth 8 rgba:$@

build/visual-prototype-v070.xex: less-i-know-release-v035.xex tools/build_bitmap_sequence.py tools/build_sequence.py tools/title_mode.py tools/music_timing.py tools/gym_background.py tools/gym_practice.py tools/dance_banks.py tools/engine_effects.py tools/crush_portraits.py tools/build_title.py tools/build_visual_prototype.py tools/extract_music.py tools/os_ram.py tools/school_story.py tools/school_portrait_bank.py tools/rainbow_ball.py tools/pompom_effects.py tools/basketball_hero.py tools/trevor_awakens.py tools/trevor_polished.py tools/mosaic.py tools/school_parallax.py tools/tunnel_ball.py tools/scene_memory.py build/kaleidoscope.gray build/gym-v056.rgb build/dance-v056-0.rgb build/dance-v056-1.rgb build/dance-v056-2.rgb build/dance-v056-3.rgb build/school.rgb build/school-front.rgb build/north-girl.rgba build/practice-storyboard.rgb build/crush-portraits.rgb build/school-girl-side-v033.rgb build/school-wide-v034.rgb build/school-girl-cutout-v034.rgba build/basketball-hero.rgb build/trevor-panel-0.rgb build/trevor-pmg-0.rgb build/trevor-polished-0.rgb
	$(PYTHON) tools/build_bitmap_sequence.py

build/kaleidoscope.xex: less-i-know-release-v035.xex build/kaleidoscope.gray tools/build_visual_prototype.py tools/extract_music.py
	$(PYTHON) tools/build_visual_prototype.py $< build/kaleidoscope.gray $@

clean:
	rm -f build/kaleidoscope.gray build/visual-prototype-v070.xex build/title.gray build/title.pgm build/kaleidoscope.xex

build/practice-storyboard.rgb: assets/art/source/act1_practice_storyboard_v011.png
	$(CONVERT) $< -filter point -resize 160x192\! -depth 8 rgb:$@

build/crush-portraits.rgb: assets/art/source/act2_cheer_performance_v015.png
	$(CONVERT) $< -filter point -resize 160x104\! -depth 8 rgb:$@

build/school-girl-front.rgb: assets/art/source/act1_blonde_portraits_reserved_v014.png
	$(CONVERT) $< -crop 50%x50%+0+0 +repage -delete 1--1 -filter point -resize 160x64\! -depth 8 rgb:$@

build/basketball-hero.rgb: assets/art/source/act3_basketball_hero_v024.png
	$(CONVERT) $< -filter point -resize 320x168\! -depth 8 rgb:$@

build/trevor-panel-0.rgb build/trevor-panel-1.rgb build/trevor-panel-2.rgb build/trevor-panel-3.rgb &: assets/art/source/act4_trevor_awakens_v025.png
	$(CONVERT) $< -crop 2x2@ +repage -filter point -resize 160x64\! -depth 8 +adjoin rgb:build/trevor-panel-%d.rgb

build/trevor-pmg-0.rgb build/trevor-pmg-1.rgb &: assets/art/source/act4_trevor_awakens_v025.png
	$(CONVERT) $< -crop 2x2@ +repage -delete 0,1 -trim +repage -filter point -resize 16x24\! -depth 8 +adjoin rgb:build/trevor-pmg-%d.rgb

build/school-girl-side-v033.rgb: assets/art/source/act1_girl_side_walking_v033.png
	$(CONVERT) $< -filter point -resize 160x64\! -depth 8 rgb:$@

build/school-wide-v034.rgb build/school-girl-cutout-v034.rgba &: tools/prepare_school_pan.py assets/art/source/act1_school_background_v034.png assets/art/source/act1_girl_side_walking_v033.png
	python3 tools/prepare_school_pan.py

build/trevor-polished-0.rgb build/trevor-polished-1.rgb build/trevor-polished-2.rgb build/trevor-polished-3.rgb &: assets/art/source/act4_trevor_polished_v043.png
	$(CONVERT) $< -crop 2x2@ +repage -filter point -resize 160x64\! -depth 8 +adjoin rgb:build/trevor-polished-%d.rgb
