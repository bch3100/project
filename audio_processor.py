import os
import librosa
import numpy as np

# 현재 디렉토리에서 모든 MP3 파일 찾기
audio_files = [f for f in os.listdir('.') if f.endswith('.mp3')]

if len(audio_files) < 2:
    print("현 디렉토리에는 2개의 음성파일이 존재해야 합니다")
else:
    audio_file1 = audio_files[0]
    audio_file2 = audio_files[1]

    # Librosa를 사용하여 두 오디오 파일 불러오기
    audio1, sr1 = librosa.load(audio_file1, sr=None)
    audio2, sr2 = librosa.load(audio_file2, sr=None)

    # 두 오디오 파일의 샘플링 레이트가 동일한지 확인
    if sr1 != sr2:
        print("두 오디오 파일의 샘플링 레이트가 다릅니다. 동일하게 변환해주세요.")
    else:
        # 두 오디오 신호의 길이를 동일하게 만들기 위해 짧은 쪽을 패딩 처리
        if len(audio1) > len(audio2):
            audio2 = np.pad(audio2, (0, len(audio1) - len(audio2)))
        elif len(audio2) > len(audio1):
            audio1 = np.pad(audio1, (0, len(audio2) - len(audio1)))

        # 두 오디오 신호를 합쳐서 오버레이하기
        combined = audio1 + audio2

        # 출력 경로 설정 (필요에 따라 변경 가능)
        output_path = r"C:\Users\USER\Desktop\opensource\project\Music\output.wav"

        # 결합된 오디오를 WAV 파일로 내보내기
        librosa.output.write_wav(output_path, combined, sr1)

        print(f"결합된 오디오가 다음 위치에 저장되었습니다: {output_path}")


