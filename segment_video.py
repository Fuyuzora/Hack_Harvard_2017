import cv2
import os
from pydub import AudioSegment
import subprocess
import io


def save_screenshots(vid_file):
    vidcap = cv2.VideoCapture(vid_file)
    success, image = vidcap.read()
    count = 0
    success = True
    while success:
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        cv2.imwrite("screenshots/time_%d.jpg" % count, image)  # save frame as JPEG file
        for i in range(20):
            success, image = vidcap.read()
        count += 1

    # can't find the time of each snapshot, but can at least find the total number of saves
    return count


def segment_sound(tot_frames, video_file):
    time_segments = []
    for (dirpath, dirnames, filenames) in os.walk('screenshots'):
        time_segments.extend(filenames)
    for i, time in enumerate(time_segments):
        time_segments[i] = int(time.split('.')[0].split('_')[-1])
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}.wav".format(video_file, video_file.split('.')[0])
    subprocess.call(command, shell=True)
    sound = AudioSegment.from_wav(video_file.split('.')[0] + '.wav')

    frame_time = int(len(sound) / tot_frames)

    sound_segments = []
    start = 0
    for time in time_segments:
        time *= frame_time
        sound_segments.append(sound[start:time])
        start = time
    sound_segments.append(sound[(time_segments[-1] * frame_time):])

    newpath = 'sound_segments/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for i, segment in enumerate(sound_segments):
        file_name = newpath + str(i) + '.wav'
        segment.export(file_name, format='wav')
