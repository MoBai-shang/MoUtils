from PIL import Image
from images2gif import writeGif
import os
import imageio
import numpy as np
def create_gif(image_list, gif_name):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    # Save them as frames into a gif
    imageio.mimsave(gif_name, frames, 'GIF', duration=0.5)
    return
def createGif(filenames,gif_name):
    frames = []
    for image_name in filenames:  # 索引各自目录
        im = Image.open(image_name)  # 将图片打开，本文图片读取的结果是RGBA格式，如果直接读取的RGB则不需要下面那一步
        im = im.convert("RGB")  # 通过convert将RGBA格式转化为RGB格式，以便后续处理
        im = np.array(im)  # im还不是数组格式，通过此方法将im转化为数组
        frames.append(im)  # 批量化
    writeGif(gif_name, frames, duration=0.1 )  #subRectangles=False 生成GIF，其中durantion是延迟，这里是1ms
def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    '''
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results

def processImage(path):
    '''
    Iterate the GIF, extracting each frame.
    '''
    mode = analyseImage(path)['mode']
    im = Image.open(path)
    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')
    try:
        while True:
            print("saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile))
            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)
            new_frame = Image.new('RGBA', im.size)
            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)
            new_frame.paste(im, (0, 0), im.convert('RGBA'))
            new_frame.save('%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), i), 'PNG')
            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass
def Resize(srcImg,dstImg):
    simg=Image.open(srcImg)
    dimg=simg.resize((1080, 1906), Image.ANTIALIAS)
    dimg.save(dstImg)
    print(srcImg,"done")
def dirImgRsize(srcPath, dstPath):  # 将位于srcPath下的图片压缩处理后结果存于dstPath下
        # 如果不存在目的目录则创建一个，保持层级结构
        if not os.path.exists(dstPath):
            os.makedirs(dstPath)
            print(dstPath, '创建成功！')
        for filename in os.listdir(srcPath):
            # 拼接完整的文件或文件夹路径
            srcFile = os.path.join(srcPath, filename)
            dstFile = os.path.join(dstPath, filename)
            # 如果是文件就处理
            if os.path.isfile(srcFile):
                Resize(srcFile,dstFile)
            # 如果是文件夹就递归
            if os.path.isdir(srcFile):
                dirImgRsize(srcFile, dstFile)
def main():
    #image_list=[filename for filename in os.listdir("output_wps")]
    image_list = ["output_wps/output_wps图片_"+str(i)+".jpg" for i in range(1,148)]
    image_list = ['picture/'+str(i) + ".png" for i in range(1, 10)]

    gif_name = 'created_gif4.gif'
    create_gif(image_list, gif_name)
    #im.save('gif.gif', save_all=True, append_images=image_list[1:], loop=1, duration=0.1, comment=b"aaabb")
    #processImage('test_gif.gif')
#dirImgRsize("output_wps", "out_img")
main()






'''
outfilename = "my.gif" # 转化的GIF图片名称
filenames = []         # 存储所需要读取的图片名称
for i in range(100):   # 读取100张图片
    filename = path    # path是图片所在文件，最后filename的名字必须是存在的图片
    filenames.append(filename)              # 将使用的读取图片汇总
frames = []
for image_name in filenames:                # 索引各自目录
    im = Image.open(image_name)             # 将图片打开，本文图片读取的结果是RGBA格式，如果直接读取的RGB则不需要下面那一步
    im = im.convert("RGB")                  # 通过convert将RGBA格式转化为RGB格式，以便后续处理
    im = np.array(im)                       # im还不是数组格式，通过此方法将im转化为数组
    frames.append(im)                       # 批量化
writeGif(outfilename, frames, duration=0.1, subRectangles=False) # 生成GIF，其中durantion是延迟，这里是1ms
# -*- coding: UTF-8 -*-
'''