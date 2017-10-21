import io
from google.cloud import speech
from google.cloud.speech import types
from pydub import AudioSegment
import subprocess
import os


def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    client = speech.SpeechClient()

    # [START migration_sync_request]
    # [START migration_audio_config_file]
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(language_code='en-US')
    # [END migration_audio_config_file]

    # [START migration_sync_response]
    response = client.recognize(config, audio)
    # [END migration_sync_request]
    # Print the first alternative of all the consecutive results.
    script = ''
    for result in response.results:
        script += result.alternatives[0].transcript + '\n'
        # print('Transcript: {}'.format(result.alternatives[0].transcript))
    return script


def prepare_audio_file(file_dir):
    # assuming mp3 type
    sound = AudioSegment.from_wav(file_dir + '.wav')
    sound = sound.set_channels(1)

    split_sound = []

    # NOTE: change implementation here to take into account pauses instead
    # so that it doesn't cut it off in the middle of a word
    # split sound into list of 60 second or less sound segments
    while len(sound) >= 60000:
        split_sound.append(sound[:59000])
        sound = sound[58000:]
    split_sound.append(sound)

    # save sound segments in a new folder
    for i, sound_segment in enumerate(split_sound):
        newpath = file_dir + '/sound_clips/'
        file_name = newpath + str(i) + '.wav'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        sound_segment.export(file_name, format='wav')


def transcript_from_video(video_file):
    file_dir = video_file.split(".")[0]
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}.wav".format(video_file, file_dir)
    subprocess.call(command, shell=True)

    prepare_audio_file(file_dir)

    audio_files = []
    for (dirpath, dirnames, filenames) in os.walk(file_dir + '/sound_clips'):
        audio_files.extend(filenames)

    transcript = ""
    for file in audio_files:
        transcript += transcribe_file(file_dir + '/sound_clips/' + file) + '\n'

    return transcript
