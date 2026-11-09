"""Composite foreground players and missiles using the playfield palette."""


def player_masks(pixels, memory, height, raster_start=17, rainbow_bands=False,
                 pmg_color_offset=4):
    result = bytearray(pixels)
    players = bool(memory[0xd01d] & 2 and memory[0xd400] & 8)
    missiles = bool(memory[0xd01d] & 1 and memory[0xd400] & 4)
    if not (players or missiles):
        return result
    if memory[0xd01b] & 15 != 1:
        raise ValueError('preview expects players above playfield (PRIOR=1)')
    single = bool(memory[0xd400] & 16)
    base = (memory[0xd407] & (0xf8 if single else 0xfc)) << 8
    stride, offset = (256, 0x400) if single else (128, 0x200)
    colors = {memory[0xd01a]: 0, memory[0xd016]: 1,
              memory[0xd017]: 2, memory[0xd018]: 3}

    def draw(index, missile=False):
        position = memory[0xd004 + index if missile else 0xd000 + index]
        if position == 0:
            return
        color=memory[0xd019] if missile and memory[0xd01b]&0x10 else memory[0xd012+index]
        ink=(pmg_color_offset+(color>>1) if pmg_color_offset>=16 else
             colors.get(color,4+(color>>1)))
        left = position - 48
        size = ((memory[0xd00c] >> (2 * index)) & 3 if missile else
                memory[0xd008 + index] & 3)
        scale = (1, 2, 1, 4)[size]
        address = base + (0x300 if single else 0x180) if missile else base + offset + index * stride
        bits = 2 if missile else 8
        for y in range(height):
            if rainbow_bands:
                from ribbon_dance import rainbow_palette
                # Ideal DLI bands; real transitions include decoder latency.
                band=min(3,(y+9)//78)
                color=rainbow_palette(memory[0x83e2],band,airflow=12<=memory[0x83ed]<16,
                                      kiss=memory[0x83e0]==14 and memory[0x83ed]==15)[4 if missile else index]
                ink=colors.get(color,4+(color>>1))
            line = y + raster_start
            value = memory[address + (line if single else line // 2)]
            if missile:
                value = (value >> (2 * index)) & 3
            for bit in range(bits):
                if value & (1 << (bits - bit - 1)):
                    for dx in range(scale):
                        x = left + bit * scale + dx
                        if 0 <= x < 160:
                            result[y * 160 + x] = ink

    # Fifth-player missiles lie over the playfield but behind the players
    # in PRIOR=$11, so render their splash before the lettering players.
    if memory[0xd01b] & 0x10:
        if missiles:
            for index in range(4):draw(index, missile=True)
        if players:
            for index in range(3,-1,-1):draw(index)
    else:
        # Fixed GTIA object priority: P0/M0 precede P1/M1, etc.
        # Paint the lowest-priority objects first; each player covers its missile.
        for index in range(3,-1,-1):
            if missiles:draw(index, missile=True)
            if players:draw(index)
    return result


def atari_rgb(color):
    """Approximate PAL hue wheel for PMG preview colors outside the playfield."""
    import colorsys
    hue,lum=color>>4,color&15
    if hue==0:return (lum*17,)*3
    angles=(0,42,25,8,330,300,270,240,220,195,165,140,110,80,60,45)
    rgb=colorsys.hsv_to_rgb(angles[hue]/360,0.78,min(1,0.08+lum/16))
    return tuple(round(channel*255) for channel in rgb)
