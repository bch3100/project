import os
from pydub import AudioSegment

audio_files = [ f for f in os.listdir('.') if f,endswith('.mp3')]

if len(audio_files) < 2:
    print("현 디렉토리에는 2개의 음성파일이 존재해야 합니다")
else:      
    audio_file1 = audio_files[0]
    audio_file2 = audio_files[1]

    audio1 = Audiosegment.from_mp3(audio_file1)
    audio2 = Audiosegment.from_mp3(audio_file2)
    combined = audio1.overlay(audio2)

    output_file = " output.mp3"
    combined.export(output_file, format = 'mp3')
    
