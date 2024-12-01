import os
import subprocess
from pydub import AudioSegment

# 두 개의 프로그램 파일 경로를 지정합니다.
FIRST_PROGRAM_PATH = './first_program.py'
SECOND_PROGRAM_PATH = './second_program.py'

# 음성 파일을 가져오는 함수입니다.
def get_audio_file():
    current_directory = os.getcwd()
    for file in os.listdir(current_directory):
        if file.endswith(".wav") or file.endswith(".mp3"):
            return os.path.join(current_directory, file)
    return None

def main():
    # 음성 파일을 찾습니다.
    audio_file = get_audio_file()
    if not audio_file:
        print("음성 파일을 찾을 수 없습니다. .wav 또는 .mp3 파일을 추가해주세요.")
        return

    # 첫 번째 프로그램 실행
    first_command = ['python', FIRST_PROGRAM_PATH, audio_file]
    try:
        first_result = subprocess.check_output(first_command, text=True).strip()
        print("첫 번째 프로그램 결과:", first_result)
    except subprocess.CalledProcessError as e:
        print("첫 번째 프로그램 실행 중 오류가 발생했습니다:", e)
        return

    # 두 번째 프로그램 실행
    second_command = ['python', SECOND_PROGRAM_PATH, audio_file, first_result]
    try:
        second_result = subprocess.check_output(second_command, text=True).strip()
        print("두 번째 프로그램 결과:", second_result)
    except subprocess.CalledProcessError as e:
        print("두 번째 프로그램 실행 중 오류가 발생했습니다:", e)
        return

    # 두 번째 결과를 mp3 파일로 저장합니다.
    output_audio = AudioSegment.from_file(audio_file)
    output_file_path = os.path.join(os.getcwd(), "second_result.mp3")
    output_audio.export(output_file_path, format="mp3")
    print(f"두 번째 결과를 {output_file_path}에 저장했습니다.")

if __name__ == "__main__":
    main()
