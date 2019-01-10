def mix_av(video_file, audio_file, output_file):

    from ffmpy import FFmpeg
    from subprocess import DEVNULL, STDOUT
    ff = FFmpeg(
        inputs={video_file: None, audio_file: None},
        outputs={output_file: '-c copy -map 0:v:0  -map 1:a:0 -strict -2'}
    )
    ff.run(stdout=DEVNULL, stderr=STDOUT)
