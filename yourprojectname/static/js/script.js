// Define DOM elements
const recordButton = document.getElementById('record-button');
const stopButton = document.getElementById('stop-button');
const messageEl = document.getElementById('message');

// Check browser support for audio recording
if (!navigator.mediaDevices.getUserMedia) {
  alert('Your browser does not support audio recording.');
  return;
}

// Start recording audio
recordButton.addEventListener('click', () => {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];

      // Capture audio data chunks
      mediaRecorder.addEventListener('dataavailable', event => {
        audioChunks.push(event.data);
      });

      // Update buttons
      recordButton.disabled = true;
      stopButton.disabled = false;

      // Stop recording after 3 seconds
      setTimeout(() => {
        mediaRecorder.stop();
      }, 3000);

      // Convert audio chunks to blob and send to Django backend
      mediaRecorder.onstop = function() {
        const blob = new Blob(audioChunks, { type: 'audio/ogg; codecs=opus' });
        const formData = new FormData();
        formData.append('audio', blob, 'recording.ogg');

        // Replace 'your_url' with your actual Django URL
        fetch('transcribe_audio', {
          method: 'POST',
          body: formData,
        })
          .then(response => response.json())
          .then(data => {
            messageEl.textContent = 'Audio uploaded successfully.';
            // Update buttons and message
            stopButton.disabled = true;
            recordButton.disabled = false;
          })
          .catch(error => {
            messageEl.textContent = 'Error uploading audio: ' + error;
          });
      };
    })
    .catch(error => {
      messageEl.textContent = 'Error accessing microphone: ' + error;
    });
});

// Stop recording audio
stopButton.addEventListener('click', () => {
  mediaRecorder.stop();
});
