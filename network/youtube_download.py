from six.moves import urllib
import os
import sys
'''!wget https://yt-dl.org/downloads/latest/youtube-dl -O youtube-dl
!chmod a+rx youtube-dl'''

import os
import pandas as pd
import subprocess
from itertools import cycle
from multiprocessing import Pool
from tqdm.auto import tqdm

DEVNULL = open(os.devnull, 'wb')


def run(paras):
    download(*paras)


def download(video_id, youtube, video_folder):
    video_id = video_id.split('#')[0]
    video_path = os.path.join(video_folder, video_id + ".mp4")
    if os.path.exists(video_path):
        return
    subprocess.call([youtube, '-f', "''best/mp4''", '--write-auto-sub', '--write-sub',
                     '--sub-lang', 'en', '--skip-unavailable-fragments',
                     "https://www.youtube.com/watch?v=" + video_id, "--output",
                     video_path], stdout=DEVNULL, stderr=DEVNULL)
    return video_path


def load_video(metadata, video_folder, youtube, workers: int = 1):
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    df = pd.read_csv(metadata)
    pool = Pool(processes=8)
    youtubes = cycle([youtube])
    video_folders = cycle([video_folder])

    video_ids = set(df['video_id'])

    video_ids = set(list(video_ids)[294 + 95 + 289 + 8:])
    for chunks_data in tqdm(pool.imap_unordered(run, zip(video_ids, youtubes, video_folders))):
        pass


load_video('F:\\code\\Datasets\\Voxceleb/vox-metadata.csv',
           'video_folder',
           'F:\\code\\pretrained_model\\youtube-dl',8)