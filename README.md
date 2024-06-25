# Transcriber
Transcriber is a Python program that converts audio and video files into text, then utilizes AI via the Ollama LLM and an uncensored model to refine the transcription and save the cleaned output as a PDF.

## Features

- Supports various media formats (MP4, MP3, MPEG, WAV)
- Extracts audio from video files
- Transcribes audio using Google Speech Recognition
- Cleans up transcriptions using Ollama's llama2-uncensored model
- Generates a formatted PDF of the cleaned transcription

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- Ollama installed with the llama2-uncensored:latest model
- The following Python libraries:
  - moviepy
  - speech_recognition
  - pydub
  - reportlab
  - requests

## Installation
  1. Clone this repository:
   ```bash
   git clone [https://github.com/yourusername/transcriber.git](https://github.com/yourusername/transcriber.git)
   cd transcriber
```

  2. Install the required Python libraries:
```
pip install moviepy SpeechRecognition pydub reportlab requests
```
3. Ensure Ollama is installed and running with the llama2-uncensored:latest model.

## Usage

1. Run the script:
```
python transcriber.py
```
2. A file dialog will open. Select the media file you want to transcribe.

3. The program will process the file, transcribe the audio, clean up the transcription, and save it as a PDF.

4. The cleaned transcription PDF will be saved in the same directory as the original file, with "_cleaned" added to the filename.

## Configuration

You can adjust the following parameters in the `main()` function:

- `max_chars_per_page`: Maximum number of characters per page in the PDF output (default: 2000)

## Troubleshooting

- If you encounter issues with audio extraction, ensure you have the necessary codecs installed for moviepy.
- For transcription errors, check your internet connection, as Google Speech Recognition requires an internet connection.
- If the cleaning process fails, make sure Ollama is running and the llama2-uncensored:latest model is available.

## Contributing

Contributions to Transcriber are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
