"""Package a stereo prototype using the hardware-confirmed release 058 loader.

The reference is immutable. Refuse unexpected loader changes instead of silently
shipping a new bank-loading protocol. See docs/HARDWARE_LOADER_CONTRACT.md.
"""
import argparse
import hashlib
from pathlib import Path

from build_avg_late_lowram import build as late_lowram
from build_compact_xex import build as compact, fast_clear_code
from build_visual_prototype import xex_segment
from extract_music import segments
from school_portrait_bank import loader

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / 'releases/less-i-know-demo-release-058-stereo.xex'
REFERENCE_SHA256 = 'f3c14bc36b96220ead8fbe24df2e0dfc7ef5d30371d5cd83d11f808b62706b8f'
APPROVED_STEREO = ROOT / 'releases/less-i-know-demo-release-133-stereo.xex'
APPROVED_STEREO_SHA256 = 'e56ea5f05ba6af99a019612fbfd283b0ed948725c90fc56bab1459a16ef5c43f'
RELEASE_122 = ROOT / 'releases/less-i-know-demo-release-122-stereo.xex'
RELEASE_122_SHA256 = 'fb19ccf0c1cad0b5a9950fb44ee36e577ac6af84e774782629d6763d8e11c0d4'
LOW_ENDS = {0x0400: 0x07df, 0x0800: 0x08bf, 0x0900: 0x0976,
            0x0980: 0x09ff, 0x0a00: 0x0bff}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def with_approved_music(data, *, earlier_percussion=False, release_122=False):
    """Copy the approved stereo stream and decoder tables into a raw prototype."""
    approved = (RELEASE_122 if release_122 else APPROVED_STEREO).read_bytes()
    expected_hash = RELEASE_122_SHA256 if release_122 else APPROVED_STEREO_SHA256
    require(hashlib.sha256(approved).hexdigest() == expected_hash,
            'Approved stereo music source changed')
    entries = list(segments(approved))
    bank_size = 0x4000
    music_end = 7 * bank_size + 0x0b10
    table_addresses = (0x2e00, 0x2e80, 0x2f00)
    tables = {a: p for a, _, p in entries if a in table_addresses}
    clears = [i for i, (a, _, _) in enumerate(entries) if a == 0x3a00]
    music = bytearray()
    for begin, end in zip(clears[:8], clears[1:9]):
        bank = bytearray(bank_size)
        for a, b, payload in entries[begin:end]:
            if 0x8000 <= a <= b <= 0xbfff:
                bank[a-0x8000:b-0x8000+1] = payload
        music.extend(bank)
    require(len(music) == 8 * bank_size, 'Incomplete approved music banks')

    if earlier_percussion or release_122:
        from build_audio_revision import decode, encode, music_packets, training_build_and_drop

        dictionary = [lo | mi << 8 | hi << 16
                      for lo, mi, hi in zip(*(tables[a] for a in table_addresses))]
        packets = decode(music[:music_end], dictionary)
        source = music_packets(data)
        require(len(packets) == len(source) == 59833, 'Unexpected music update count')
        if release_122:
            from build_sequence import DANCE_TICK
            from gym_practice import PRACTICE_TICK
            for tick in range(DANCE_TICK):
                packet = bytearray(packets[tick])
                packet[5] &= 0xf0
                if tick >= PRACTICE_TICK:
                    # Ease both bass channels down through the training shots.
                    # Return to the approved level before the dancer enters.
                    fade_in = min(1.0, (tick - PRACTICE_TICK) / 64)
                    fade_out = min(1.0, (DANCE_TICK - tick) / 64)
                    gain = 1.0 - 0.2 * min(fade_in, fade_out)
                    for control in (3, 12):
                        packet[control] = (packet[control] & 0xf0) | round((packet[control] & 15) * gain)
                packets[tick] = bytes(packet)
        else:
            training_build_and_drop(packets, source)
        stream, dictionary = encode(packets)
        require(len(stream) <= music_end, 'Music exceeds existing bank allocation')
        music = stream.ljust(music_end, b'\xff')
        tables = {a: bytes((mask >> (8 * i)) & 255 for mask in dictionary)
                  for i, a in enumerate(table_addresses)}

    output = bytearray(b'\xff\xff')
    offset = 0
    seen_tables = set()
    for a, b, payload in segments(data):
        if (a, b) == (0x8000, 0xbfff) and offset < music_end:
            replacement = music[offset:min(offset+bank_size,music_end)]
            payload = replacement + payload[len(replacement):]
            offset += len(replacement)
        elif a in tables:
            require(len(payload) == len(tables[a]), f'Music table size changed at ${a:04X}')
            payload = tables[a]
            seen_tables.add(a)
        output.extend(xex_segment(a, payload))
    require(offset == music_end and seen_tables == set(table_addresses),
            'Prototype is missing the v035 music layout')
    return bytes(output)


def build(data, reference=None, *, fast_clear=False):
    reference = REFERENCE.read_bytes() if reference is None else reference
    require(hashlib.sha256(reference).hexdigest() == REFERENCE_SHA256,
            'Hardware reference 058 changed')
    ref = list(segments(reference))
    entries = list(segments(data))
    wrappers = [p for a, b, p in ref if a == 0x3900]
    bank_loaders = [p for a, b, p in ref if a == 0x1000]
    player = next(p for a, b, p in ref if a == 0x2000)
    require([a for a, b, p in ref[:4]] == [0x3800, 0x3880, 0x38a0, 0x2e2],
            'Unexpected reference screen')
    out = bytearray(b'\xff\xff')
    for a, b, p in ref[:4]:
        out.extend(xex_segment(a, p))
    init_count = bank_count = screens = 0
    i = 0
    while i < len(entries):
        a, b, p = entries[i]
        # Remove only the early prototype screen, never later runtime low RAM.
        if a == 0x0600 and screens == 0:
            screen = entries[i:i+4]
            require([s[0] for s in screen] == [0x0600, 0x0700, 0x0780, 0x2e2]
                    and screen[-1][2] == b'\x80\x07', 'Unexpected prototype screen')
            screens += 1
            i += 4
            continue
        if a == 0x2000:
            p = bytearray(p)
            require(p[7:10] == bytes.fromhex('8d 00 d4'), 'Unexpected bank probe DMA')
            p[7:10] = b'\xea' * 3
            require(p[:0x146] == player[:0x146], 'Original music-bank loader changed')
        if a == 0x1000:
            require(bank_count < len(bank_loaders), 'Too many bank loaders')
            expected = bank_loaders[bank_count]
            if p != expected and bank_count < 50:
                # Accept only the known prototype ellipsis addition, then use
                # exactly the old loader, including its bank selector logic.
                generated = list(segments(b'\xff\xff' + loader(bytes(16384), bank_count, progress=True)))
                require(p == generated[1][2], f'Unexpected bank loader {bank_count}')
            else:
                require(p == expected, f'Unexpected OS loader {bank_count}')
            p = expected
            bank_count += 1
        if a == 0x2e2:
            require(init_count < len(wrappers), 'Too many INITs')
            wrapper = wrappers[init_count]
            require(wrapper[28] == 0x20 and p == wrapper[29:31],
                    f'INIT {init_count + 1} target/order changed')
            out.extend(xex_segment(0x3900, wrapper))
            p = b'\x00\x39'
            init_count += 1
        if init_count == 66 and a in LOW_ENDS:
            # v353's helper shrank by two bytes. Pad its unused tail so the
            # proven bootstrap retains exactly the same copy spans as 058.
            require(b <= LOW_ENDS[a], f'Runtime exceeds reference span at ${a:04X}')
            p = bytes(p) + bytes(LOW_ENDS[a] - b)
        out.extend(xex_segment(a, p))
        i += 1
    require((screens, init_count, bank_count) == (1, 66, 51), 'Incomplete prototype')
    result = late_lowram(compact(bytes(out)))
    final = list(segments(result))
    # Compare the full load protocol, not just INIT addresses/counts.
    for address in (0x3800, 0x3880, 0x38a0, 0x3900, 0x3a00, 0x4800, 0x1000, 0x2e2):
        require([p for a, b, p in final if a == address] ==
                [p for a, b, p in ref if a == address],
                f'Hardware loader differs at ${address:04X}')
    if fast_clear:
        result = replace_staging_clear(final)
    require(len(result) < 1024 * 1024, 'Hardware XEX exceeds the established size bound')
    return result


def replace_staging_clear(entries):
    """Change only the audited clear segments in an already validated XEX."""
    start = 0x3a00
    code = fast_clear_code()
    end = start + len(code) - 1
    clear_indices = [i for i, (a, _, _) in enumerate(entries) if a == start]
    require(len(clear_indices) == 64, 'Expected 64 staging clears')
    last_clear = clear_indices[-1]
    bootstrap = next(i for i, (a, _, _) in enumerate(entries) if a == 0x4800)
    require(any(a <= start <= end <= b for a, b, _ in entries[last_clear + 1:bootstrap]),
            'Late runtime must overwrite the staging clear workspace')
    out = bytearray(b'\xff\xff')
    for i, (a, b, payload) in enumerate(entries):
        if a == start:
            require(entries[i + 1] == (0x02e2, 0x02e3, b'\x00\x3a'),
                    'Staging clear is missing its INIT')
            payload = code
        elif a <= end and start <= b:
            require(i > last_clear, 'Fast clear overlaps loader memory')
        out.extend(xex_segment(a, payload))
    return bytes(out)


def with_runad_handoff(data):
    """Install the base-RAM startup used in AVG-tested prerelease 187."""
    entries = list(segments(data))
    init_vector = xex_segment(0x02e2, b'\x00\x48')
    run_vector = xex_segment(0x02e0, b'\xe0\x13')
    tail = init_vector + run_vector
    require(data.endswith(tail)
            and entries[-2:] == [(0x02e2, 0x02e3, b'\x00\x48'),
                                 (0x02e0, 0x02e1, b'\xe0\x13')]
            and [entry[:2] for entry in entries[-4:-2]] == [
                (0x4000, 0x47ff), (0x4800, 0x4873)],
            'Unexpected low-RAM restore and startup records')
    stub_address = 0x3fb0
    stub = bytes.fromhex(
        '78 a9 00 8d 0e d4 8d 00 d4 8d 2f 02'  # Disable IRQ, NMI and DMA.
        ' a9 ff 8d 01 d3 4c 00 48'              # Select base RAM and enter bootstrap.
    )
    stub_end = stub_address + len(stub) - 1
    require(all(end < stub_address or start > stub_end for start, end, _ in entries),
            'RUNAD stub overlaps existing XEX data')
    result = (data[:-len(tail)] + xex_segment(stub_address, stub)
              + xex_segment(0x02e0, stub_address.to_bytes(2, 'little')))
    require(len(result) < 1024 * 1024, 'Hardware XEX exceeds the established size bound')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--replace-dev', action='store_true',
                        help='replace only build/hardware-dev.xex')
    parser.add_argument('--animated-loading', action='store_true',
                        help='show the finale star during bank loading')
    parser.add_argument('--full-rate-loading', action='store_true',
                        help='use the full finale star animation in a loader VBI')
    parser.add_argument('--runad-handoff', action='store_true',
                        help='use the AVG-tested base-RAM startup from prerelease 187')
    parser.add_argument('--fast-clear', action='store_true',
                        help='use the experimental unrolled staging clear')
    parser.add_argument('--approved-music', action='store_true',
                        help='use the exact stereo soundtrack from release 133')
    parser.add_argument('--earlier-percussion', action='store_true',
                        help='use the hall snare, training swell and bass drop in the release 133 mix')
    parser.add_argument('--release-122-music', action='store_true',
                        help='use release 122 music with the opening kick muted')
    args = parser.parse_args()
    if args.earlier_percussion and not args.approved_music:
        parser.error('--earlier-percussion requires --approved-music')
    source = args.source.read_bytes()
    if args.approved_music:
        source = with_approved_music(source, earlier_percussion=args.earlier_percussion,
                                     release_122=args.release_122_music)
    result = build(source, fast_clear=args.fast_clear)
    if args.animated_loading or args.full_rate_loading:
        from animated_loading import install
        result = install(result, full_rate=args.full_rate_loading)
    if args.runad_handoff:
        result = with_runad_handoff(result)
    if args.replace_dev:
        require(args.output.resolve() == ROOT / 'build/hardware-dev.xex',
                '--replace-dev is restricted to build/hardware-dev.xex')
    with args.output.open('wb' if args.replace_dev else 'xb') as stream:
        stream.write(result)
    print(f'{args.output}: {len(result)} B; SHA-256 {hashlib.sha256(result).hexdigest()}')
