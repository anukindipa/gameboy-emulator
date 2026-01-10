"""
It works like this:
The Logo is simple a bitmap
Each pair of bytes encodes a 4x4 tile of 8 pixels (4 pixels per byte)
0xCE = 11001110
1100 is the first 4 pixels of the first row
1110 is the first 4 pixels of the next row
0xED = 1110 1101
So the first two bytes encodes:
██__ 
███_
███_
██_█
"""

# The Nintendo Logo in its 48 bytes of glory
Logo = [
    0xCE, 0xED, 0x66, 0x66, 0xCC, 0x0D, 0x00, 0x0B, 0x03,
    0x73, 0x00, 0x83, 0x00, 0x0C, 0x00, 0x0D, 0x00, 0x08,
    0x11, 0x1F, 0x88, 0x89, 0x00, 0x0E, 0xDC, 0xCC, 0x6E,
    0xE6, 0xDD, 0xDD, 0xD9, 0x99, 0xBB, 0xBB, 0x67, 0x63,
    0x6E, 0x0E, 0xEC, 0xCC, 0xDD, 0xDC, 0x99, 0x9F, 0xBB,
    0xB9, 0x33, 0x3E]

# The boot logo is 48x8 pixels, made of 12x2 tiles (4x4 pixels each)
def convert_to_arr(Logo):
    """Convert the Logo byte array to a 2D array of pixels (0=white, 3=black)"""
    pixels = [[0 for _ in range(48)] for _ in range(8)]  # 8 rows x 48 cols
    
    # construst the tiles
    tiles = []
    for t in range(0, 48, 2):  # 24 pairs of bytes
        b1 = format(Logo[t], '08b') 
        b2 = format(Logo[t+1], '08b') 
        tile = []
        tile.append(b1[0:4])  # row 0 of tile
        tile.append(b1[4:8])  # row 1 of tile
        tile.append(b2[0:4])  # row 2 of tile
        tile.append(b2[4:8])  # row 3 of tile
        tiles.append(tile)
    
    # Place tiles into the pixel grid: 12 tiles wide, 2 tiles tall
    for tile_idx, tile in enumerate(tiles):
        tile_x = tile_idx % 12  # which tile horizontally (0-11)
        tile_y = tile_idx // 12  # which tile vertically (0-1)
        
        # Starting pixel position for this tile
        px_start = tile_x * 4
        py_start = tile_y * 4
        
        # Fill in the 4×4 tile pixels
        for row in range(4):
            for col in range(4):
                pixels[py_start + row][px_start + col] = int(tile[row][col])
            
    return pixels

print("--------------------------------------------")
print("Nintendo Logo array")
print("--------------------------------------------")
print('\n'.join(''. join(str(ch) for ch in row) for row in convert_to_arr(Logo)))

print("--------------------------------------------")
print("Logo bitmap")
print("--------------------------------------------")
for row in convert_to_arr(Logo):
    print("".join([ '█' if p else ' ' for p in row]))