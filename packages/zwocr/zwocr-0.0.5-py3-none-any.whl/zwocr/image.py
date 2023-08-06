from PIL import Image
from pathlib import Path

def binimagefile(pth, tmppth=None, threshold=200):
    tmppth = tmppth or pth.parent/('%s.tmp'%Path(pth).stem)
    with Image.open(str(pth)) as im:
        im = binimage(im, threshold)
        im.save(tmppth)
    return tmppth

def binimage(im: Image, threshold=200):
    im = im.convert('L')
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    im = im.point(table, '1')
    return im