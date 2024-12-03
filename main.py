import os
import librosa
import numpy as np
import subprocess

# 두 개의 프로그램 파일 경로를 지정
FIRST_PROGRAM_PATH = './first_program.py'
SECOND_PROGRAM_PATH = './second_program.py'

# 폴더 내 오디오 파일 확보
def get_audio_file_from_folder(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(folder_path):
        print(f"폴더 {folder_name}가 존재하지 않습니다. 먼저 폴더를 생성하고 파일을 추가해주세요.")
        return None
    for file in os.listdir(folder_path):
        if file.endswith(".wav") or file.endswith(".mp3"):
            return os.path.join(folder_path, file)
    print(f"폴더 {folder_name}에 음성 파일이 없습니다. .wav 또는 .mp3 파일을 추가해주세요.")
    return None

def main():
    # MR 폴더에서 음성 파일 검색
    mr_audio_file = get_audio_file_from_folder("MR")
    if not mr_audio_file:
        return

    # VOCAL 폴더에서 음성 파일 검색
    vocal_audio_file = get_audio_file_from_folder("VOCAL")
    if not vocal_audio_file:
        return

    # 첫 번째 프로그램 실행
    first_command = ['python', FIRST_PROGRAM_PATH, mr_audio_file, vocal_audio_file]
    try:
        first_result = subprocess.check_output(first_command, text=True).strip()
    except subprocess.CalledProcessError as e:
        print("첫 번째 프로그램 실행 중 오류가 발생했습니다:", e)
        return

    # 두 번째 프로그램 실행 (현재 주석 처리, 필요시 활성화)
    # second_command = ['python', SECOND_PROGRAM_PATH, mr_audio_file, first_result]
    # try:
    #     second_result = subprocess.check_output(second_command, text=True).strip()
    # except subprocess.CalledProcessError as e:
    #     print("두 번째 프로그램 실행 중 오류가 발생했습니다:", e)
    #     return

    # 두 번째 결과를 wav 파일로 저장
    # Librosa를 사용하여 오디오 파일 불러오기
    # audio_data, sr = librosa.load(vocal_audio_file, sr=None)
    #
    # 출력 경로 설정
    # output_file_path = os.path.join(os.getcwd(), "second_result.wav")
    # librosa.output.write_wav(output_file_path, audio_data, sr)
    # print(f"두 번째 결과를 {output_file_path}에 저장했습니다.")

if __name__ == "__main__":
    main()

