"""Four additional solo inbetweens, packed in existing ribbon-bank tails.

Original poses/ticks remain authoritative. A small unbanked adapter selects
half-step frames, restores/updates hand anchors and routes a fast LZ copy.
"""
from functools import lru_cache
from build_sequence import Code

SELECT,COPY,PRIVATE=0x0d60,0x0db0,0x0dc0
BANK_ENTRY,DECODER=0x4040,0x5e00
SOURCE,VALUE,STEP,INDEX,ANCHORS=PRIVATE,PRIVATE+2,PRIVATE+3,PRIVATE+4,PRIVATE+8
PAIRS=((0,32),(1,32),(1,33),(3,33),(2,3),(2,32),
       (4,5),(5,34),(6,34),(6,7),(8,9),(9,35),(10,35),(8,10))
POSES=(0,1,2,3,4,5,0,1,6,4,7,0,8,4)
QUARTER_POSES=(0,1,2,3)
QUARTER_HANDS=(((.23,.12),(.22,.42)),((.18,.55),(.52,.48)),
               ((.22,.59),(.80,.24)),((.17,.24),(.87,.20)))
HANDS=(((.23,.337),(.34,.103)),((.164,.384),(.205,.457)),
       ((.166,.619),(.414,.645)),((.258,.547),(.703,.159)),
       ((.124,.258),(.804,.052)),((.166,.255),(.310,.335)),
       ((.234,.532),(.581,.302)),((.138,.248),(.763,.023)),
       ((.159,.248),(.347,.176)))


def step_midpoint(step):
    import ribbon_dance as d
    if step>=117 or 31<=step<=63:return None
    pair=tuple(sorted((d.frame_for_step(step),d.frame_for_step(step+1))))
    return PAIRS.index(pair) if pair in PAIRS else None


def midpoint_at(tick,step):
    import ribbon_dance as d
    mid=step_midpoint(step)
    return mid if mid is not None and tick>=(d.STEPS[step]+d.STEPS[step+1])//2 else None


def quarter_at(tick,step):
    import ribbon_dance as d
    mid=step_midpoint(step)
    if mid is None or not 6<=mid<10:return None
    quarter=(3*d.STEPS[step]+d.STEPS[step+1])//4
    # Match the shipped selector: it gates quarter selection on midpoint first.
    return mid if tick>=max(quarter,(d.STEPS[step]+d.STEPS[step+1])//2) else None


@lru_cache(maxsize=28)
def artwork(index):
    import ribbon_dance as d
    quarter=index>=14
    pair=index-8 if quarter else index
    p=d.gym(6<=pair<10);pose=QUARTER_POSES[index-14] if quarter else POSES[pair]
    sheet=3 if quarter else True
    if pair<6:
        left=d.actor(p,pose,32,57,.09,mid=sheet)
        right=d.actor(p,pose,128,57,.09,True,mid=sheet)
        hero=d.actor(p,pose,80,61,.125,mid=sheet)
        hands=[hero[0],hero[1],left[0],right[1]]
    elif pair<10:
        hero=d.actor(p,pose,80,67,.16,mid=sheet)
        hands=[hero[0],hero[1],hero[0],hero[1]]
    else:
        left=d.actor(p,pose,42,61,.10,mid=sheet)
        right=d.actor(p,pose,118,61,.10,True,mid=sheet)
        hero=d.actor(p,pose,80,55,.11,mid=sheet)
        hands=[hero[0],hero[1],left[0],right[1]]
    return bytes(p),hands


def packed(index):
    p=artwork(index)[0]
    return bytes(sum(p[i+k]<<(6-2*k) for k in range(4)) for i in range(0,len(p),4))


def compress(data):
    """Literal runs 128..255; matches 1..127 (length+2), LE distance; 0 end."""
    out=bytearray();literal=bytearray();seen={};i=0
    def flush():
        if literal:out.append(127+len(literal));out.extend(literal);literal.clear()
    while i<len(data):
        length=0;pos=0
        for previous in reversed(seen.get(data[i:i+3],[])):
            count=3
            while count<129 and i+count<len(data) and data[previous+count]==data[i+count]:count+=1
            if count>length:length,pos=count,previous
            if count==129:break
        # Tiny matches cost more CPU than a few extra literal bytes. Prefer
        # long runs: the half-step deadline matters more than minimum size.
        if length>=8:
            flush();out.extend((length-2,(i-pos)&255,(i-pos)>>8));end=i+length
        else:
            literal.append(data[i]);end=i+1
            if len(literal)==128:flush()
        while i<end:
            seen.setdefault(data[i:i+3],[]).append(i);i+=1
    flush();out.append(0)
    return bytes(out)


def decompress(data):
    out=bytearray();i=0
    while data[i]:
        cmd=data[i];i+=1
        if cmd&128:
            count=(cmd&127)+1;out.extend(data[i:i+count]);i+=count
        else:
            distance=data[i]|data[i+1]<<8;i+=2
            for _ in range(cmd+2):out.append(out[-distance])
    assert i==len(data)-1
    return bytes(out)


@lru_cache(maxsize=1)
def payloads():
    result=[];region=0;address=0x4600
    for index in range(14):
        data=compress(packed(index));assert decompress(data)==packed(index)
        if index<7:
            if address+len(data)>0x5e00 and region==0:region=1;address=0x6000
            assert address+len(data)<=(0x5e00 if region==0 else 0x7800)
            bank=2;source=address;address+=len(data)
        else:
            bank=32+index-7;source=0x4a00
            assert source+len(data)<=0x5400
        result.append((bank,source,data))
    # Keep streams in loader banks with an installed decoder. Four solo poses
    # fit beside the existing compressed frames in indices 32–35.
    for index in range(14,18):
        data=compress(packed(index));assert decompress(data)==packed(index)
        owner=32+index-14
        source=max(address+len(blob) for bank,address,blob in result if bank==owner)
        assert source+len(data)<=0x5400,(owner,hex(source),len(data))
        result.append((owner,source,data))
    return tuple(result)


def selector():
    import ribbon_dance as d
    c=Code(BANK_ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    c.emit(0xa9,0);a(0x8d,0x83e5)
    a(0xae,0x83ed)
    for plane in range(8):
        c.jump(0xbd,'original_meta'+str(plane));a(0x8d,ANCHORS+plane)
    a(0xae,STEP);c.emit(0xe0,64);c.branch(0xb0,'front');c.emit(0x60)
    c.label('front');c.emit(0x8a,0x38,0xe9,64,0xaa)
    c.jump(0xbd,'mid_ids');c.emit(0xc9,255);c.branch(0xd0,'check_time');c.emit(0x60)
    c.label('check_time');a(0xad,0x83e3);c.jump(0xdd,'mid_hi');c.branch(0x90,'original');c.branch(0xd0,'quarter_check')
    a(0xad,0x83e2);c.jump(0xdd,'mid_lo');c.branch(0xb0,'quarter_check')
    c.label('original');c.emit(0x60)
    c.label('quarter_check');a(0xad,0x83e3);c.jump(0xdd,'q3_hi');c.branch(0x90,'between');c.branch(0xd0,'quarter')
    a(0xad,0x83e2);c.jump(0xdd,'q3_lo');c.branch(0x90,'between')
    c.jump(0xbd,'mid_ids');c.emit(0xc9,6);c.branch(0x90,'between');c.emit(0xc9,10);c.branch(0xb0,'between')
    c.label('quarter');c.jump(0xbd,'mid_ids');c.emit(0xc9,6);c.branch(0x90,'between');c.emit(0xc9,10);c.branch(0xb0,'between')
    c.jump(0xbd,'mid_ids');c.emit(0x18,0x69,8);a(0x8d,INDEX);c.jump(0x4c,'asset')
    c.label('between');c.jump(0xbd,'mid_ids');a(0x8d,INDEX);c.jump(0x4c,'asset')
    c.label('asset');c.emit(0xaa,0xa9,128);a(0x8d,0x83e5)
    c.jump(0xbd,'banks');c.emit(0xa8,0xc0,2);c.branch(0xd0,'extra_bank')
    a(0xad,0x24b5);c.jump(0x4c,'bank_ready')
    c.label('extra_bank');a(0xb9,0x08c0)
    c.label('bank_ready');a(0x8d,VALUE)
    for name,target in (('sources_lo',SOURCE),('sources_hi',SOURCE+1)):
        c.jump(0xbd,name);a(0x8d,target)
    for plane in range(8):
        c.jump(0xbd,'mid_meta'+str(plane));a(0x8d,ANCHORS+plane)
    c.emit(0x60)
    master=d.metadata()
    for plane in range(8):c.label('original_meta'+str(plane));c.emit(*master[plane*36:(plane+1)*36])
    for plane in range(8):
        c.label('mid_meta'+str(plane))
        c.emit(*((max(0,min(255,artwork(i)[1][plane][0]+34)) if plane<4 else
                  ((artwork(i)[1][plane-4][1]*3+17)//2-32)&255) for i in range(18)))
    c.label('mid_ids');c.emit(*(255 if step_midpoint(step) is None else step_midpoint(step) for step in range(128)))
    times=[(d.STEPS[step]+d.STEPS[step+1])//2 if step<127 else 65535 for step in range(128)]
    c.label('mid_lo');c.emit(*(t&255 for t in times))
    c.label('mid_hi');c.emit(*(t>>8 for t in times))
    q3=[(3*d.STEPS[step]+d.STEPS[step+1])//4 if step<127 else 65535 for step in range(128)]
    c.label('q3_lo');c.emit(*(t&255 for t in q3))
    c.label('q3_hi');c.emit(*(t>>8 for t in q3))
    c.label('banks')
    c.emit(*(bank for bank,source,data in payloads()))
    for name,shift in (('sources_lo',0),('sources_hi',8)):
        c.label(name);c.emit(*((source>>shift)&255 for bank,source,data in payloads()))
    code=c.finish();assert BANK_ENTRY+len(code)<=0x4600
    return code


def decoder(origin=DECODER):
    c=Code(origin)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    for offset,name in ((0,'get_lo'),(1,'get_hi')):a(0xad,SOURCE+offset);c.jump(0x8d,name)
    c.emit(0xa9,0);c.jump(0x8d,'write_lo');a(0xad,0x83fe);c.jump(0x8d,'write_hi')
    c.label('command');c.jump(0x20,'get');c.branch(0xd0,'has_command');c.emit(0x60)
    c.label('has_command');c.branch(0x10,'match')
    c.emit(0x29,127,0x18,0x69,1,0xaa)
    for part in ('lo','hi'):c.jump(0xad,'get_'+part);c.jump(0x8d,'copy_'+part)
    c.emit(0x8a,0x18);c.jump(0x6d,'get_lo');c.jump(0x8d,'get_lo');c.branch(0x90,'run');c.jump(0xee,'get_hi');c.jump(0x4c,'run')
    c.label('match');c.emit(0x18,0x69,2,0xaa)
    c.jump(0x20,'get');c.jump(0x8d,'distance_lo');c.jump(0x20,'get');c.jump(0x8d,'distance_hi')
    c.emit(0x38);c.jump(0xad,'write_lo');c.label('subtract_lo');c.emit(0xe9,0);c.jump(0x8d,'copy_lo')
    c.jump(0xad,'write_hi');c.label('subtract_hi');c.emit(0xe9,0);c.jump(0x8d,'copy_hi')
    c.label('run');c.emit(0xa0,0)
    c.label('byte');c.label('copy');c.emit(0xb9,0,0)
    c.label('write');c.emit(0x99,0,0,0xc8,0xca);c.branch(0xd0,'byte')
    c.emit(0x98,0x18);c.jump(0x6d,'write_lo');c.jump(0x8d,'write_lo');c.branch(0x90,'next');c.jump(0xee,'write_hi')
    c.label('next');c.jump(0x4c,'command')
    c.label('get');c.label('input');c.emit(0xad,0,0)
    c.jump(0xee,'get_lo');c.branch(0xd0,'got');c.jump(0xee,'get_hi')
    c.label('got');c.emit(0x09,0,0x60)  # N/Z describe the byte, not pointer INC.
    for name in ('copy','write','input'):
        stem='get' if name=='input' else name
        c.labels[stem+'_lo']=c.labels[name]+1;c.labels[stem+'_hi']=c.labels[name]+2
    c.labels['distance_lo']=c.labels['subtract_lo']+1;c.labels['distance_hi']=c.labels['subtract_hi']+1
    code=c.finish();assert len(code)<=512
    return code


def install_runtime(runtime):
    import ribbon_dance as d
    c=Code(SELECT)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0x8e,STEP);a(0xad,0xd301);c.emit(0x48)
    a(0xad,0x24b5);a(0x8d,0xd301);a(0x20,BANK_ENTRY)
    c.emit(0x68);a(0x8d,0xd301);a(0xae,0x83ed)
    for plane in range(8):a(0xad,ANCHORS+plane);a(0x9d,d.META+plane*36)
    c.emit(0x60);assert c.origin+len(c.data)<=COPY
    c.emit(*bytes(COPY-c.origin-len(c.data)))
    a(0xad,VALUE);a(0x8d,0xd301);a(0x20,DECODER);c.emit(0x60)
    code=c.finish();assert SELECT+len(code)<=PRIVATE
    out=bytearray(runtime);offset=SELECT-0xc00
    assert not any(out[offset:offset+len(code)])
    out[offset:offset+len(code)]=code
    assert not any(out[PRIVATE-0xc00:PRIVATE-0xc00+16])
    return bytes(out)


def install(bank,index):
    parts=[]
    if index==2:parts.append((BANK_ENTRY,selector()))
    if index==2 or 32<=index<39:parts.append((DECODER,decoder()))
    parts.extend((source,data) for owner,source,data in payloads() if owner==index)
    out=bytearray(bank)
    for address,data in parts:
        offset=address-0x4000
        assert 0<=offset and offset+len(data)<=len(out)
        assert not any(out[offset:offset+len(data)]),(index,hex(address),len(data))
        out[offset:offset+len(data)]=data
    return bytes(out)
