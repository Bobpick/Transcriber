import os
import tkinter as tk
from tkinter import filedialog
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from typing import List
import requests
import json

#version 1.0.0
def select_file() -> str:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a media file",
        filetypes=(("Media files", "*.mp4 *.mp3 *.mpeg *.wav"), ("All files", "*.*"))
    )
    return file_path

def extract_audio(file_path: str) -> str:
    filename, file_extension = os.path.splitext(file_path)
    audio_path = f"{filename}.wav"
    
    if file_extension.lower() in ('.mp4', '.mpeg'):
        with mp.VideoFileClip(file_path) as video:
            video.audio.write_audiofile(audio_path)
    elif file_extension.lower() == '.mp3':
        AudioSegment.from_mp3(file_path).export(audio_path, format="wav")
    elif file_extension.lower() == '.wav':
        return file_path  # Already in the correct format
    else:
        raise ValueError("Unsupported file format")
    
    return audio_path

def transcribe_audio(audio_path: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
def clean_transcription(text: str) -> str:
    prompt = f"""
    Enhance the following transcription for clarity, accuracy, and professional use:

    {text}

    Please perform the following tasks:

    1. Remove filler words (e.g., "um," "uh," "like"), false starts, and stutters.
    2. Correct any grammatical errors and misspellings.
    3. Clarify ambiguous phrases or complete any incomplete sentences while maintaining the original meaning.
    4. Ensure the transcription accurately reflects the spoken content without altering the core message.
    5. Improve overall readability and flow of the text.
    6. Format the text into coherent paragraphs if necessary.
    7. Retain any technical terms, proper nouns, or specific jargon relevant to the topic.

    Provide the enhanced transcription below, maintaining a professional tone suitable for formal documentation or publication.

    Enhanced transcription:
    """

    response = requests.post("http://localhost:11434/api/generate", 
                             json={
                                 "model": "llama2-uncensored:latest",
                                 "prompt": prompt,
                                 "stream": False
                             })
    
    if response.status_code == 200:
        result = response.json()
        return result['response'].strip()
    else:
        raise Exception(f"Error in Ollama API call: {response.status_code} - {response.text}")
def paginate_text(text: str, max_chars_per_page: int) -> List[str]:
    words = text.split()
    pages = []
    current_page = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= max_chars_per_page:
            current_page.append(word)
            current_length += len(word) + 1
        else:
            pages.append(' '.join(current_page))
            current_page = [word]
            current_length = len(word)
    
    if current_page:
        pages.append(' '.join(current_page))
    
    return pages

def save_as_pdf(pages: List[str], output_pdf_path: str):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    margin = inch
    font_size = 12
    line_height = font_size * 1.2
    max_lines_per_page = int((height - 2 * margin) / line_height)

    for page in pages:
        text_object = c.beginText(margin, height - margin)
        text_object.setFont("Helvetica", font_size)
        
        lines = page.split('\n')
        for line in lines[:max_lines_per_page]:
            text_object.textLine(line)
        
        c.drawText(text_object)
        c.showPage()
    
    c.save()

def main():
    media_file_path = select_file()
    if not media_file_path:
        print("No file selected")
        return
    
    try:
        audio_file_path = extract_audio(media_file_path)
        transcription = transcribe_audio(audio_file_path)
        
        print("Cleaning transcription...")
        cleaned_transcription = clean_transcription(transcription)
        
        max_chars_per_page = 2000  # Adjust based on estimated characters per page
        pages = paginate_text(cleaned_transcription, max_chars_per_page)
        output_pdf_path = f"{os.path.splitext(media_file_path)[0]}_cleaned.pdf"
        save_as_pdf(pages, output_pdf_path)
        print(f"Cleaned transcription saved to {output_pdf_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
