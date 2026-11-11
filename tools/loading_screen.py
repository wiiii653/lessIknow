"""Small ANTIC text display visible while the XEX loads its expansion banks."""
from build_sequence import Code
from build_visual_prototype import xex_segment

SCREEN=0x0600
DLIST=0x0700
ENTRY=0x0780
LINES=('NOW LOADING ATARI XE DEMO', 'SILLY VENTURE 2026 WE', 'AI-SLOP/OGNJEN')

def segments():
    # ANTIC mode 2 uses Atari screen codes (upper-case ATASCII minus 32).
    text=b''.join(bytes(ord(ch)-32 for ch in line.center(40)) for line in LINES)
    display=bytes((0x70,0x70,0x70,0x42,SCREEN&255,SCREEN>>8,2,2,0x41,DLIST&255,DLIST>>8))
    c=Code(ENTRY)
    def store(address,value): c.emit(0xa9,value,0x8d,address&255,address>>8)
    # Set both OS shadows and hardware. Existing bank INITs re-enable VBI,
    # which otherwise replaces hardware registers with old shadow values.
    # CHBASE is $D409. $D018 is COLPF2, the text background colour.
    for address,value in ((0x022f,0x22),(0x0230,DLIST&255),(0x0231,DLIST>>8),
                          (0x02f4,0xe0),(0x02c5,0x0e),(0x02c6,0x00),
                          (0xd402,DLIST&255),(0xd403,DLIST>>8),
                          (0xd409,0xe0),(0xd017,0x0e),(0xd018,0xe0),
                          (0xd400,0x22)):
        store(address,value)
    c.emit(0x60)
    return (xex_segment(SCREEN,text)+xex_segment(DLIST,display)+
            xex_segment(ENTRY,bytes(c.finish()))+xex_segment(0x02e2,ENTRY.to_bytes(2,'little')))
