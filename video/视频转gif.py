from PIL import Image
from moviepy.editor import *
def videoToGif(avi,outGif):
    clip=(VideoFileClip(avi))
    clip.write_gif(outGif)
    print("转换完成了")
def crop_gif_short(gif, gif_out, box):#box: crop box (left, up, right, down)
    im = Image.open(gif)
    frames = [im.crop(box) for frame in range(0, im.n_frames) if not im.seek(frame)]
    frames[0].save(gif_out, save_all=True, append_images=frames, loop=0, duration=im.info['duration'])
#crop_gif_short("output.gif", "output1.gif", (100,0,200,200))
videoToGif('video.avi','out.gif')