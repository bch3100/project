import os
from pydub import AudioSegment

audio_files = [ f for f in os.listdir('.') if f.endswith('.mp3')]

if len(audio_files) < 2:
    print("현 디렉토리에는 2개의 음성파일이 존재해야 합니다")
else:      
    audio_file1 = audio_files[0]
    audio_file2 = audio_files[1]

    audio1 = AudioSegment.from_mp3(audio_file1)
    audio2 = AudioSegment.from_mp3(audio_file2)
    
    combined = audio1.overlay(audio2)

    output_path = r"C:\Users\USER\Desktop\opensource\project\Music\output.mp3"

    combined.export(output_path, format='mp3')
