"""Select the working build, or an explicit archived XEX for comparisons."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XEX = ROOT / os.environ.get('ATARI_TEST_XEX', 'build/visual-prototype-dev.xex')
METADATA = XEX.with_suffix('.json')
