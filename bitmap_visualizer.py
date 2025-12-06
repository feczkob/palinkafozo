#!/usr/bin/env python3
"""
Bitmap Visualizer - Converts 5x8 LCD character bitmaps into text/image representations
"""

CHAR_HEATER_ENABLED_OFF = [
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b11111,
    0b11111,
]

CHAR_HEATER_ENABLED_ON = [
    0b01010,
    0b10101,
    0b00000,
    0b01010,
    0b10101,
    0b00000,
    0b11111,
    0b11111,
]



def visualize_bitmap(bitmap, char='█', empty=' '):
    """
    Visualize a 5x8 bitmap as ASCII art
    
    Args:
        bitmap: List of 8 bytes representing the 5x8 pattern
        char: Character to use for "on" pixels (default: █)
        empty: Character to use for "off" pixels (default: space)

    Returns:
        String representation of the bitmap
    """
    output = []
    for row in bitmap:
        line = ""
        for bit in range(4, -1, -1):  # Check bits 4 down to 0 (5 bits)
            if row & (1 << bit):
                line += char
            else:
                line += empty
        output.append(line)
    return '\n'.join(output)


def bitmap_to_image(bitmap, filename='bitmap.png', scale=10):
    """
    Create a PNG image from a 5x8 bitmap (requires PIL/Pillow)
    
    Args:
        bitmap: List of 8 bytes representing the 5x8 pattern
        filename: Output filename
        scale: Scale factor for the image (default: 10px per pixel)
    """
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("PIL/Pillow not installed. Run: pip install Pillow")
        return
    
    width, height = 5, 8
    img = Image.new('RGB', (width * scale, height * scale), 'white')
    draw = ImageDraw.Draw(img)
    
    for y, row in enumerate(bitmap):
        for x in range(5):
            bit = 4 - x  # Bit position (4 to 0)
            if row & (1 << bit):
                # Draw filled rectangle for "on" pixel
                x0 = x * scale
                y0 = y * scale
                x1 = x0 + scale
                y1 = y0 + scale
                draw.rectangle([x0, y0, x1, y1], fill='black')
    
    img.save(filename)
    print(f"Image saved to {filename}")


if __name__ == "__main__":
    print(visualize_bitmap(CHAR_HEATER_ENABLED_ON))
    print(visualize_bitmap(CHAR_HEATER_ENABLED_OFF))
    
    # Uncomment to create PNG image (requires Pillow)
    #bitmap_to_image(CHAR_HEATER_ENABLED_ON, 'char_heater_enabled_on.png')
