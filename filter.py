import os
from glob import glob
import shutil
with open("all_model.txt", "r") as f:
    all_line = f.readlines()

img_lsts = glob(os.getcwd() + "/*.jpg")
save = "save"
for line in all_line:
    line = line.strip()
    full_name = os.path.join(os.getcwd(), line)
    #print("full_name: " , full_name)
    if os.path.exists(full_name):
        print("------------------------------")
        print(full_name)
        print("******************************")
        shutil.move(full_name, os.path.join(save, line))
    else:
        print("{} not exists".format(full_name))
        continue
