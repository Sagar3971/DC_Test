import os
from django.core.files.storage import default_storage
import time
from google.cloud import speech_v1p1beta1 as speech
from django.shortcuts import render
from django.core.files.base import ContentFile
from google.cloud import speech
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# Load the Google Cloud credentials from the JSON key file
credentials_path = 'static/secretkey/speech_to_text.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


def chatbot(request):
    return render(request, 'chatbot.html')

def chatbot(request):
    return render(request, 'chatbot.html')

@csrf_exempt
def transcribe_audio(request):
    if request.method == 'POST':
        try:
            raw_audio = request.FILES.get('audio')
            print(raw_audio)
            client = speech.SpeechClient()
            path = default_storage.save('static/audiofile/file.wav', ContentFile(raw_audio.read()))
            print(path)
            print("this")
            time.sleep(3)

            with open(path, "rb") as audio_file:
                content = audio_file.read()

            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=48000,
                language_code="en-IN",
                model="latest_long",
                audio_channel_count=2,
                enable_word_confidence=True,
                enable_word_time_offsets=True,
            )

            response = client.recognize(config=config, audio=audio)

            # Each result is for a consecutive portion of the audio. Iterate through
            # them to get the transcripts for the entire audio file.
            for result in response.results:
                # The first alternative is the most likely one for this portion.
                print(f"Transcript: {result.alternatives[0].transcript}")

            return JsonResponse({'status': 'success', 'message': 'Transcription completed successfully'})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})