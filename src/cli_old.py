from dl_engine import HarvesterEngine as OpenEngine
from threading import _start_new_thread
from time import sleep
from req_fn import toast, p_unit
from tqdm import tqdm
from os import get_terminal_size, mkdir
from os.path import isdir
# in CLI the pause and resume is not implemented
# for pausing use CRTL-C or exit the Download
# for resuming just start the download if resumable it will resume itself
__version__ = '0.2.1'
__dl_location__ = 'Downloads/'
if not isdir(__dl_location__):
    mkdir(__dl_location__)


def display_handlers(self):
    print('\n\n')
    sleep(0.2)
    buff = 0
    pbar = tqdm(total=self.size, unit_scale=1, unit='B',
                initial=self.done, unit_divisor=10024)
    while not self.completed:
        done = self.done
        pbar.update(done - buff)
        buff = done
        sleep(0.00167)
    pbar.close()
    sleep(0.1)


def not_downloadable_handler(url):
    import webbrowser
    toast(1, 'File not download able or link expired')
    print('Open in web browser? (Y/N)')
    if input('').upper() == 'Y':
        toast(0, 'Opening in web browser')
        webbrowser.open(url)


def yt_handler(dl_link):
    from pafy import new as pafy_new
    print('Hang tight checking Youtube For Your Video....!')
    yt_obj = pafy_new(dl_link)
    a_or_v = input('Audio/Video Enter A or V: ')
    if a_or_v.upper() == 'A':
        print('Enter The SERIAL of desired format And bitrate')
        a_streams = yt_obj.audiostreams
        for sl_no, _stream in enumerate(a_streams, 1):
            print(str(sl_no) + ')', _stream)
        while True:
            try:
                sl_no = input('Serial No: ')
                return a_streams[int(sl_no) - 1].url, a_streams[int(sl_no) - 1].filename
                break
            except Exception as e:
                print('Try again!')

    if a_or_v.upper() == 'V':
        print('Enter The SERIAL of desired format And bitrate')
        v_streams = yt_obj.streams
        for sl_no, _stream in enumerate(v_streams, 1):
            print(str(sl_no) + ')', _stream)
        while True:
            try:
                sl_no = input('Serial No: ')
                return v_streams[int(sl_no) - 1].url, v_streams[int(sl_no) - 1].filename
                break
            except Exception as e:
                print('Try again!')


if __name__ == '__main__':
    print('------------------ ODM ------------------')
    print('Version: {}'.format(__version__), 'Build with Python 3.6.5')
    print('Author: liupold @ github')
    print('Support: liupold@programmer.net')
    print('-----------------------------------------')
    while True:
        print('\n')
        dl_link = input('URL-->')
        if 'https://www.youtube.com/watch?v=' == dl_link[0:32]:
            dl_link, yt_filename = yt_handler(dl_link)
            main_instance = OpenEngine(dl_link)
            main_instance.location = __dl_location__
            main_instance.file_name = yt_filename
        else:
            main_instance = OpenEngine(dl_link)
            main_instance.location = __dl_location__
        if main_instance.downloadable:
            print('\n')
            print("File Name: {}".format(main_instance.file_name))
            print('File Size: {}'.format(p_unit(main_instance.size)))
            _user_input = input('Did we got that correct? (Y/N)')
            if _user_input.upper() == 'Y':
                _start_new_thread(display_handlers, (main_instance,))
                main_instance.Download()
        else:
            not_downloadable_handler(dl_link)
        print('\n')
        print('\a')
        print('=' * get_terminal_size()[0])
