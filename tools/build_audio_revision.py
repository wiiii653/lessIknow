"""Package an audited prototype with stereo headroom or a stable mono fold."""
import argparse
from collections import Counter
import hashlib
from pathlib import Path

from build_hardware_xex import build as hardware_xex
from build_visual_prototype import xex_segment
from extract_music import segments
from make_mono import mono

SOURCE_SHA256 = {
    '383739cfeb918b678d3a3e0482829639cfcc5ead7cade3519a6ae6326132a7f2',  # v356
    'c86324bfe9c1f5196033f8f47c410a21cbdc3c1f9a4fc6158dc4b7c8641210bc',  # v357
    '2d903732c216692ada760920b3e74233e8852b03d0822dad551c6b63a75023fc',  # v358
    'c71fcb42340362709f426d67b635e684904bc023e870c13c8b503815062b93a6',  # v359
    '9ba948ef56c068062fbdc1733b3005a475c6829cc4f38a500f57eed18c98847c',  # v360
    '97a5323148f6c9f3e1090f277585c0a10304767efcab911ac68901d8027a6c33',  # v361
    '907129567675fea5383e6f293ddcc9b5307ae98938c22239b5d41afe71e18324',  # v362
    'ea74113db2af5de513ca73d933465125f83455169653c55b7d6bdf9fca6d506f',  # v363
    '58f2062cb454f20bc305eae13c0d8efd9fb1ca988a4fc66a2f7ff98732683e79',  # v364
    'e185a7e2504b5a6275f1dbcf0363c1fb5f20fd63f79c44d80aa5fa9507ec4a9c',  # v365
    '8f22a492088af78beda307fd5b61ae4da30c929b70deb6494864b6aafeb96b1b',  # v366
    '8d5b1b2fc106069379bba0592e81f7f3f846e64b6b37d2c6a6e387fb5415971b',  # v367
    '6247d4e80a008a088c903e5d2a0d840210f2dc220ec13ee4f613432017b310c4',  # v368
    'cf5be1f29c50b55c1ee883d7111a4ba28f3b1b93b28de73c380093af2d4cbfc3',  # v369
    '4796e8d293b89a335d16b023c43f6c652cffc4fefa53fb4aa79720c066d7a3b6',  # v370
    'd30da9aea4827ff183b00de87d17c69fab65dc7b2d21ad9fa404601d618002f6',  # v371
    '8bc0e3a61fedc880777a2c38e0ebad571bed6dd64902401858825920d438ae50',  # v372
    'f7f10c71103ec362293cbca6ca83ec01ab547577a54e2af4f25f26a8edaefdc9',  # v373
    '5b4290adf0c71b95fce5cd2a25b500a51f8e5bcc69957787b9eb1322800bded8',  # v374
    '542f6f7da0a369313818bb26599bbd17c3d5de7962f1c2eecb5d0e9e7622be15',  # v375
    'a42b97cba41b85ff51a17128e4d66e2cf2d93e015304b40f224142c84bca0ad5',  # v376
    '5b6f416813a4512e360cb4b56f84cd232bd69729e86ae21dbd508eb48d2767ed',  # v377
    '5be3dc2edfda57fe7db42616254440a89fdebaa7f59a12a29ea11b1948921c77',  # v378
    '3c1b08b0a1c46132a1ef3dad50279bea66ec8c91efb34f8235fa2bbc414eea60',  # v379
    '5e8a5783015ad3b2c883bce7fee9cd92db7c9d07d113eab18b67192e933c144e',  # v380
    'db4e3a6e5f35a35ca0d55d1ebae4d6e3505ab5f138c289b12bf60a91d5db9826',  # v381
    'c35c784c2f97098a07e415dfe553caef7a70fbf26c0ec6a1c886d08e5c07deb7',  # v382
    '39c8e9f46e80d9a942c893ad4f9a5529f1c746517423414a234339709c89efe0',  # v383
    'a36d93a7df44a11ddd51690eb82d483473e821ae3e56208913ac48753a4861f1',  # v384
    '51e3f72dafc22386719e4aaaef60059675ac3c063da72b8c2c57f31a2ee021c9',  # v385
    '4aecdc0876a85e1d48109ce989cebc8bb6bdb3b5e6e3b9884875a6450716229e',  # v386
    '435b801c9f8c1b3310c92b89c936d07526522153216f80452ca0c6fcf893e746',  # v388
    '60f568d7310490ff45d89bbc1c704fb7ae56af01cd10d2234b2f67b6dff8fefc',  # v389
    'a121a69aa27ee65c3f2305ed5b339f6ed21497daa3b30a163a33d8c5d3d6b442',  # v390
}
DICTIONARY = (0x2e00, 0x2e80, 0x2f00)
BANK_SIZE = 0x4000
MUSIC_END = 7 * BANK_SIZE + 0x0b10
VOLUME_BUDGET = 24
PAL_UPDATES_PER_SECOND = 4 * 1773447 / 35568
UNFADED_ENDING = Path(__file__).resolve().parents[1] / 'assets/music/v035-unfaded-ending.bin'
UNFADED_START = 59277
UNFADED_SHA256 = '4124771af6fd710e34f0efb702e301097e314400b740dcab5a165dec81cc5985'


def restore_ending_gain(packets):
    """Undo the six-beat master fade where v035 retained audible volume."""
    controls = (1, 3, 5, 7, 10, 12, 14, 16)
    peaks = dict.fromkeys(controls, 0)
    for tick, packet in enumerate(packets):
        beats_left = 640 - tick * (128 / 60) / PAL_UPDATES_PER_SECOND
        if beats_left >= 6:
            if beats_left < 10:
                for reg in controls:
                    peaks[reg] = max(peaks[reg], packet[reg] & 15)
            yield packet
            continue
        gain = max(1 / 15, beats_left / 6)
        restored = bytearray(packet)
        for reg in controls:
            volume = packet[reg] & 15
            # Limit quantization spikes to the voice's pre-fade peak.
            restored[reg] = (packet[reg] & 0xf0) | min(max(volume, peaks[reg]),
                                                      round(volume / gain))
        yield bytes(restored)


def decode(stream, dictionary):
    state = bytearray(18)
    packets, pos = [], 0
    while pos < len(stream):
        token = stream[pos]
        pos += 1
        if token == 255:
            return packets
        if token >= 128:
            packets.extend([bytes(state)] * ((token & 127) + 1))
            continue
        if token == 127:
            mask = int.from_bytes(stream[pos:pos+3], 'little')
            pos += 3
        else:
            mask = dictionary[token]
        if mask >= 1 << 18:
            raise ValueError('invalid register mask')
        for reg in range(18):
            if mask & (1 << reg):
                state[reg] = stream[pos]
                pos += 1
        packets.append(bytes(state))
    raise ValueError('no end marker in music staging area')


def encode(packets):
    masks, previous = [], None
    for packet in packets:
        masks.append(sum(1 << i for i, value in enumerate(packet)
                         if previous is None or value != previous[i]))
        previous = packet
    dictionary = [mask for mask, _ in Counter(m for m in masks if m).most_common(127)]
    indices = {mask: index for index, mask in enumerate(dictionary)}
    stream = bytearray()
    pos = 0
    while pos < len(packets):
        mask = masks[pos]
        if not mask:
            end = pos + 1
            while end < min(len(masks), pos + 127) and not masks[end]:
                end += 1
            stream.append(128 | (end - pos - 1))
            pos = end
            continue
        index = indices.get(mask, 127)
        stream.append(index)
        if index == 127:
            stream.extend(mask.to_bytes(3, 'little'))
        stream.extend(value for i, value in enumerate(packets[pos]) if mask & (1 << i))
        pos += 1
    stream.append(255)
    dictionary.extend([0] * (127 - len(dictionary)))
    if decode(stream, dictionary) != packets:
        raise ValueError('register stream round trip failed')
    return bytes(stream), dictionary


def limit(packet, chip):
    # Only attenuate simultaneous peaks. Keep each voice's mode and pitch.
    controls = tuple(chip + i for i in (3, 5, 7))
    levels = [packet[i] & 15 for i in controls]
    for _ in range(sum(levels) - VOLUME_BUDGET):
        loudest = max(range(len(levels)), key=levels.__getitem__)
        levels[loudest] -= 1
    for i, level in zip(controls, levels):
        packet[i] = (packet[i] & 0xf0) | level


def mix(packets, single_pokey):
    drum_owner = 0
    previous_drums = (False, False)
    for source in packets:
        packet = bytearray(source)
        if single_pokey:
            drum_levels = (source[5] & 15, source[14] & 15)
            active = tuple(level > 0 for level in drum_levels)
            other = 1 - drum_owner
            # Hold a hit through its envelope. A newly audible competing hit
            # may take over when it is louder than the current hit.
            if active[other] and (not active[drum_owner] or
                                 (not previous_drums[other] and
                                  drum_levels[other] > drum_levels[drum_owner])):
                drum_owner = other
            offset = drum_owner * 9
            packet[4:6] = source[4+offset:6+offset]
            previous_drums = active

            # The left side is the melody. Use the right accompaniment when
            # that voice has space, without letting a volume crossover jump octaves.
            if not source[7] & 15:
                packet[6:8] = source[15:17]
            level = ((source[3] & 15) + (source[12] & 15) + 1) // 2
            packet[3] = (source[3] & 0xf0) | level
            packet[9:] = bytes(9)
            # Reuse unwritten right-side controls for the original visual meters.
            for i in (3, 5, 7):
                packet[i+9] = source[i]
        else:
            packet[9], packet[11] = packet[0], packet[2]
            limit(packet, 9)
        limit(packet, 0)
        yield bytes(packet)


def introduce_theme_during_training(packets):
    """Preview the four-bar dance lead while the training groove continues."""
    from music_timing import tick_at_bar

    lead_registers = (6, 7, 15, 16)
    for bar in range(16, 24):
        phrase_bar = 24 + (bar - 16) % 4
        source = tick_at_bar(phrase_bar)
        last = tick_at_bar(phrase_bar + 1) - 1
        start = tick_at_bar(bar)
        for tick in range(start, tick_at_bar(bar + 1)):
            lead = packets[min(source + tick - start, last)]
            packet = bytearray(packets[tick])
            for register in lead_registers:
                packet[register] = lead[register]
            packets[tick] = bytes(packet)


def fade_in_dance_drums(packets, *, during_training=False):
    """Raise the left and right drum levels on alternating beats."""
    from build_sequence import DANCE_TICK
    from music_timing import tick_at_beat

    controls = (5, 14)
    dance_beat = 24 * 4
    assert tick_at_beat(dance_beat) == DANCE_TICK
    first_beat = dance_beat - 8 if during_training else dance_beat
    # Reserve the last gain step on both channels for the dance cut.
    full_gain = 5 if during_training else 4
    levels = [0, 0]
    intervals = [(0, tick_at_beat(first_beat), tuple(levels))]
    for beat in range(8):
        levels[beat % 2] += 1
        intervals.append((tick_at_beat(first_beat + beat),
                          tick_at_beat(first_beat + beat + 1), tuple(levels)))
    for start, end, gains in intervals:
        for tick in range(start, end):
            packet = bytearray(packets[tick])
            for control, gain in zip(controls, gains):
                volume = packet[control] & 15
                packet[control] = (packet[control] & 0xf0) | ((volume * gain + full_gain // 2) // full_gain)
            packets[tick] = bytes(packet)


def swell_training_drums(packets):
    """Ease in the drums, leaving the last gain jump for the dance cut."""
    from build_sequence import DANCE_TICK
    from music_timing import tick_at_bar

    start = tick_at_bar(22)
    duration = DANCE_TICK - start
    for tick in range(DANCE_TICK):
        progress = max(0, tick - start) / duration
        gain = .65 * progress ** 2
        packet = bytearray(packets[tick])
        for control in (5, 14):
            volume = packet[control] & 15
            packet[control] = (packet[control] & 0xf0) | round(volume * gain)
        packets[tick] = bytes(packet)


def training_build_and_drop(packets, source):
    """Start the snares at the hall and build into the dancer's bass hit."""
    from build_sequence import DANCE_TICK
    from gym_practice import PRACTICE_TICK
    from music_timing import tick_at_bar
    from school_story import WHISTLE_END

    # Use a dry training backbeat at the hall to avoid the source riser there.
    dry_backbeat = tick_at_bar(17)
    for tick in range(WHISTLE_END, PRACTICE_TICK):
        snare = source[dry_backbeat + tick - WHISTLE_END]
        if snare[13] in (10, 25, 41):
            raise_right_percussion(packets, tick, snare, .20)

    for tick in range(PRACTICE_TICK, DANCE_TICK):
        progress = (tick - PRACTICE_TICK) / (DANCE_TICK - PRACTICE_TICK)
        raise_right_percussion(packets, tick, source[tick], .15 + .43 * progress**2)

    # The dancer's first visible pixels fall closest to the second POKEY
    # update of the frame that displays her first pose.
    attack_tick = DANCE_TICK - 2
    first_bass = packets[DANCE_TICK]
    kick_end = next(tick for tick in range(DANCE_TICK+1, DANCE_TICK+96)
                    if not packets[tick][5] & 15)
    lead = DANCE_TICK - attack_tick
    opening_kick = [packet[4:6] for packet in packets[DANCE_TICK:kick_end+lead]]
    bass_tail = (15, 15, 15, 15, 15, 15, 15, 15, 14, 14, 13, 13,
                 12, 12, 11, 11, 10, 10, 10, 10)
    for elapsed, tick in enumerate(range(attack_tick, kick_end)):
        packet = bytearray(packets[tick])
        packet[4:6] = opening_kick[elapsed]
        if elapsed < len(bass_tail):
            for offset in (0, 9):
                pitch, control = offset + 2, offset + 3
                if tick < DANCE_TICK:
                    packet[pitch] = first_bass[pitch]
                volume = max(packet[control] & 15, bass_tail[elapsed])
                packet[control] = (first_bass[control] & 0xf0) | volume
                room = VOLUME_BUDGET - volume
                for voice in (5, 7):
                    register = offset + voice
                    level = min(room, packet[register] & 15)
                    packet[register] = (packet[register] & 0xf0) | level
                    room -= level
        packets[tick] = bytes(packet)


def raise_right_percussion(packets, tick, source, gain):
    packet = bytearray(packets[tick])
    room = max(0, VOLUME_BUDGET - (packet[12] & 15) - (packet[16] & 15))
    volume = min(room, int((source[14] & 15) * gain + .5))
    if volume > (packet[14] & 15):
        packet[13] = source[13]
        packet[14] = (source[14] & 0xf0) | volume
        packets[tick] = bytes(packet)


def music_packets(data):
    """Read v035 register updates from a raw prototype."""
    entries = list(segments(data))
    tables = [next(p for a, _, p in entries if a == address) for address in DICTIONARY]
    dictionary = [lo | mi << 8 | hi << 16 for lo, mi, hi in zip(*tables)]
    banks = [p for a, b, p in entries if (a, b) == (0x8000, 0xbfff)][:8]
    return decode(b''.join(banks)[:MUSIC_END], dictionary)


def build(data, single_pokey, *, fast_clear=False, no_ending_fade=False, unfaded_ending=False, drums_at_dance=False, fade_dance_drums=False, build_drums_during_training=False, early_theme=False, training_drum_swell=False):
    if hashlib.sha256(data).hexdigest() not in SOURCE_SHA256:
        raise ValueError('requires an audited raw v356–v390 prototype')
    entries = list(segments(data))
    banks = [i for i,(a,b,_) in enumerate(entries) if (a,b)==(0x8000,0xbfff)][:8]
    packets = music_packets(data)
    if len(packets) != 59833:
        raise ValueError('unexpected number of source music updates')
    if unfaded_ending:
        ending = UNFADED_ENDING.read_bytes()
        if (len(ending) != (len(packets) - UNFADED_START) * 18 or
                hashlib.sha256(ending).hexdigest() != UNFADED_SHA256):
            raise ValueError('unfaded ending does not match the audited render')
        packets[UNFADED_START:] = [ending[i:i+18] for i in range(0, len(ending), 18)]
    elif no_ending_fade:
        packets = restore_ending_gain(packets)
    if early_theme:
        introduce_theme_during_training(packets)
    mixed = list(mix(packets, single_pokey))
    if training_drum_swell:
        swell_training_drums(mixed)
    elif fade_dance_drums or build_drums_during_training:
        fade_in_dance_drums(mixed, during_training=build_drums_during_training)
    elif drums_at_dance:
        from build_sequence import DANCE_TICK

        # Gate channel 3 on each POKEY. Keep the original packet count,
        # pitches and control modes so the beat returns on the dance cue.
        for tick in range(DANCE_TICK):
            packet = bytearray(mixed[tick])
            for control in (5, 14):
                packet[control] &= 0xf0
            mixed[tick] = bytes(packet)
    stream, dictionary = encode(mixed)
    if len(stream) > MUSIC_END:
        raise ValueError(f'{len(stream)} music bytes exceed the existing {MUSIC_END}-byte allocation')
    padded = stream.ljust(MUSIC_END, b'\xff')
    bank_ordinals = {index: i for i,index in enumerate(banks)}
    out = bytearray(b'\xff\xff')
    for index,(a,b,payload) in enumerate(entries):
        if index in bank_ordinals:
            offset = bank_ordinals[index] * BANK_SIZE
            patch = padded[offset:offset+BANK_SIZE]
            payload = patch + payload[len(patch):]
        elif a in DICTIONARY:
            shift = DICTIONARY.index(a) * 8
            payload = bytes((mask >> shift) & 255 for mask in dictionary)
        out.extend(xex_segment(a, payload))
    if single_pokey:
        # Remove all second-chip writes, including the startup and mute paths.
        blocks = segments(mono(bytes(out)))
        out = bytearray(b'\xff\xff')
        for a,b,payload in blocks:
            if (a,b)==(0x2c00,0x2c80):
                # First chip's stores plus the existing visual meters and tick.
                writer = bytearray(payload[:0x36] + payload[0x6c:])
                for i, reg in enumerate((3, 5, 7)):
                    writer[0x37+i*6] = reg + 9
                payload = writer.ljust(len(payload), b'\xea')
            out.extend(xex_segment(a,payload))
    return hardware_xex(bytes(out), fast_clear=fast_clear), len(stream)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--mono', action='store_true')
    fade = parser.add_mutually_exclusive_group()
    fade.add_argument('--no-ending-fade', action='store_true',
                      help='reproduce stereo 114 using gain compensation')
    fade.add_argument('--unfaded-ending', action='store_true',
                      help='use the final patterns re-rendered from the source arrangement')
    parser.add_argument('--fast-clear', action='store_true',
                        help='use the experimental unrolled staging clear')
    drums = parser.add_mutually_exclusive_group()
    drums.add_argument('--build-drums-during-training', action='store_true',
                       help='raise alternate drum channels in bars 22–23 and restore both at bar 24')
    drums.add_argument('--training-drum-swell', action='store_true',
                       help='swell the drums into the original dance entrance')
    drums.add_argument('--fade-dance-drums', action='store_true',
                       help='raise alternating drum channels over the first two dance bars')
    drums.add_argument('--drums-at-dance', action='store_true',
                        help='mute the drum channels before the first dance shot')
    parser.add_argument('--early-theme', action='store_true',
                        help='introduce the dance lead at the training entrance')
    args = parser.parse_args()
    result, size = build(args.source.read_bytes(), args.mono, fast_clear=args.fast_clear,
                         no_ending_fade=args.no_ending_fade, unfaded_ending=args.unfaded_ending, drums_at_dance=args.drums_at_dance,
                         fade_dance_drums=args.fade_dance_drums,
                         build_drums_during_training=args.build_drums_during_training,
                         early_theme=args.early_theme, training_drum_swell=args.training_drum_swell)
    with args.output.open('xb') as output:
        output.write(result)
    print(f'{args.output}: {len(result)} B; compressed music {size} B; '
          f'SHA-256 {hashlib.sha256(result).hexdigest()}')
