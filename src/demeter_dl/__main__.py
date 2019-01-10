import click
from .Core import HarvesterEngine
from .Helper import LOG
from time import sleep
from os import get_terminal_size, environ, remove
from os.path import isfile
import os
import platform
import json
from colorama import init

init()


platform_name = platform.system()

art = """
██████╗ ███████╗███╗   ███╗███████╗████████╗███████╗██████╗    ██████╗ ██╗
██╔══██╗██╔════╝████╗ ████║██╔════╝╚══██╔══╝██╔════╝██╔══██╗   ██╔══██╗██║
██║  ██║█████╗  ██╔████╔██║█████╗     ██║   █████╗  ██████╔╝   ██║  ██║██║
██║  ██║██╔══╝  ██║╚██╔╝██║██╔══╝     ██║   ██╔══╝  ██╔══██╗   ██║  ██║██║
██████╔╝███████╗██║ ╚═╝ ██║███████╗   ██║   ███████╗██║  ██║   ██████╔╝███████╗
╚═════╝ ╚══════╝╚═╝     ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═════╝ ╚══════╝

                             ██╗    ██████╗    ██╗
                            ███║   ██╔═████╗  ███║
                            ╚██║   ██║██╔██║  ╚██║
                             ██║   ████╔╝██║   ██║
                             ██║██╗╚██████╔╝██╗██║
                             ╚═╝╚═╝ ╚═════╝ ╚═╝╚═╝

"""

__version__ = '1.0.1'
__url__ = 'https://github.com/Liupold/harvester'
# INDICATE VERSION AND BUILD, PREVENTS ERROR WITH CONFIG FILE
pbar = None
toast = LOG()


def generate_DownloadLocation():
    if platform_name == 'Windows':
        return environ['USERPROFILE'] + "/Downloads/"
    elif platform_name == 'Linux':
        return environ['HOME'] + "/Downloads/"
    else:
        return ""


def generate_PartLocation():
    if platform_name == 'Windows':
        return environ['LOCALAPPDATA'] + "/Barn(Harvester storage)/"
    elif platform_name == 'Linux':
        return environ['HOME'] + "/Barn(Harvester storage)/"
    else:
        return ""


def GenHomeLocation():
    if platform_name == 'Windows':
        return environ['USERPROFILE'] + "/Documents/"
    elif platform_name == 'Linux':
        return environ['HOME']
    else:
        return ""


def get_config(key, default_value):
    if isfile(GenHomeLocation() + 'demeter_dl.config.json'):
        with open(GenHomeLocation() + 'demeter_dl.config.json', 'r') as f:
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
            with open(GenHomeLocation() + 'demeter_dl.config.json', 'w') as f:
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
        with open(GenHomeLocation() + 'demeter_dl.config.json', 'w') as f:
            f.write(json_main_dict)
        return default_value


def display_handlers(self):
    sleep(1)
    print('\n\n')
    global pbar
    from tqdm import tqdm
    buff = self.done
    pbar = tqdm(total=self.size, unit_scale=1, unit='B',
                initial=buff, unit_divisor=1024)
    while (not self.completed) or (self.stoped):
        done = self.done
        pbar.update(done - buff)
        buff = done
    pbar.close()
    sleep(0.1)
    """
    print('\n\n')
    _initial = self.done
    widgets = [progressbar.Bar(marker="█", left="[", right="]", fill="░"),
               progressbar.Percentage(), " | ",
               progressbar.FileTransferSpeed(), " | ",
               progressbar.DataSize(), " | ",
               progressbar.ETA()]

    bar = progressbar.ProgressBar(
        widgets=widgets, maxval=self.size, initial_value=_initial).start()

    while (not self.completed) or (self.stoped):
        bar.update(self.done)
    bar.finish()
    """


def not_downloadable_handler(url):
    import webbrowser
    toast(1, 'File not download able or link expired')
    print('Open in web browser? (Y/N)')
    if input('').upper() == 'Y':
        toast(0, 'Opening in web browser')
        webbrowser.open(url)


def yt_handler(dl_link):
    from pafy import new as pafy_new
    global yt_obj
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
                _file_name = a_streams[int(sl_no) - 1].filename.split('.')

                _file_name[-2] += " ({})".format(
                    a_streams[int(sl_no) - 1].notes)

                filename = '.'.join(_file_name)
                return a_streams[int(sl_no) - 1].url,\
                    filename, 'A'
            except Exception as e:
                print('Try again!')

    if a_or_v.upper() == 'V':
        print('Enter The SERIAL of desired format And bitrate')
        v_streams = yt_obj.videostreams
        for sl_no, _stream in enumerate(v_streams, 1):
            print(str(sl_no) + ')', _stream, _stream.notes)
        while True:
            try:
                sl_no = input('Serial No: ')
                _file_name = v_streams[int(sl_no) - 1].filename.split('.')

                _file_name[-2] += " ({})".format(
                    v_streams[int(sl_no) - 1].notes)

                filename = '.'.join(_file_name)
                return v_streams[int(sl_no) - 1].url, \
                    filename, 'V'
            except Exception as e:
                print('Try again!')
                print(e)


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
            _type = None
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
            elif url == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                print('-------------- Harvester ---------------')
                print('Version: {}'.format(__version__),
                      'Build with Python 3.7.2')
                print('Author: liupold @ github')
                print('Support: liupold@programmer.net')
                print('-----------------------------------------\n\n\n')
            elif url == "":
                print('\n\n\a')
                print('=' * get_terminal_size()[0])
                print('\n\n')
            else:
                if 'https://www.youtube.com/watch?v=' == url[0:32]\
                        or 'https://youtu.be/' == url[0:17]:
                    url, yt_filename, _type = yt_handler(url)
                    print("Hang on Getting File Info")
                    if _type == 'V':
                        yt_filename = '__video__' + yt_filename
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
                    if _type == "V":
                        try:
                            main_instance.Download(False)
                        except FileExistsError as e:
                            print("Video File Exist")
                    else:
                        main_instance.Download(False)
                    display_handlers(main_instance)
                else:
                    not_downloadable_handler(url)

                if _type == 'V':
                    print('\n\n')
                    print("Getting Audio, pls wait.")
                    a_object = yt_obj.getbestaudio()
                    audio_url, audio_fiename = a_object.url, a_object.filename
                    audio_instance = \
                        HarvesterEngine(audio_url, location=location,
                                        part_location=part_location,
                                        max_alive_at_once=max_alive_at_once,
                                        no_of_parts=no_of_parts,
                                        file_name="__audio__" + audio_fiename)
                    try:
                        audio_instance.Download(False)
                    except FileExistsError:
                        print("Audio File Exists continuing....")
                    display_handlers(audio_instance)
                    print("Mixing Audio With Video PLS WAIT")
                    from .mixer import mix_av
                    if yt_filename.split('.')[-1].lower() == 'webm':
                        out_put_file_name = yt_filename[9::].replace(
                            '.webm', '.mkv')
                    else:
                        out_put_file_name = " " + yt_filename[9::]
                    mix_av(location + yt_filename,
                           location + "__audio__" + audio_fiename,
                           location + out_put_file_name)
                    remove(location + "__audio__" + audio_fiename)
                    remove(location + yt_filename)

                print('\n\n')
                print('\a')
                print('=' * get_terminal_size()[0])
                print('\n\n')
        except KeyboardInterrupt:
            if main_instance is not None:
                main_instance.Stop()
                pbar.close()
            else:
                quit()
            print('\n\n\a')
            print('=' * get_terminal_size()[0])
            print('\n\n')


if __name__ == '__main__':
    print('-------------- Harvester ---------------')
    print('Version: {}'.format(__version__), 'Build with Python 3.7.2')
    print('Author: liupold @ github')
    print('Support: liupold@programmer.net')
    print('-----------------------------------------')
    print('\n\n')
    cli()
