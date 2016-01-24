#!/usr/bin/python

import sys
import os
import shutil
from PIL import Image

def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)

    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.

    return reduce(lambda x, (y, z): x | (z << y), enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())), 0)

if __name__ == '__main__':
    path = sys.argv[1]
    dupefolder = 'dupes'
    dupedir = path + os.sep + dupefolder + os.sep
    filecount = 0
    dupecount = 0

    hashs = {}

    for root, dirs, files in os.walk(path):
        folder = os.path.normpath(root) + os.sep

        if folder.split(os.sep)[-2] == dupefolder:
            continue

        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG', '.gif', '.GIF')):
                image = folder + file

                filecount += 1

                imghash = avhash(image)

                if hashs.has_key(imghash):
                    print '- dupe "%s" -> "%s"' % (hashs.get(imghash), image)
                    dupecount += 1

                    if not os.path.exists(dupedir):
                        os.makedirs(dupedir)

                    if not os.path.isfile(dupedir + file):
                        shutil.move(image, dupedir)
                        continue

                    os.remove(image)
                    continue

                hashs[imghash] = image
                # print '+ %s [%s]' % (image, imghash)