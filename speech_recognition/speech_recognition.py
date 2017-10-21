import io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def transcribe_streaming(stream_file):
    """Streams transcription of the given audio file."""
    client = speech.SpeechClient()

    # [START migration_streaming_request]
    with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()

    # In practice, stream should be a generator yielding chunks of audio data.
    stream = [content]
    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')
    streaming_config = types.StreamingRecognitionConfig(config=config)

    # streaming_recognize returns a generator.
    # [START migration_streaming_response]
    responses = client.streaming_recognize(streaming_config, requests)
    # [END migration_streaming_request]

    for response in responses:
        for result in response.results:
            print('Finished: {}'.format(result.is_final))
            print('Stability: {}'.format(result.stability))
            alternatives = result.alternatives
            for alternative in alternatives:
                print('Confidence: {}'.format(alternative.confidence))
                print('Transcript: {}'.format(alternative.transcript))
    # [END migration_streaming_response]
# [END def_transcribe_streaming]


