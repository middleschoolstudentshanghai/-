from requests import get
from threading import Thread
from argparse import ArgumentParser
from os.path import join, basename, abspath, exists
from os import makedirs

def download_file(url, file_path, file_name):
    response = get(url, stream=True)
    full_path = join(file_path, file_name)
    with open(full_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

def multi_threaded_downloader(urls, num_threads, file_path, file_name):
    threads = []
    for url in urls:
        thread = Thread(target=download_file, args=(url, file_path, file_name or basename(url)))
        thread.start()
        threads.append(thread)

        # 等待指定数量的线程完成下载
        if len(threads) >= num_threads:
            for thread in threads:
                thread.join()
            threads = []

    # 等待剩余的线程完成下载
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    parser = ArgumentParser(description='多线程下载器')
    parser.add_argument('urls', nargs='+', help='待下载文件的URL列表')
    parser.add_argument('-n', '--num-threads', type=int, default=5, help='线程数量')
    parser.add_argument('-p', '--path', type=str, default='./', help='下载路径，默认为当前路径')
    parser.add_argument('-f', '--filename', type=str, help='下载文件名')

    args = parser.parse_args()

    # 指定下载文件名
    if args.filename:
        file_name = args.filename
    else:
        file_name = None

    # 获取默认下载路径
    default_path = abspath(args.path)

    # 创建下载路径
    if not exists(default_path):
        makedirs(default_path)

    # 调用多线程下载函数
    multi_threaded_downloader(args.urls, args.num_threads, default_path, file_name)
