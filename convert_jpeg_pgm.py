# coding=utf-8 
from PIL import Image
import os
import glob

def jpg2pgm( jpg_file , pgm_dir ):
    jpg = Image.open( jpg_file )
    gray = jpg.convert('L')
    name = os.path.basename(jpg_file)[:-4] + "pgm"
    gray.save( name )

# 将所有的jpg文件放在当前工作目录，或者 cd {存放jpg文件的目录}
for jpg_file in glob.glob(os.getcwd() + "/*.jpeg"):
    jpg2pgm( jpg_file , os.getcwd() )
