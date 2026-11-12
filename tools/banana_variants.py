"""Dense full-turn banana motifs with page-bounded RLE playback.

Independent input/output cursors avoid per-packet 16-bit pointer updates.
Only the inactive framebuffer is written; music NMI needs no shared scratch.
"""
from functools import lru_cache
from build_sequence import Code
from music_timing import tick_at_bar
ENTRY=0x7c00
KEY,CACHE=0x0ddd,0x0dde
FRAMES=32

def variant_at(tick):
    from post_trevor_director import MONTAGE_START, SHIFT, END
    clock=tick+SHIFT if MONTAGE_START<=tick<END else tick
    if tick_at_bar(88)<=clock<tick_at_bar(96):return 0
    return (clock>>11)&1

@lru_cache(maxsize=1)
def peeled_tile():
    """Single pale fruit with three recognisable folded-back yellow peels."""
    tile=bytearray([2]*4096)
    def inside(x,y,poly):
        hit=False
        for (ax,ay),(bx,by) in zip(poly,poly[1:]+poly[:1]):
            if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax:hit=not hit
        return hit
    def shape(poly,ink,shade=False):
        mask={(x,y) for y in range(64) for x in range(64) if inside(x+.5,y+.5,poly)}
        for x,y in mask:
            edge=any((x+dx,y+dy) not in mask for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
            shadow=shade and (x+2,y) not in mask
            tile[y*64+x]=0 if edge else 1 if shadow else ink
    # Curved exposed upper half and the still-covered lower half.
    shape(((37,5),(42,4),(46,9),(47,16),(45,24),(41,32),(35,39),
           (29,43),(25,42),(27,35),(32,28),(35,20),(36,12)),3,True)
    shape(((29,31),(39,29),(40,37),(36,47),(30,55),(23,59),
           (18,57),(21,49),(25,41)),1)
    # Three separate curling flaps, folded down from the same split.
    shape(((30,30),(23,28),(16,31),(10,34),(5,31),(8,38),
           (15,42),(23,40),(31,34)),1)
    shape(((35,29),(41,27),(47,30),(51,35),(57,38),(59,35),
           (58,44),(52,47),(47,44),(42,37),(36,35)),1)
    shape(((31,30),(35,31),(34,37),(28,46),(25,52),(27,56),
           (23,55),(20,49),(23,41),(27,34)),1)
    # Pale inner peel ridges; black outlines separate them from the flesh.
    for poly in (((13,35),(22,31),(26,32),(20,36),(15,38)),
                 ((41,30),(45,32),(50,39),(54,41),(51,42),(46,38)),
                 ((29,35),(32,34),(29,41),(24,49),(24,45))):
        for y in range(64):
            for x in range(64):
                if inside(x+.5,y+.5,poly):tile[y*64+x]=3
    return bytes(tile)


def packed(frame,variant):
    import mosaic
    p=mosaic.pixels(frame,variant)
    return bytes(sum(p[i+k]<<(6-2*k) for k in range(4)) for i in range(0,len(p),4))


VARIANT_ENTRY=0xebf0
EYE_MAP_ENTRY=0xec04
SELECT_ENTRY=0xed4d

def selector_inserts():
    from engine_effects import DL_KEYS
    import terminal_typing,post_trevor_director
    assert terminal_typing.ENTRY+len(terminal_typing.helper().finish())<=VARIANT_ENTRY
    assert post_trevor_director.ENTRY+len(post_trevor_director.helper())<=SELECT_ENTRY
    c=Code(VARIANT_ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0xad,0xd301);c.emit(0x48);a(0xad,0x24b5);a(0x8d,0xd301)
    a(0x20,0x7400);c.emit(0xaa,0x68);a(0x8d,0xd301);c.emit(0x8a,0x60)
    variant=bytes(c.finish());assert VARIANT_ENTRY+len(variant)<=EYE_MAP_ENTRY
    c=Code(EYE_MAP_ENTRY)
    a(0xad,0xd301);c.emit(0x48);a(0xad,0x24b5);a(0x8d,0xd301)
    a(0x20,0x7500);c.emit(0x68);a(0x8d,0xd301);a(0xad,0x83ed);c.emit(0x60)
    eye_map=bytes(c.finish());assert EYE_MAP_ENTRY+len(eye_map)<=0xec20
    c=Code(SELECT_ENTRY)
    a(0x20,EYE_MAP_ENTRY);c.emit(0xc9,32);c.branch(0x90,'banana');c.emit(0x4a,0x4a,0xaa,0x60)
    c.label('banana');a(0x20,VARIANT_ENTRY);a(0x8d,KEY)
    a(0xad,0x83fa);c.emit(0xc9,255);c.branch(0xf0,'layout');c.emit(0xa9,255);a(0x8d,CACHE)
    c.label('layout');a(0xad,0x83e6);c.emit(0x29,4,0x4a,0x4a,0x49,1,0xaa);a(0xbd,DL_KEYS);c.emit(0xc9,1);c.branch(0xf0,'index');c.emit(0xa9,255);a(0x8d,CACHE)
    c.label('index');a(0xad,0x83ed);c.emit(0x4a,0x4a,0xaa)
    from banana_cache import FLAG, SELECT
    a(0xad,FLAG);c.branch(0xf0,'selected');c.emit(0xc9,2);c.branch(0xf0,'raw')
    a(0x20,SELECT);c.emit(0x60)
    c.label('raw');c.emit(0x8a);a(0x2c,KEY);c.branch(0x50,'selected');c.emit(0x18,0x69,37,0xaa)
    c.label('selected');c.emit(0x60)
    select=bytes(c.finish());assert SELECT_ENTRY+len(select)<=0xeda0
    return [(VARIANT_ENTRY,variant),(EYE_MAP_ENTRY,eye_map),(SELECT_ENTRY,select)]



HELPER=0x7840
COPY=0x7c80
DECODER=0x7d00
POINTERS=0x7f80
SRC,COUNT,STEP=0x0dc0,0x0dc4,0x0dc5
CAPACITY=HELPER-0x4000

def encode(raw,threshold=4,offset=0):
    """No packet crosses either an input or an output 256-byte page."""
    out=bytearray();i=0
    while i<3840:
        source=(offset+len(out))%256
        if source>253:
            out.extend(bytes(256-source));continue
        end=min(3840,(i//256+1)*256);j=i+1
        while j<end and raw[j]==raw[i] and j-i<127:j+=1
        if j-i>=threshold:
            out.extend((128+j-i,raw[i]));i=j
        else:
            start=i;i+=1;limit=min(end,start+127,start+255-source)
            while i<limit:
                if raw[i:i+threshold]==raw[i:i+1]*threshold:break
                i+=1
            out.append(i-start);out.extend(raw[start:i])
    return bytes(out)

def estimated_cost(data,offset=0):
    i=0;cost=0
    while i<len(data):
        count=data[i];i+=1
        if count==0:
            i+=255-(offset+i-1)%256
        elif count<128:
            cost+=52+15.5*count;i+=count
        else:
            cost+=73+7.625*(count&127);i+=1
    return cost

@lru_cache(maxsize=8)
def streams(index):
    raw=[packed(index*4+i,v) for v in range(2) for i in range(4)]
    candidates=[]
    for r in raw:
        candidates.append([(estimated_cost(d),len(d),t)
                           for t in range(3,25) if (d:=encode(r,t,0))])
    # Minimise the most expensive frame, spending only this bank's own space.
    for limit in sorted({cost for cs in candidates for cost,size,t in cs}):
        choices=[]
        for cs in candidates:
            eligible=[(size,cost,t) for cost,size,t in cs if cost<=limit]
            if not eligible:break
            choices.append(min(eligible)[2])
        if len(choices)!=8:continue
        ss=[];offset=0
        for r,threshold in zip(raw,choices):
            data=encode(r,threshold,offset);ss.append(data);offset+=len(data)
        if offset<=CAPACITY:return ss
    raise ValueError(f'banana bank {index} does not fit')

def decoder():
    # Y walks a source page, X walks a destination page. The encoder splits
    # packets at both boundaries, so inner loops need no 16-bit pointer maths.
    # Source padding uses token 0; completion is exactly fifteen output pages.
    c=Code(DECODER)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0xad,SRC+1)
    for label in ('control','value','lit0','lit1'):c.jump(0x8d,label+'_hi')
    a(0xac,SRC);a(0xad,0x83fe)
    for label in ('store0','store1',*[f'fill{i}' for i in range(8)]):c.jump(0x8d,label+'_hi')
    c.emit(0xa9,15);a(0x8d,COUNT);c.emit(0xa2,0)
    c.label('packet');c.label('control');c.emit(0xb9,0,0x40)
    c.branch(0xd0,'nonzero');c.jump(0x4c,'source_page')
    c.label('nonzero');c.branch(0x30,'run');c.emit(0xc8)
    # Count and end index; preserve parity across the source load.
    c.emit(0x48);a(0x8e,STEP);c.emit(0x18);a(0x6d,STEP);c.jump(0x8d,'lit_end_lo');c.emit(0x68,0x4a);c.branch(0xb0,'lit1')
    c.label('lit0');c.emit(0xb9,0,0x40);c.label('store0');c.emit(0x9d,0,0x90,0xc8,0xe8)
    c.label('lit1');c.emit(0xb9,0,0x40);c.label('store1');c.emit(0x9d,0,0x90,0xc8,0xe8)
    c.label('lit_end');c.emit(0xe0,0);c.branch(0xd0,'lit0');c.jump(0x4c,'packet_done')
    c.label('run');c.emit(0xc8,0x29,127);a(0x8c,STEP+1);c.emit(0xa8)
    a(0x8e,STEP);c.emit(0x18);a(0x6d,STEP);c.jump(0x8d,'fill_end_lo')
    a(0xb9,0x7f00);c.jump(0x8d,'fill_jump_lo');a(0xac,STEP+1)
    c.label('value');c.emit(0xb9,0,0x40,0xc8)
    c.label('fill_jump');c.emit(0x4c,0,0x7e)
    assert c.origin+len(c.data)<=0x7e00
    c.emit(*bytes(0x7e00-c.origin-len(c.data)))
    for i in range(8):
        c.label(f'fill{i}');c.emit(0x9d,0,0x90,0xe8)
    c.label('fill_end');c.emit(0xe0,0);c.branch(0xd0,'fill0')
    c.label('packet_done');c.emit(0xe0,0);c.branch(0xd0,'source_check')
    a(0xce,COUNT);c.branch(0xd0,'dest_page');c.emit(0x60)
    c.label('dest_page')
    for label in ('store0','store1',*[f'fill{i}' for i in range(8)]):c.jump(0xee,label+'_hi')
    c.label('source_check');c.emit(0xc0,0);c.branch(0xf0,'source_page');c.jump(0x4c,'packet')
    c.label('source_page');c.emit(0xa0,0)
    for label in ('control','value','lit0','lit1'):c.jump(0xee,label+'_hi')
    c.jump(0x4c,'packet')
    for label in ('control','value','lit0','lit1','store0','store1',*[f'fill{i}' for i in range(8)]):
        c.labels[label+'_hi']=c.labels[label]+2
    c.labels['lit_end_lo']=c.labels['lit_end']+1;c.labels['fill_end_lo']=c.labels['fill_end']+1
    c.labels['fill_jump_lo']=c.labels['fill_jump']+1
    assert c.origin+len(c.data)<=0x7f00
    c.emit(*bytes(0x7f00-c.origin-len(c.data)))
    c.emit(*(c.labels[f'fill{(-i)&7}']&255 for i in range(128)))
    code=c.finish();assert DECODER+len(code)<=POINTERS,len(code)
    return bytes(code)

def entry_helpers():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0x20,HELPER);a(0x2c,KEY);c.branch(0x50,'classic')
    c.emit(0xa9,0xee);a(0x8d,0xd018);c.emit(0xa9,0xea);a(0x8d,0xd016)
    c.label('classic');c.emit(0xa9,255);a(0x8d,0x83fa);c.emit(0x60)
    entry=bytes(c.finish())
    c=Code(COPY)
    a(0xad,0x83ed);c.emit(0x29,3);a(0x2c,KEY);c.branch(0x50,'index');c.emit(0x09,4)
    c.label('index');c.emit(0xaa);a(0xbd,POINTERS);a(0x8d,SRC);a(0xbd,POINTERS+8);a(0x8d,SRC+1);c.emit(0x4c,DECODER&255,DECODER>>8)
    return entry,bytes(c.finish())

def bank(index):
    import mosaic
    out=bytearray(16384);pos=0x4000
    for i,data in enumerate(streams(index)):
        out[pos-0x4000:pos-0x4000+len(data)]=data
        out[POINTERS-0x4000+i]=pos&255;out[POINTERS-0x4000+8+i]=pos>>8;pos+=len(data)
    code=mosaic.helper(HELPER,copy_entry=COPY,cache_key=KEY,banana_only=True,cache_address=CACHE)
    out[HELPER-0x4000:HELPER-0x4000+len(code)]=code
    for address,code in zip((ENTRY,COPY),entry_helpers()):
        out[address-0x4000:address-0x4000+len(code)]=code
    code=decoder();out[DECODER-0x4000:DECODER-0x4000+len(code)]=code
    return bytes(out)

def memory_report():
    import mosaic
    sizes=[sum(map(len,streams(i))) for i in range(8)]
    code=len(mosaic.helper(HELPER,copy_entry=COPY,cache_key=KEY,banana_only=True,cache_address=CACHE))+sum(map(len,entry_helpers()))+len(decoder())+16
    return dict(variants=2,frames_per_variant=32,banks=8,packed_bytes=sum(sizes),code_bytes_per_bank=code,free_bytes=8*(16384-code)-sum(sizes),payload_bytes_per_bank=sizes,raw_symmetry=False,
                runtime_raw_banks=16,reused_title_banks=list(range(40,49)),
                runtime_raw_bitmap_bytes=64*3840,runtime_raw_helper_bytes=16*981,
                runtime_raw_bank_free_bytes=16*(16384-15360-981),
                startup_packed_archive_only=True)
