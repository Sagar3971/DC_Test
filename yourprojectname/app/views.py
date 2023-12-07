from django.shortcuts import render

# Create your views here.

def chatbot(request):
    return render(request, 'chatbot.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import wave

@csrf_exempt
def save_audio(request):
    if request.method == 'POST':
        audio_data = request.POST.get('audio_data')
        save_path = 'path/to/save/audio.wav'

        # Decode base64 and save the audio file
        audio_binary = base64.b64decode(audio_data)
        with open(save_path, 'wb') as audio_file:
            audio_file.write(audio_binary)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
