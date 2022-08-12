import numpy as np
from PIL import Image
from typing import Union,List
import os
from shutil import copyfile,move
import cv2
from glob import glob
from tqdm.auto import tqdm
from collections import Counter
import cv2
def split_img(src_img:str,v_cut:List[Union[int,float]]=[],h_cut:List[Union[int,float]]=[],save_dir:str=''):
    if len(v_cut)==0 and len(h_cut)==0:
        return
    if len(v_cut)>0 and min(v_cut)<0 or len(h_cut)>0 and min(h_cut)<0:
        raise ValueError('neither parameter V nor parameter h can be less than 0')
    img=Image.open(src_img)
    if save_dir=='':
        save_dir=os.path.dirname(src_img)
    os.makedirs(save_dir, exist_ok=True)
    img_name,img_format = os.path.basename(src_img).split('.')
    ImgSize=img.size
    v_cut=[round(v*ImgSize[0]) if v<1 else round(v) for v in v_cut]
    h_cut = [round(h * ImgSize[1]) if h < 1 else round(h) for h in h_cut]
    v_cut.extend([0,ImgSize[0]])
    h_cut.extend([0,ImgSize[1]])
    v_cut=sorted(set(v_cut))
    h_cut=sorted(set(h_cut))
    for i in range(len(v_cut)-1):
        for j in range(len(h_cut)-1):
            img.crop( (v_cut[i], h_cut[j],v_cut[i+1],h_cut[j+1])).save(os.path.join(save_dir,'%s-(%d,%d,%d,%d).%s'%(img_name,v_cut[i], h_cut[j],v_cut[i+1],h_cut[j+1],img_format)))


def img_filter(src_path,pad:int=255,bias=44):
    img = Image.open(src_path)
    canvas=Image.fromarray(np.zeros((img.size[1],img.size[0]))).convert("RGB")
    #gray = img.convert('L')  # 转换成灰度
    #gray.point(lambda i: i if i>=255 else 0).show()
    r,g,b = img.split()
    # select regions where red is less than 100
    # 如果变量mask对应图像的值为255，则模板图像的值直接被拷贝过来；如果变量mask对应图像的值为0，则保持当前图像的原始值。变量mask对应图像的其他值，将对两张图像的值进行透明融合。
    # mask :透明度
    mask = r.point(lambda i: (i<pad-bias or i>pad+bias) and 255)
    canvas.paste(img,mask=mask)
    canvas.show()
    #im = Image.merge(img.mode, (mask,source[G],source[B]))

def crop_img(src_img:str,v_cut:List[Union[int,float]]=[],h_cut:List[Union[int,float]]=[],save_dir:str=''):
    if len(v_cut)==0 and len(h_cut)==0:
        return
    if len(v_cut)>0 and min(v_cut)<0 or len(h_cut)>0 and min(h_cut)<0:
        raise ValueError('neither parameter V nor parameter h can be less than 0')
    img=Image.open(src_img)
    if save_dir=='':
        save_dir=os.path.dirname(src_img)
    os.makedirs(save_dir, exist_ok=True)
    img_name,img_format = os.path.basename(src_img).split('.')
    ImgSize=img.size
    v_cut=[round(v*ImgSize[0]) if v<1 else round(v) for v in v_cut]
    h_cut = [round(h * ImgSize[1]) if h < 1 else round(h) for h in h_cut]
    v_cut.extend([0,ImgSize[0]])
    h_cut.extend([0,ImgSize[1]])
    v_cut=sorted(set(v_cut))
    h_cut=sorted(set(h_cut))
    for i in range(len(v_cut)-1):
        for j in range(len(h_cut)-1):
            img.crop( (v_cut[i], h_cut[j],v_cut[i+1],h_cut[j+1])).save(os.path.join(save_dir,'%s-(%d,%d,%d,%d).%s'%(img_name,v_cut[i], h_cut[j],v_cut[i+1],h_cut[j+1],img_format)))


def pad_split_Image(src_dir:str,save_dir:str=None,*,pad_values:List[tuple]=[(250,255)],pad_bias:int=4,pad_width:int=2,oritention=['v'],rate:float=1,ignore_edge:bool=False,min_shape_vh=(1,1),formats=['png','jpg']):
    '''
    :param src_dir: 源图像文件夹，或单个图像文件路径名，或多个图像文件路径名列表、元组
    :param save_dir: 保存图像文件夹，当值为None时，为第一个源图像所在文件夹
    :param pad_values: 灰度图像中的分割元素，当pad_values值为None时，自动依据图像计算分割元素值，此时，当pad_bias为非正数时，水平或垂直方向上完全相同的像素作为分割元素值。当pad_bias为正数时，水平或垂直方向上像素值波动不大于该值时则设置为分割元素；当pad_values值不为None时，将像素值界于pad_values闭区间范围内的像素点作为分割元素。
    :param pad_bias: 当pad_values为None时，控制自动求分割点算法的参数
    :param pad_width: 最小合法分割条带宽度
    :param oritention: 分割方向，列表或元组，取值为’h‘或’v‘
    :param rate: 水平或垂直方向上像素点作为分割点所具备满足pad_value条件的最小比例
    :param ignore_edge: 是否忽略图像两端
    :param min_shape_vh: 保存图像的最小尺寸，为列表或元组，当元素值小于1时，将被视为比例
    :param formats: 源文件夹中指定格式的文件作为输入图像
    :return: None
    '''
    if isinstance(src_dir,str):
        if os.path.isdir(src_dir):
            srcs=[]
            for fma in formats:
                srcs.extend(glob(src_dir+'/*'+('' if '.' in fma else '.')+fma))
        else:
            srcs=[src_dir]
    elif isinstance(src_dir,tuple) or isinstance(src_dir,list):
        srcs=src_dir
    else:
        raise ValueError('src_dir must be tuple, list, or str')
    if save_dir is None or save_dir=='':
        save_dir = os.path.dirname(srcs[0])
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if rate<0 or rate>1:
        raise ValueError('rate error')
    bar=tqdm(srcs)
    for src_path in bar:
        img = Image.open(src_path)
        ImgSize = img.size
        ImgSize0=ImgSize[0]*rate
        ImgSize1=ImgSize[1]*rate
        img_name, img_format = os.path.basename(src_path).split('.')
        bar.set_description(img_name)
        gray = img.convert('L')  # 转换成灰度
        pixel=np.array(gray)
        v_cuts=[]
        h_cuts=[]

        if pad_values is None:
            if pad_bias<1:
                if 'v' in oritention:
                    i = 0
                    while i < ImgSize[0]:
                        if sum(pixel[:, i] == pixel[0, i])>=ImgSize1:
                            j = i + 1
                            while j < ImgSize[0] and sum(pixel[:, j] == pixel[0, i])>=ImgSize1:
                                j = j + 1
                            if j - i >= pad_width:
                                v_cuts.append((i, j))
                            i = j
                        else:
                            i = i + 1
                if 'h' in oritention:
                    i = 0
                    while i < ImgSize[1]:
                        if sum(pixel[i, :] == pixel[i, 0])>=ImgSize0:
                            j = i + 1
                            while j < ImgSize[1] and sum(pixel[j, :] == pixel[i, 0])>=ImgSize0:
                                j = j + 1
                            if j - i >= pad_width:
                                h_cuts.append((i, j))
                            i = j
                        else:
                            i = i + 1
            else:
                if 'v' in oritention:
                    f=round((0.5-rate/2)*ImgSize[1])
                    t=ImgSize[1]-f
                    i =0
                    while i < ImgSize[0]:
                        vimin,vimax=pixel[f:t, i].min(),pixel[f:t, i].max()
                        if vimax-vimin<=pad_bias:
                            j = i + 1
                            vmins, vmaxs = [vimin], [vimax]
                            vms_min, vms_max = vimin, vimax
                            while j < ImgSize[0]:
                                vmin,vmax=pixel[f:t, j].min(),pixel[f:t, j].max()
                                if vmax-vmin<=pad_bias:
                                    vmins.append(vmin)
                                    vmaxs.append(vmax)
                                    vms_min = min(vms_min, vmin)
                                    vms_max = max(vms_max, vmax)
                                    while vms_max-vms_min>pad_bias:
                                        vmins.pop(0)
                                        vmaxs.pop(0)
                                        vms_min,vms_max=min(vmins),max(vmaxs)
                                    j = j + 1
                                else:
                                    break
                            if len(vmins) >= pad_width:
                                v_cuts.append((i, j))
                            i = j
                        i = i + 1

                if 'h' in oritention:
                    i = 0
                    f = round((0.5 - rate / 2) * ImgSize[0])
                    t = ImgSize[0] - f

                    while i < ImgSize[1]:
                        vimin, vimax = pixel[i, f:t].min(), pixel[i, f:t].max()
                        if vimax - vimin <= pad_bias:
                            j = i + 1
                            vmins, vmaxs = [vimin], [vimax]
                            vms_min, vms_max = vimin, vimax
                            while j < ImgSize[1]:
                                vmin, vmax = pixel[j, f:t].min(), pixel[j, f:t].max()
                                if vmax - vmin <= pad_bias:
                                    vmins.append(vmin)
                                    vmaxs.append(vmax)
                                    vms_min = min(vms_min, vmin)
                                    vms_max = max(vms_max, vmax)

                                    while vms_max - vms_min > pad_bias:
                                        vmins.pop(0)
                                        vmaxs.pop(0)
                                        vms_min, vms_max = min(vmins), max(vmaxs)
                                    j = j + 1
                                else:
                                    break
                            if len(vmins) >= pad_width:
                                h_cuts.append((i, j))
                            i = j
                        i = i + 1
        else:
            if 'v' in oritention:
                i = 0
                while i<ImgSize[0]:
                    #if np.logical_or.reduce([sum(pixel[:, i] >= l)>=ImgSize1 & sum(pixel[:, i] <= u)>=ImgSize1 for (l, u) in pad_values]):
                    if np.logical_or.reduce([sum((pixel[:, i] >= l) & (pixel[:, i] <= u))>=ImgSize1 for (l, u) in pad_values]):

                        j=i+1
                        #while j<ImgSize[0] and np.logical_or.reduce([sum(pixel[:, j] >= l)>=ImgSize1 & sum(pixel[:, j] <= u)>=ImgSize1 for (l, u) in pad_values]):
                        while j<ImgSize[0] and np.logical_or.reduce([sum((pixel[:, j] >= l) & (pixel[:, j] <= u))>=ImgSize1 for (l, u) in pad_values]):
                            j=j+1
                        if j-i>=pad_width:
                            v_cuts.append((i,j))
                        i=j

                    i=i+1

            if 'h' in oritention:
                i = 0
                while i<ImgSize[1]:
                    #if np.logical_or.reduce([sum(pixel[i,:] >= l)>=ImgSize0 & sum(pixel[i,:] <= u)>=ImgSize0 for (l, u) in pad_values]):
                    if np.logical_or.reduce([sum((pixel[i,:] >= l) & (pixel[i,:] <= u))>=ImgSize0 for (l, u) in pad_values]):
                        j=i+1
                        #while j<ImgSize[1] and np.logical_or.reduce([sum(pixel[j,:] >= l)>=ImgSize0 & sum(pixel[j,:] <= u)>=ImgSize0 for (l, u) in pad_values]):
                        while j<ImgSize[1] and np.logical_or.reduce([sum((pixel[j,:] >= l) & (pixel[j,:] <= u))>=ImgSize0 for (l, u) in pad_values]):
                            j=j+1
                        if j-i>=pad_width:
                            h_cuts.append((i,j))
                        i=j
                    i=i+1

        if len(v_cuts)==0 and len(h_cuts)==0:
            print('failed to located pad area!')
            return

        v_cuts=[(0,ImgSize[0])] if len(v_cuts)==0 else [(v2,v1) for (_,v2),(v1,_) in zip(v_cuts[:-1],v_cuts[1:])] if ignore_edge else ([(0, v_cuts[0][0])]+[(v2,v1) for (_,v2),(v1,_) in zip(v_cuts[:-1],v_cuts[1:])]+[(v_cuts[-1][1], ImgSize[0])])
        h_cuts=[(0,ImgSize[1])] if len(h_cuts)==0 else [(v2,v1) for (_,v2),(v1,_) in zip(h_cuts[:-1],h_cuts[1:])] if ignore_edge else ([(0, h_cuts[0][0]) ]+[(v2,v1) for (_,v2),(v1,_) in zip(h_cuts[:-1],h_cuts[1:])]+[(h_cuts[-1][1], ImgSize[1])])


        min_shape_vh=(min_shape_vh[0] if min_shape_vh[0]>=1 else min_shape_vh[0]*ImgSize[0],min_shape_vh[1] if min_shape_vh[1]>=1 else min_shape_vh[1]*ImgSize[1])
        for v1,v2 in v_cuts:
            if v2-v1<min_shape_vh[0]:
                continue
            for h1,h2 in h_cuts:
                if h2-h1>=min_shape_vh[1]:
                    img.crop((v1, h1, v2, h2)).save(os.path.join(save_dir, '%s-(%d,%d,%d,%d).%s' % (img_name, v1, h1, v2,h2, img_format)),quality=95)

def pad_split_cv2(src_dir:str,save_dir:str=None,*,pad_values:List[tuple]=None,pad_bias:int=8,pad_width:int=8,oritention=['v'],rate:float=1,f_t_rate=None,ignore_edge:bool=False,min_shape_hv=(1,1),draw_rect:bool=False,formats=['png','jpg'],save_format=None):
    '''
    :param src_dir: 源图像文件夹，或单个图像文件路径名，或多个图像文件路径名列表、元组
    :param save_dir: 保存图像文件夹，当值为None时，为第一个源图像所在文件夹
    :param pad_values: 灰度图像中的分割元素，当pad_values值为None时，自动依据图像计算分割元素值，此时，当pad_bias为非正数时，水平或垂直方向上完全相同的像素作为分割元素值。当pad_bias为正数时，水平或垂直方向上像素值波动不大于该值时则设置为分割元素；当pad_values值不为None时，将像素值界于pad_values闭区间范围内的像素点作为分割元素。
    :param pad_bias: 当pad_values为None时，控制自动求分割点算法的参数
    :param pad_width: 最小合法分割条带宽度
    :param oritention: 分割方向，列表或元组，取值为’h‘或’v‘
    :param rate: 水平或垂直方向上像素点作为分割点所具备满足pad_value条件的最小比例
    :param f_t_rate: 边缘忽略比
    :param ignore_edge: 是否忽略图像两端
    :param min_shape_hv: 保存图像的最小尺寸，为列表或元组，当元素值小于1时，将被视为比例
    :param formats: 源文件夹中指定格式的文件作为输入图像
    :param save_format: 保存图像的格式，当值为None时，保存为源格式
    :return: None
    '''
    if isinstance(src_dir,str):
        if os.path.isdir(src_dir):
            srcs=[]
            for fma in formats:
                srcs.extend(glob(src_dir+'/*'+('' if '.' in fma else '.')+fma))
        else:
            srcs=[src_dir]
    elif isinstance(src_dir,tuple) or isinstance(src_dir,list):
        srcs=src_dir
    else:
        raise ValueError('src_dir must be tuple, list, or str')
    if save_dir is None or save_dir=='':
        save_dir = os.path.dirname(srcs[0])
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if rate<0 or rate>1:
        raise ValueError('rate error')
    if isinstance(save_format,str) and '.' in save_format:
        save_format=save_format.split('.')[1]
    bar=tqdm(srcs)
    for src_path in bar:
        img_name, img_format = os.path.basename(src_path).split('.')
        if isinstance(save_format,str):
            img_format=save_format
        bar.set_description(img_name)
        image = cv2.imread(src_path)
        pixel= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        Imgsize1 = pixel.shape[1] * rate
        Imgsize0 = pixel.shape[0] * rate
        v_cuts=[]
        h_cuts=[]

        if pad_values is None:
            if pad_bias<1:
                if 'v' in oritention:
                    i = 0
                    while i < pixel.shape[1]:
                        if sum(pixel[:, i] == pixel[0, i])>=Imgsize0:
                            j = i + 1
                            while j < pixel.shape[1] and sum(pixel[:, j] == pixel[0, i])>=Imgsize0:
                                j = j + 1
                            if j - i >= pad_width:
                                v_cuts.append((i, j))
                            i = j
                        else:
                            i = i + 1
                if 'h' in oritention:
                    i = 0
                    while i < pixel.shape[0]:
                        if sum(pixel[i, :] == pixel[i, 0])>=Imgsize1:
                            j = i + 1
                            while j < pixel.shape[0] and sum(pixel[j, :] == pixel[i, 0])>=Imgsize1:
                                j = j + 1
                            if j - i >= pad_width:
                                h_cuts.append((i, j))
                            i = j
                        else:
                            i = i + 1
            else:
                if 'v' in oritention:
                    i =0
                    if f_t_rate is None:
                        f = round((0.5 - rate / 2) * pixel.shape[0])
                        t = pixel.shape[0] - f
                    else:
                        f=round(pixel.shape[0]*f_t_rate[0])
                        t=round(pixel.shape[0]*f_t_rate[1])
                    while i < pixel.shape[1]:
                        vimin,vimax=pixel[f:t, i].min(),pixel[f:t, i].max()
                        if vimax-vimin<=pad_bias:
                            j = i + 1
                            vmins, vmaxs = [vimin], [vimax]
                            vms_min, vms_max = vimin, vimax
                            while j < pixel.shape[1]:
                                vmin,vmax=pixel[f:t, j].min(),pixel[f:t, j].max()
                                if vmax-vmin<=pad_bias:
                                    vmins.append(vmin)
                                    vmaxs.append(vmax)
                                    vms_min = min(vms_min, vmin)
                                    vms_max = max(vms_max, vmax)
                                    if vms_max-vms_min>pad_bias:
                                        if j-i>=pad_width:
                                            break
                                        while vms_max-vms_min>pad_bias:
                                            vmins.pop(0)
                                            vmaxs.pop(0)
                                            vms_min,vms_max=min(vmins),max(vmaxs)
                                            i=i+1
                                    j = j + 1
                                else:
                                    break
                            if j-i >= pad_width:
                                v_cuts.append((i, j))
                            i = j
                        i = i + 1

                if 'h' in oritention:
                    i = 0
                    if f_t_rate is None:
                        f = round((0.5 - rate / 2) * pixel.shape[1])
                        t = pixel.shape[1] - f
                    else:
                        f=round(pixel.shape[1]*f_t_rate[0])
                        t=round(pixel.shape[1]*f_t_rate[1])


                    while i < pixel.shape[0]:
                        vimin, vimax = pixel[i, f:t].min(), pixel[i, f:t].max()
                        if vimax - vimin <= pad_bias:

                            j = i + 1
                            vmins, vmaxs = [vimin], [vimax]
                            vms_min, vms_max = vimin, vimax
                            while j < pixel.shape[0]:
                                vmin, vmax = pixel[j, f:t].min(), pixel[j, f:t].max()

                                if vmax - vmin <= pad_bias:
                                    vmins.append(vmin)
                                    vmaxs.append(vmax)

                                    vms_min = min(vms_min, vmin)
                                    vms_max = max(vms_max, vmax)
                                    if vms_max - vms_min > pad_bias:
                                        if j-i>=pad_width:
                                            break
                                        while vms_max - vms_min > pad_bias:
                                            vmins.pop(0)
                                            vmaxs.pop(0)
                                            vms_min, vms_max = min(vmins), max(vmaxs)
                                            i=i+1
                                    j = j + 1
                                else:
                                    break
                            if j-i >= pad_width:
                                h_cuts.append((i, j))
                            i = j
                        i = i + 1
        else:
            if 'v' in oritention:
                i = 0
                while i<pixel.shape[1]:
                    #if np.logical_or.reduce([sum(pixel[:, i] >= l)>=Imgsize0 & sum(pixel[:, i] <= u)>=Imgsize0 for (l, u) in pad_values]):
                    if np.logical_or.reduce([sum((pixel[:, i] >= l) & (pixel[:, i] <= u))>=Imgsize0 for (l, u) in pad_values]):

                        j=i+1
                        #while j<pixel.shape[1] and np.logical_or.reduce([sum(pixel[:, j] >= l)>=Imgsize0 & sum(pixel[:, j] <= u)>=Imgsize0 for (l, u) in pad_values]):
                        while j<pixel.shape[1] and np.logical_or.reduce([sum((pixel[:, j] >= l) & (pixel[:, j] <= u))>=Imgsize0 for (l, u) in pad_values]):
                            j=j+1
                        if j-i>=pad_width:
                            v_cuts.append((i,j))
                        i=j

                    i=i+1

            if 'h' in oritention:
                i = 0
                while i<pixel.shape[0]:
                    #if np.logical_or.reduce([sum(pixel[i,:] >= l)>=Imgsize1 & sum(pixel[i,:] <= u)>=Imgsize1 for (l, u) in pad_values]):
                    if np.logical_or.reduce([sum((pixel[i,:] >= l) & (pixel[i,:] <= u))>=Imgsize1 for (l, u) in pad_values]):
                        j=i+1
                        #while j<pixel.shape[0] and np.logical_or.reduce([sum(pixel[j,:] >= l)>=Imgsize1 & sum(pixel[j,:] <= u)>=Imgsize1 for (l, u) in pad_values]):
                        while j<pixel.shape[0] and np.logical_or.reduce([sum((pixel[j,:] >= l) & (pixel[j,:] <= u))>=Imgsize1 for (l, u) in pad_values]):
                            j=j+1
                        if j-i>=pad_width:
                            h_cuts.append((i,j))
                        i=j
                    i=i+1

        if len(v_cuts)==0 and len(h_cuts)==0:
            print(img_name,'failed to located pad area!')
            #move(src_path,os.path.join(save_dir,'fail',os.path.basename(src_path)))
            continue

        v_cuts=[(0,pixel.shape[1])] if len(v_cuts)==0 else [(v2,v1) for (_,v2),(v1,_) in zip(v_cuts[:-1],v_cuts[1:])] if ignore_edge else ([(0, v_cuts[0][0])]+[(v2,v1) for (_,v2),(v1,_) in zip(v_cuts[:-1],v_cuts[1:])]+[(v_cuts[-1][1], pixel.shape[1])])

        h_cuts=[(0,pixel.shape[0])] if len(h_cuts)==0 else [(v2,v1) for (_,v2),(v1,_) in zip(h_cuts[:-1],h_cuts[1:])] if ignore_edge else ([(0, h_cuts[0][0]) ]+[(v2,v1) for (_,v2),(v1,_) in zip(h_cuts[:-1],h_cuts[1:])]+[(h_cuts[-1][1], pixel.shape[0])])


        min_shape_hv=(min_shape_hv[0] if min_shape_hv[0]>=1 else min_shape_hv[0]*pixel.shape[0],min_shape_hv[1] if min_shape_hv[1]>=1 else min_shape_hv[1]*pixel.shape[1])
        for v1,v2 in v_cuts:
            if v2-v1<min_shape_hv[1]:
                continue
            for h1,h2 in h_cuts:
                if h2-h1>=min_shape_hv[0]:
                    cv2.imwrite(os.path.join(save_dir, '%s-(%d,%d,%d,%d).%s' % (img_name, v1, h1, v2,h2, img_format)),image[h1:h2,v1:v2])
        if draw_rect:
            for h1,h2 in h_cuts:
                if h2-h1>=min_shape_hv[0]:
                    for v1,v2 in v_cuts:
                        if v2-v1>=min_shape_hv[1]:
                            cv2.rectangle(image,(v1,h2),(v2,h1),color=(0,0,255),thickness=6)

            cv2.imwrite(os.path.join(save_dir,os.path.basename(src_path)),image)


def de_watermark(src_path:str,save_dir:str=''):
    if save_dir=='':
        save_dir = os.getcwd()

    newpath = os.path.join(save_dir,'new_'+os.path.basename(src_path))
    img = cv2.imread(src_path, 1)
    # img.shape[:3] 则取彩色图片的高、宽、通道。
    hight, width, depth = img.shape[0:3]
    print(hight)
    print(width)
    # 裁剪水印坐标为[y0:y,x0:x1]
    cropped = img[int(hight * 0.9):hight, int(width * 0.7):width]
    cv2.imwrite(newpath, cropped)

    # 将图片加载为内存对象 参一：完整路径；参二：flag：-1彩色，0灰色，1原有
    imgsy = cv2.imread(newpath, 1)

    # 图片二值化处理，把[200,200,200]~[255, 255, 255]以外的颜色变成0
    # 这个颜色区间就是水印周边的背景颜色
    thresh = cv2.inRange(imgsy, np.array([28, 28, 28]), np.array([54, 54, 54]))
    # #创建形状和尺寸的结构元素 创建水印蒙层
    kernel = np.ones((3, 3), np.uint8)
    # 对水印蒙层进行膨胀操作
    hi_mask = cv2.dilate(thresh, kernel, iterations=10)
    specular = cv2.inpaint(imgsy, hi_mask, 5, flags=cv2.INPAINT_TELEA)
    cv2.imwrite(newpath, specular)

    # 覆盖图片
    imgsy = Image.open(newpath)
    img = Image.open(src_path)
    img.paste(imgsy, (int(width * 0.7), int(hight * 0.9), width, hight))
    img.save(newpath)

#de_watermark('img/3.jpg')

#split_img('img/1.jpg',h_cut=[0.5],v_cut=[0.5])

pad_split_cv2('2','outputs',oritention=['h'],pad_values=None,pad_width=8,pad_bias=8,formats=['jpg'],ignore_edge=False,min_shape_hv=(0.16,0.16),rate=0.96,draw_rect=False,save_format='png')
#pad_split_cv2('mop','outputs',oritention=['v'],pad_values=None,pad_width=8,pad_bias=8,formats=['png'],ignore_edge=False,min_shape_hv=(0.16,0.16),rate=0.94,draw_rect=False,save_format='png')

#pad_split_cv2('pop','outputs2',oritention=['h'],pad_values=None,pad_width=8,pad_bias=12,formats=['jpg'],ignore_edge=False,min_shape_hv=(0.16,0.16),rate=0.92,draw_rect=True,save_format='jpg')
#pad_split_cv2('pop','outputs',oritention=['h'],pad_values=None,pad_width=4,ignore_edge=False,min_shape_hv=(0.16,0.16),rate=0.92,draw_rect=True)