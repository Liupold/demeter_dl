import click
from dl_engine import HarvesterEngine
from tqdm import tqdm
from threading import _start_new_thread
from time import sleep
from os import get_terminal_size
from req_fn import toast

__version__ = 1.0


def display_handlers(self):
    sleep(1)
    print('\n\n')
    buff = self.done
    pbar = tqdm(total=self.size, unit_scale=1, unit='B',
                initial=buff, unit_divisor=1024)
    while not self.completed:
        done = self.done
        pbar.update(done - buff)
        buff = done
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


@click.command()
@click.option('--location', default='Downloads/', help='download location')
@click.option('--part_location', default='Downloads/Barn(Harvester storage)/',
              help='tmp location')
@click.option('--max_alive_at_once', default=8,
              help='Max thread to run in || during downloading')
@click.option('--no_of_parts', default=16,
              help='number of fragment the file is devided')
def cli(location, part_location, max_alive_at_once, no_of_parts):
    while True:
        try:
            url = input('URL-->')
            if 'https://www.youtube.com/watch?v=' == url[0:32] or'https://youtu.be/' == url[0:17]:
                url, yt_filename = yt_handler(url)
                print("Hang on Getting File Info")
                main_instance = HarvesterEngine(url, location=location,
                                                part_location=part_location,
                                                max_alive_at_once=max_alive_at_once,
                                                no_of_parts=no_of_parts,
                                                file_name=yt_filename)
            else:
                print("Hang on Getting File Info")
                main_instance = HarvesterEngine(url, location=location,
                                                part_location=part_location,
                                                max_alive_at_once=max_alive_at_once,
                                                no_of_parts=no_of_parts)
            print('\n\n')
            print(main_instance.Get_info())
            if main_instance.downloadable:
                _start_new_thread(display_handlers, (main_instance,))
                main_instance.Download()
            else:
                not_downloadable_handler(url)
            sleep(1)
            print('\n\n')
            print('\a')
            print('=' * get_terminal_size()[0])
            print('\n\n')
        except KeyboardInterrupt:
            print('\n')
            exit()


if __name__ == '__main__':
    print('-------------- Harvester ---------------')
    print('Version: {}'.format(__version__), 'Build with Python 3.6.5')
    print('Author: liupold @ github')
    print('Support: liupold@programmer.net')
    print('-----------------------------------------')
    print('\n\n')
    cli()
