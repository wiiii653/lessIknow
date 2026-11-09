"""Stage compressed finale resources in audited unbanked player gaps."""
from functools import lru_cache
from build_sequence import Code
from ribbon_inbetweens import decoder,SOURCE
import outro_text
ENTRY=0x3e58
FLAG=0x0dd7
GAPS=((0x28bd,0x2900),(0x2940,0x2a00),(0x2a65,0x2c00),
      (0x2c81,0x2e00),(0x2f7f,0x3000),
      (0x307f,0x3100),(0x3135,0x3180),(0x31a4,0x31f0),(0x31f1,0x3300),(0x3fce,0x4000),
      (0x23ce,0x2451))  # retired UI; terminal timing now loads with the font

def pack(data):
    # Optimal literal/match parsing using the existing 6502 LZ format.
    n=len(data);seen={};matches=[]
    for i in range(n):
        best=0;distance=0
        for previous in reversed(seen.get(data[i:i+3],[])):
            length=0
            while length<129 and i+length<n and data[previous+length]==data[i+length]:length+=1
            if length>best:best=length;distance=i-previous
            if best==129:break
        matches.append((best,distance));seen.setdefault(data[i:i+3],[]).append(i)
    cost=[0]*(n+1);choice=[None]*n
    for i in range(n-1,-1,-1):
        options=[(1+k+cost[i+k],k,0) for k in range(1,min(128,n-i)+1)]
        length,distance=matches[i]
        options += [(3+cost[i+k],k,distance) for k in range(3,length+1)]
        cost[i],length,distance=min(options)
        choice[i]=(length,distance)
    out=bytearray();i=0
    while i<n:
        length,distance=choice[i]
        if distance:out.extend((length-2,distance&255,distance>>8))
        else:out.append(127+length);out.extend(data[i:i+length])
        i+=length
    return bytes(out)+b"\0"


@lru_cache(maxsize=1)
def resources():
    raw=bytearray(0xf00)
    for address,data in outro_text.inserts():
        assert 0xc000<=address and address+len(data)<=0xcf00
        raw[address-0xc000:address-0xc000+len(data)]=data
    packed=pack(bytes(raw))
    chunks=[];offset=0
    for lo,hi in GAPS:
        while lo<hi and offset<len(packed):
            n=min(255,hi-lo,len(packed)-offset)
            chunks.append((lo,packed[offset:offset+n],0xb000+offset))
            lo+=n;offset+=n
    if offset!=len(packed):raise ValueError(f'outro staging exceeds gaps: {len(packed)} > {offset}')
    return bytes(raw),packed,chunks


def bootstrap():
    _,_,chunks=resources()
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0xad,FLAG);c.branch(0xf0,'load');a(0x4c,outro_text.ENTRY)
    c.label('load')
    for i,(src,data,dst) in enumerate(chunks):
        c.emit(0xa2,len(data));c.label(f'chunk{i}')
        a(0xbd,src-1);a(0x9d,dst-1);c.emit(0xca);c.branch(0xd0,f'chunk{i}')
    # Save original final-shot DLIST before converting the top band to text.
    a(0xad,0x83e6);c.emit(0x18)
    for page in range(3):
        c.jump(0x8d,f'save{page}_hi')
        if page<2:c.emit(0x69,1)
    c.emit(0xa2,0);c.label('save')
    for page in range(3):
        c.label(f'save{page}');a(0xbd,0x8000+page*256);a(0x9d,0xb800+page*256)
        c.labels[f'save{page}_hi']=c.labels[f'save{page}']+2
    c.emit(0xe8);c.branch(0xd0,'save')
    for addr,val in ((SOURCE,0),(SOURCE+1,0xb0),(0x83fe,0xc0)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.jump(0x20,'decode')
    c.emit(0xa9,1);a(0x8d,FLAG)
    c.emit(0xa9,0);a(0x8d,outro_text.STATE_FLAG)
    a(0x4c,outro_text.ENTRY)
    c.label('decode');code=decoder(c.origin+len(c.data));c.emit(*code)
    result=bytes(c.finish())
    if ENTRY+len(result)>0x3fce:raise ValueError(f'outro loader too large: {len(result)}')
    return result


def inserts():
    return [(src,data) for src,data,dst in resources()[2]]+[(ENTRY,bootstrap())]
