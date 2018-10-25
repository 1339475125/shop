#coding=utf-8
# 导入必要的包
import argparse
import shelve
import imagehash
import glob
from PIL import Image


# 构建参数解析，并分析参数
ap =argparse.ArgumentParser()
# ap.add_argument("-d","--dataset", required=True, help="~/Downloads/simliar_picture/")
# ap.add_argument("-s","--shelve",required=True, help="shelve数据集的输出")
# args =vars(ap.parse_args())
# for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
# 加载图片并计算哈希值的差异
imagePath = "/home/wrh/Downloads/simliar_picture/watch/image_0002.jpg"
image =Image.open(imagePath)
h = str(imagehash.dhash(image))
print h
# 提取路径中的文件名并更新数据库
# 用散列作为字典的键，文件名添加到值列表
# filename = imagePath[imagePath.rfind("/") + 1:]
# db[h] = db.get(h, []) + [filename]
