import os
import subprocess

# 첫 번째 및 두 번째 프로그램 파일 경로
FIRST_PROGRAM_PATH = os.path.join('.', 'harmony_generator.py')
SECOND_PROGRAM_PATH = os.path.join('.', 'sound_generator.py')

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

    # 첫 번째 프로그램 실행
    first_command = ['python', FIRST_PROGRAM_PATH, mr_audio_file]
    try:
        # 첫 번째 프로그램 실행 및 결과 문자열로 가져오기
        first_result = subprocess.check_output(first_command, text=True).strip()
        
        # 문자열 결과를 배열로 변환
        result_array = [item.strip() for item in first_result.split(',')]
        print("첫 번째 프로그램 결과 (배열):", result_array)
    except subprocess.CalledProcessError as e:
        print("첫 번째 프로그램 실행 중 오류가 발생했습니다:", e)
        return

    # 두 번째 프로그램 실행
    try:
        # 배열을 문자열로 변환하여 전달
        array_as_string = ','.join(result_array)
        second_command = ['python', SECOND_PROGRAM_PATH, mr_audio_file, array_as_string]
        
        # 두 번째 프로그램 실행
        subprocess.run(second_command)
    except subprocess.CalledProcessError as e:
        print("두 번째 프로그램 실행 중 오류가 발생했습니다:", e)
        return

if __name__ == "__main__":
    main()
