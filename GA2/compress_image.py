import os, io
from PIL import Image
import numpy as np

# The original PNG file bytes - write directly and compress
# First let's check if original.png exists
if os.path.exists('original.png'):
    img = Image.open('original.png')
    print('Loaded original.png - Size:', img.size, 'Mode:', img.mode)
    
    # Analyze
    arr = np.array(img.convert('RGB'))
    unique_colors = np.unique(arr.reshape(-1, 3), axis=0)
    print('Unique colors:', len(unique_colors))
    for c in unique_colors:
        print(' ', tuple(c))
    
    # Convert to palette mode PNG
    img_rgb = img.convert('RGB')
    img_p = img_rgb.convert('P', palette=Image.ADAPTIVE, colors=len(unique_colors))
    
    buf = io.BytesIO()
    img_p.save(buf, format='PNG', optimize=True, compress_level=9)
    compressed = buf.getvalue()
    print('Compressed size:', len(compressed), 'bytes')
    
    # Verify lossless
    orig_arr = np.array(img.convert('RGB'))
    comp_arr = np.array(Image.open(io.BytesIO(compressed)).convert('RGB'))
    identical = np.array_equal(orig_arr, comp_arr)
    print('Lossless?', identical)
    
    if identical and len(compressed) < 400:
        with open('compressed.png', 'wb') as f:
            f.write(compressed)
        print('SUCCESS! File saved at compressed.png:', len(compressed), 'bytes')
    elif not identical:
        print('NOT lossless - checking diff...')
        diff = np.argwhere(orig_arr != comp_arr)
        print('Number of different channel values:', len(diff))
        for d in diff[:10]:
            y, x, ch = d
            print(f'  Pixel ({x},{y}) ch={ch}: orig={orig_arr[y,x,ch]}, comp={comp_arr[y,x,ch]}')
else:
    print('original.png not found!')
