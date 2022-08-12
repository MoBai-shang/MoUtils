from six.moves import urllib
import os
import sys

def download_and_extract(filepath, save_dir):
    """根据给定的URL地址下载文件
    Parameter:
        filepath: list 文件的URL路径地址
        save_dir: str  保存路径
    Return:
        None
    """
    for url, index in zip(filepath, range(len(filepath))):
        filename = url.split('/')[-1]
        save_path = os.path.join(save_dir, filename)
        urllib.request.urlretrieve(url, save_path)
        sys.stdout.write('\r>> Downloading %.1f%%' % (float(index + 1) / float(len(filepath)) * 100.0))
        sys.stdout.flush()
    print('\nSuccessfully downloaded')
#download_and_extract(["https://huggingface.co/clue/roberta_chinese_large/resolve/main/vocab.txt"],"")

def download2(url,save_file):
    import urllib2

    print("downloading with urllib2")
    f = urllib2.urlopen(url) 
    data = f.read() 
    with open(save_file, "wb") as code:     
        code.write(data)

def download3(url,save_file):
    import requests
    r = requests.get(url, stream=True)
    with open(save_file, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

