from platform import system

platform_name = system()


def mix_av(video_file, audio_file, output_file):

    from ffmpy import FFmpeg
    from subprocess import DEVNULL, STDOUT
    if platform_name == 'Linux':
        executable_path = 'mixer_bin/ffmpeg'
    elif platform_name == 'Windows':
        executable_path = 'mixer_bin/ffmpeg.exe'
    else:
        executable_path = "ffmpeg"
    ff = FFmpeg(
        executable=executable_path,
        inputs={video_file: None, audio_file: None},
        outputs={output_file: '-c copy -map 0:v:0  -map 1:a:0 -strict -2'}
    )
    ff.run(stdout=DEVNULL, stderr=STDOUT)
