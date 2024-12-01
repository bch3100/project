import subprocess
import os

# Voice 폴더 경로 설정
voice_folder = os.path.join(os.getcwd(), "voice")

# Voice 폴더 내의 mp3 파일 목록 가져오기
audio_files = [f for f in os.listdir(voice_folder) if f.endswith('.mp3')]

# 새로운 음성 파일 설정
if len(audio_files) < 1:
    print("voice 폴더에 최소 1개의 mp3 파일이 있어야 합니다.")
    exit()

input_audio = os.path.join(voice_folder, audio_files[0])
existing_audio = os.path.join(voice_folder, "existing_audio.mp3")

generated_audio = os.path.join(voice_folder, "generated_audio.mp3")

# 첫 번째 프로그램 실행 - 새로운 음성 파일 생성
subprocess.run(["python", "harmony_generator.py", input_audio, existing_audio, generated_audio])

# 두 번째 프로그램 실행 - 두 개의 음성 파일을 합치는 작업
combined_output = os.path.join(voice_folder, "output_combined.mp3")
subprocess.run(["python", "audio_processor.py", generated_audio, existing_audio, combined_output])
