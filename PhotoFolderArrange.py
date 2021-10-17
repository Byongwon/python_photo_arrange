#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import logging
import timeit
import os
import shutil
import re
import pathlib
import argparse
from exifread.tags import DEFAULT_STOP_TAG, FIELD_TYPES
from exifread import process_file

def using():
    print('#####cmd src dest#####')

def copyfile(dst, datefolder, orgfile):
    dstfolder = os.path.join(dst, datefolder)
    if not os.path.exists(dstfolder) :
        os.makedirs(dstfolder)
    shutil.copy(orgfile, dstfolder)
    print("Copy " + orgfile + " To " + dstfolder)


def estimateDateByFileName(fname):
    # checker = re.compile(r'\d{4}\d{2}\d{2}')
    checker = re.compile(r'(19|20\d\d)[-_ ]?(0[1-9]|1[012])[-_ ]?(0[1-9]|[12][0-9]|3[01])')
    m = checker.search(fname)

    if m:
        print(m.groups())
        return m.group(1) + "_" + m.group(2) + "_" + m.group(3)
    else:
        return "unknown"


def PhotoArrage(src, dst):

    for f in os.listdir(src):
        #print(f)
        ff = os.path.join(src, f)
        if os.path.isfile(ff):
            ef = open(ff, 'rb')
            tags = process_file(ef, stop_tag='EXIF DateTimeOriginal')
            if not tags:
                datefolder = estimateDateByFileName(f)
                copyfile(dst, datefolder, ff)
                continue
            """ 
            for tag in tags.keys(): 
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'): 
                    print "Key: %s, value %s" % (tag, tags[tag]) 
            """
            try:
                # mk date folder
                oriTime = str(tags["EXIF DateTimeOriginal"]).split(" ")[0].split(":")
                datefolder = oriTime[0] + "/" + oriTime[0] + '-' + oriTime[1] + '-' + oriTime[2]
                # mk camera folder
                cameraType = str(tags['Image Model'])
                # mk file type folder
                fileType = str(pathlib.Path(ff).suffix)[1:]

                # concat dst folder
                dstFolderDtl = datefolder + '/' + cameraType + '/' + fileType
                # print(dstFolderDtl)

                copyfile(dst, dstFolderDtl, ff)
                ef.close()
            except:
                datefolder = estimateDateByFileName(f)
                copyfile(dst, datefolder, ff)


def main(args):
    src = args.src
    dst = args.dst
    PhotoArrage(src, dst)


if __name__ == '__main__':
    src = '/Users/abraham/Pictures/ReadyToMove/'
    dst = '/Volumes/Samsung NVME SSD 1T/Photo/'
    #argsparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", help="source folder", default=src)
    parser.add_argument("--dst", help="destination folder", default=dst)
    args = parser.parse_args()

    if os.path.exists(dst):
        main(args)
    else:
        print(f'{dst} does not exists!!')
        pass