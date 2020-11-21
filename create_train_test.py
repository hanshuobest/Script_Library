# coding:utf-8
# 将数据分成训练集和测试集单独保存
import os
import random
import glob
import numpy as np
import shutil


def isExist(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        os.mkdir(dir_path)
    else:
        os.mkdir(dir_path)


if __name__ == "__main__":
    xml_lsts = glob.glob(os.getcwd() + "/*.xml")
    total_num = len(xml_lsts)

    trainval_percent = 0.9
    train_percent = 0.9
    test_percent = 0.1

    num_lst = list(range(total_num))
    np.random.shuffle(num_lst)

    train_val_num = int(trainval_percent * total_num)

    train_num = int(train_percent * total_num)
    test_num = int(test_percent * total_num)

    trainval = random.sample(num_lst, train_val_num)
    train = random.sample(trainval, int(train_percent * train_val_num))

    train_dir = "Train"
    test_dir = "Test"
    val_dir = "Val"

    isExist(train_dir)
    isExist(test_dir)
    isExist(val_dir)

    for i in num_lst:
        if i in trainval:
            if i in train:
                shutil.copyfile(
                    xml_lsts[i],
                    os.getcwd() + "/" + train_dir + "/" + os.path.basename(xml_lsts[i]),
                )
                shutil.copyfile(
                    xml_lsts[i][:-3] + "jpg",
                    os.getcwd()
                    + "/"
                    + train_dir
                    + "/"
                    + os.path.basename(xml_lsts[i])[:-3]
                    + "jpg",
                )
            else:
                shutil.copyfile(
                    xml_lsts[i],
                    os.getcwd() + "/" + val_dir + "/" + os.path.basename(xml_lsts[i]),
                )
                shutil.copyfile(
                    xml_lsts[i][:-3] + "jpg",
                    os.getcwd()
                    + "/"
                    + val_dir
                    + "/"
                    + os.path.basename(xml_lsts[i])[:-3]
                    + "jpg",
                )

        else:
            shutil.copyfile(
                xml_lsts[i],
                os.getcwd() + "/" + test_dir + "/" + os.path.basename(xml_lsts[i]),
            )
            shutil.copyfile(
                xml_lsts[i][:-3] + "jpg",
                os.getcwd()
                + "/"
                + test_dir
                + "/"
                + os.path.basename(xml_lsts[i])[:-3]
                + "jpg",
            )
