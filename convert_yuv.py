# coding:utf-8
‘’‘
将图像转为yuv
’‘’
import glob
import json

import cv2
import numpy as np
import traceback
import os

import sys


def jpg2bgr(img_dir):
    imgs = glob.glob(img_dir)
    imgs.sort()
    for idx, img_p in enumerate(imgs[0:300]):
        img = cv2.imread(img_p)
        y, u, v = cv2.split(img)  # b, g, r

        height = img.shape[0]
        width = img.shape[1]
        file_path = "/Users/jack/bgr/{}.bgr".format(idx)
        fileSave = open(file_path, "wb")

        for step in range(0, int(height)):
            for step2 in range(0, width):
                fileSave.write(y[int(step), step2])

        for step in range(0, int(height)):
            for step2 in range(0, width):
                fileSave.write(u[int(step), step2])
        for step in range(0, int(height)):
            for step2 in range(0, width):
                fileSave.write(v[int(step), step2])
        fileSave.close()


def load_json():
    res = np.loadtxt('log.ssd', dtype=np.str)
    res_line = json.loads(res[0])
    print("pic={},[label,xmin,xmax,ymin,ymax,confidence]={}".format(res_line['pic'], res_line['boxes']))


def img_show(img, wait=0, size=0):
    if size != 0:
        show = cv2.resize(img, (size, size))
    else:
        show = img
    cv2.imshow('img', show)
    cv2.waitKey(0)


def jpg2yuv_sp(pd, type="caipin_resnet"):
    if type == "renliu":
        pd_res = pd.strip('/') + "_yuv"
        if not os.path.exists(pd_res):
            os.mkdir(pd_res)
        for idx, hour in enumerate(os.listdir(pd)):

            files_all = glob.glob(os.path.join(pd, hour, "*"))
            files_all.sort()
            if not os.path.exists(os.path.join(pd_res, str(idx))):
                os.mkdir(os.path.join(pd_res, str(idx)))
            for idx_f, f in enumerate(files_all):
                if (idx_f % 100) == 0:
                    print(idx, idx_f)
                img = cv2.imread(f)
                img = cv2.resize(img, (416, 416))
                h, w = img.shape[0:2]
                yuv_p = cv2.cvtColor(img, cv2.COLOR_BGR2YUV_I420)
                yuv_sp = yuv_p2sp(yuv_p, h=h, w=w)
                # img_show(cv2.cvtColor(yuv_sp, cv2.COLOR_YUV2BGR_NV21), size=416)

                h, w = yuv_sp.shape
                fileSave = open(os.path.join(pd_res, str(idx), str(idx_f) + '.yuv'), "wb")
                for step in range(0, int(h)):
                    for step2 in range(0, w):
                        fileSave.write(yuv_sp[int(step), step2])
                fileSave.close()
    else:
        imgs = []
        imgs_sku = [os.path.join(pd, sku) for sku in os.listdir(pd)]
        for img_sku in imgs_sku:
            imgs.extend([os.path.join(img_sku, img) for img in os.listdir(img_sku)])
        print(imgs)
        for idx, img_p in enumerate(imgs):
            print(img_p)
            img = cv2.imread(img_p)
            if type == "caipin_resnet50":
                # h, w = img.shape[0:2]
                # if h < w:
                #     img = img[0:h, int((w - h) / 2):w - int((w - h) / 2)]
                # else:
                #     img = img[int((h - w) / 2):h - int((h - w) / 2), 0:w]
                img = cv2.resize(img, (224, 224))
                h, w = img.shape[0:2]
            elif type == "caipin_yolov3":
                img = cv2.resize(img, (416, 416))
                h, w = img.shape[0:2]
            elif type == "pose":
                img = cv2.resize(img, (192, 256))
                h, w = img.shape[0:2]
            else:
                h, w = img.shape[0:2]

            yuv_p = cv2.cvtColor(img, cv2.COLOR_BGR2YUV_I420)
            yuv_sp = yuv_p2sp(yuv_p, h=h, w=w)
            # img_show(cv2.cvtColor(yuv_sp, cv2.COLOR_YUV2BGR_NV21), size=416)

            h, w = yuv_sp.shape
            fileSave = open(img_p, "wb")
            for step in range(0, int(h)):
                for step2 in range(0, w):
                    fileSave.write(yuv_sp[int(step), step2])
            fileSave.close()


def yuv_p2sp(yuvp, w, h):
    shape = (int(h * 3 / 2), w)
    half = int((shape[0] - h) / 2)

    yuv_sp = np.zeros(shape, dtype=np.uint8)
    yuv_sp[0:h, :] = yuvp[0:h, :]
    yuv_sp[h:shape[0], 0::2] = np.reshape(yuvp[h + half:shape[0], :], (int(h / 2), int(w / 2)))[:, :]
    yuv_sp[h:shape[0], 1::2] = np.reshape(yuvp[h:h + half, :], (int(h / 2), int(w / 2)))[:, :]
    return yuv_sp


def show_yuv_sp(fd, h=1080, w=1920):
    fileSave = open(fd, "rb")
    raw = fileSave.read(int(w * h / 2 * 3))
    yuv = np.frombuffer(raw, dtype=np.uint8)
    shape = (int(h / 2 * 3), w)
    yuv = yuv.reshape(shape)
    bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_NV21)
    # cv2.rectangle(bgr, (78, 746), (378, 1036), (255, 125, 255),4)
    # cv2.rectangle(bgr, (304, 280), (788, 634), (255, 125, 255), 4)
    bgr = cv2.resize(bgr, (int(w / 2), int(h / 2)))

    img_show(bgr)


def img2video():
    import cv2
    from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
    import os
    import glob

    img_root = '/Users/jack/imgs/renliu_20190410_00'
    out_root = '/Users/jack/imgs/renliu_20190410_00.avi'
    # Edit each frame's appearing time!
    fps = 30
    fourcc = VideoWriter_fourcc(*"MJPG")  # 支持jpg
    videoWriter = cv2.VideoWriter(out_root, fourcc, fps, (416, 416))
    im_names = glob.glob("/Users/jack/imgs/renliu_20190410_00/*")
    im_names.sort()
    print(im_names, len(im_names))
    for idx, im_name in enumerate(im_names):
        if idx % 1000 == 0:
            print(idx)
        frame = cv2.imread(im_name)
        frame = cv2.resize(frame, (416, 416))
        videoWriter.write(frame)

    videoWriter.release()


if __name__ == '__main__':
    # show_yuv_sp("caipin_yolov3/yolov3/ee:ee:bb:03:00:03_ee:ee:bb:03:00:03_20190528_19-59-36-062136__1.jpg", h=416,
    #             w=416)
    # show_yuv_sp("caipin_resnet50/E01/ee:ee:bb:03:10:03_E01_20190528_13-04-10-667903_00000000_0.949463.jpg", h=224, w=224)
    # img = cv2.imread('/Users/jack/check/test/1.jpg')
    # cv2.rectangle(img, (128, 33), (299, 380), (255, 125, 255), 4)
    # img_show(img)

    if len(sys.argv) < 2:
        print("<image file> <type>")
    if sys.argv[2] == "caipin_resnet50":
        jpg2yuv_sp(sys.argv[1], type="caipin_resnet50")
    elif sys.argv[2] == "caipin_yolov3":
        jpg2yuv_sp(sys.argv[1], type="caipin_yolov3")
    elif sys.argv[2] == "renliu":
        jpg2yuv_sp(sys.argv[1], type="renliu")
    elif sys.argv[2] == "pose":
        jpg2yuv_sp(sys.argv[1], type="pose")
    else:
        jpg2yuv_sp(sys.argv[1], type="origin")
