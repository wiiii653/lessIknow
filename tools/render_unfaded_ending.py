"""Re-render v035 with its six-beat master fade disabled."""
import argparse
import json
from pathlib import Path
import sys
from types import ModuleType


def render(releases, unfaded):
    scores = {}
    stage_files = (
        ('018', 'party_master', 'min(1,max(0,(16-position)/6)) if kind==\'outro\' else 1'),
        ('023', 'fix_sync', 'max(0, min(1, (640 - beat) / 6))'),
        ('024', 'rebuild_second_half', None),
        ('025', 'warm_instruments', 'min(1, max(0, (640 - beat) / 6)) if kind == \'outro\' else 1'),
        ('026', 'hammond_lead', 'min(1, max(0, (640 - beat) / 6)) if beat >= 624 else 1'),
        ('027', 'delay_lead', None),
        ('028', 'sculpt_arrangement', None),
        ('029', 'weave_arps', None),
        ('031', 'motif_motion', None),
        ('033', 'repair_master', 'min(1,max(0,(640-i/rate*bpm/60)/6)) if block==39 else 1'),
        ('034', 'pluck_lead', None),
        ('035', 'bass_release', 'min(1,max(0,(640-beat)/6)) if beat>=624 else 1'),
    )

    def folder(version):
        return releases / ('v' + version)

    def metadata(version):
        return json.loads((folder(version) / 'manifest.json').read_text())

    def score(version):
        return scores[version]

    def reference(version):
        return (folder(version) / 'registers.bin').read_bytes()

    def replay_score(version):
        version = version.removeprefix('v')
        if version not in scores:
            raw = reference(version)
            scores[version] = [tuple(raw[i:i+18]) for i in range(0, len(raw), 18)]
        return scores[version], metadata(version), {'version': 'v' + version}

    for version, name, fade in stage_files:
        path = folder(version) / (name + '.py')
        # Each release snapshots its dependencies. Import from that snapshot.
        search_path = sys.path[:]
        imports = dict(sys.modules)
        for sibling in path.parent.glob('*.py'):
            sys.modules.pop(sibling.stem, None)
        sys.path.insert(0, str(path.parent))
        module = ModuleType(name)
        module.__file__ = str(path)
        source = path.read_text()
        if unfaded and fade:
            if source.count(fade) != 1:
                raise ValueError(f'Unexpected fade expression in {path}')
            source = source.replace(fade, '1.0')
        try:
            exec(compile(source, path, 'exec'), module.__dict__)
            if 'source_voice' in sys.modules:
                sys.modules['source_voice'].ROOT = releases.parent.parent
            module.release_score = replay_score
            if version in ('018', '023', '024'):
                frames = module.musical_frames()[0]
            elif version == '025':
                frames = module.instrument_frames(score('024'), metadata('024'))
            elif version == '026':
                frames = module.organ_frames(score('025'), metadata('025'))
            elif version == '027':
                frames, _ = module.delay_frames(score('026'), metadata('026'),
                                                metadata('027')['lead_entry']['cycle'])
            elif version == '028':
                frames, _ = module.concert_frames(score('027'), metadata('027'))
            elif version == '029':
                frames, _, roles, _ = module.weave_frames(score('028'), metadata('028'))
                scores['030'] = frames
            elif version == '031':
                frames, _, _, roles = module.motion_frames(score('030'), metadata('030'), roles)
            elif version == '033':
                frames, roles, _, _ = module.heavy_frames(score('031'), metadata('032'),
                                                           score('030'), score('027'),
                                                           metadata('018'), roles)
            elif version == '034':
                frames, _, _ = module.plucked_frames(score('033'), metadata('033'),
                                                     score('030'), roles)
            else:
                frames, _ = module.release_frames(score('034'), metadata('034'))
        finally:
            sys.path[:] = search_path
            for sibling in path.parent.glob('*.py'):
                name = sibling.stem
                sys.modules.pop(name, None)
                if name in imports:
                    sys.modules[name] = imports[name]
        scores[version] = frames
        if not unfaded and b''.join(map(bytes, frames)) != reference(version):
            raise ValueError(f'Render differs from archived v{version}')

    return b''.join(map(bytes, scores['035']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('releases', type=Path, help='impala-lessIknow/remix/releases')
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    releases = args.releases.resolve()
    baseline = render(releases, unfaded=False)
    unfaded = render(releases, unfaded=True)
    first = next(i for i, (old, new) in enumerate(zip(baseline, unfaded)) if old != new)
    if len(baseline) != len(unfaded) or first // 18 < 59268 or baseline[-144:] != unfaded[-144:]:
        raise ValueError('Unexpected change outside the final six beats')
    with args.output.open('xb') as output:
        output.write(unfaded[first // 18 * 18:])
    print(f'First changed update {first // 18}')
