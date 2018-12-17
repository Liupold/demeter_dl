import click
from harvester.Core import HarvesterEngine
from harvester.HarvesterHelper import LOG
import progressbar
from time import sleep
from os import get_terminal_size, environ
from os.path import isfile
import platform
import json
platform_name = platform.system()

art = """
                                                __   _____
|   |,---.                     |               /  | |  _  |
|---||---|,---..    ,,---.,---.|--- ,---.,---  `| | | |/' |
|   ||   ||     \  / |---'`---.|    |---'|      | | |  /| |
`   '`   '`      `'  `---'`---'`---'`---'`     _| |_\ |_/ /
                                               \___(_)___/
"""

__version__ = '1.0'
__url__ = 'https://github.com/Liupold/harvester'
# INDICATE VERSION AND BUILD, PREVENTS ERROR WITH CONFIG FILE

toast = LOG()


def generate_DownloadLocation():
    global __part_location, __download_location
    if platform_name == 'Windows':
        return environ['USERPROFILE'] + "/Downloads/"
    elif platform_name == 'Linux':
        return environ['HOME'] + "/Downloads/"
    else:
        return ""


def generate_PartLocation():
    global __part_location
    if platform_name == 'Windows':
        return environ['LOCALAPPDATA'] + "/Barn(Harvester storage)/"
    elif platform_name == 'Linux':
        return environ['HOME'] + "/Barn(Harvester storage)/"
    else:
        return ""


def get_config(key, default_value):
    if isfile('config.json'):
        with open('config.json', 'r') as f:
            data = f.read()

        if len(data) != "":
            main_dict = json.loads(data)
        else:
            main_dict = {}

        if key in main_dict:
            return main_dict[key]
        else:
            main_dict[key] = default_value
            json_main_dict = json.dumps(
                main_dict, sort_keys=True, indent=4)
            with open('config.json', 'w') as f:
                f.write(json_main_dict)
            return default_value

    else:
        toast(1, 'Regenerating config file')
        toast(1, 'Any change will be revert')
        toast(1, "THIS IS NORMAL FOR FIRST RUN")
        main_dict = {}
        main_dict[key] = default_value
        json_main_dict = json.dumps(
            main_dict, sort_keys=True, indent=4)
        with open('config.json', 'w') as f:
            f.write(json_main_dict)
        return default_value


def display_handlers(self):
    """sleep(1)
    print('\n\n')
    buff = self.done
    pbar = tqdm(total=self.size, unit_scale=1, unit='B',
                initial=buff, unit_divisor=1024)
    while (not self.completed) or (self.stoped):
        done = self.done
        pbar.update(done - buff)
        buff = done
    pbar.close()
    sleep(0.1)"""
    print('\n\n')
    _initial = self.done
    widgets = [progressbar.Bar(marker="#", left="[", right="]"),
               progressbar.Percentage(), " | ",
               progressbar.FileTransferSpeed(), " | ",
               progressbar.DataSize(), " | ",
               progressbar.ETA()]

    bar = progressbar.ProgressBar(
        widgets=widgets, maxval=self.size, initial_value=_initial).start()

    while (not self.completed) or (self.stoped):
        bar.update(self.done)
        sleep(0.0167)
    bar.finish()


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
                return a_streams[int(sl_no) - 1].url,\
                    a_streams[int(sl_no) - 1].filename
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
                return v_streams[int(sl_no) - 1].url, \
                    v_streams[int(sl_no) - 1].filename
            except Exception as e:
                print('Try again!')


DownloadLocation = get_config('Download Location', generate_DownloadLocation())
PartLocation = get_config('Part Location', generate_PartLocation())


@click.command()
@click.option('--location', default=DownloadLocation,
              help='download location')
@click.option('--part_location', default=PartLocation,
              help='tmp location')
@click.option('--max_alive_at_once', default=8,
              help='Max thread to run in || during downloading')
@click.option('--no_of_parts', default=16,
              help='number of fragment the file is devided')
def cli(location, part_location, max_alive_at_once, no_of_parts):
    while True:
        try:
            main_instance = None
            url = input('URL-->')
            if url == 'art':
                print(art)
                print('\n\n')
                print('\a')
                print('=' * get_terminal_size()[0])
                print('\n\n')
            elif url == 'about':
                print('Simple Harvester CLI by Rohn Chatterjee\
                    (writer of harvester)')
                print('\n\n')
                print('\a')
                print('=' * get_terminal_size()[0])
                print('\n\n')
            else:
                if 'https://www.youtube.com/watch?v=' == url[0:32]\
                        or 'https://youtu.be/' == url[0:17]:
                    url, yt_filename = yt_handler(url)
                    print("Hang on Getting File Info")
                    main_instance = \
                        HarvesterEngine(url, location=location,
                                        part_location=part_location,
                                        max_alive_at_once=max_alive_at_once,
                                        no_of_parts=no_of_parts,
                                        file_name=yt_filename)
                else:
                    print("Hang on Getting File Info")
                    main_instance = \
                        HarvesterEngine(url, location=location,
                                        part_location=part_location,
                                        max_alive_at_once=max_alive_at_once,
                                        no_of_parts=no_of_parts)
                print('\n\n')
                print(main_instance.Get_info())
                if main_instance.downloadable:
                    input("Press Enter to start Download or Crtl+C to exit")
                    main_instance.Download(False)
                    display_handlers(main_instance)
                else:
                    not_downloadable_handler(url)
                print('\n\n')
                print('\a')
                print('=' * get_terminal_size()[0])
                print('\n\n')
        except KeyboardInterrupt:
            print('\n')
            if main_instance is not None:
                main_instance.Stop()
            else:
                quit()
            print('\n\n\a')
            print('=' * get_terminal_size()[0])
            print('\n\n')


if __name__ == '__main__':
    print('-------------- Harvester ---------------')
    print('Version: {}'.format(__version__), 'Build with Python 3.6.5')
    print('Author: liupold @ github')
    print('Support: liupold@programmer.net')
    print('-----------------------------------------')
    print('\n\n')
    cli()
