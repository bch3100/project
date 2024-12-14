import subprocess

def run_programs():
    # 첫 번째 프로그램 실행
    subprocess.run(["python", "harmony_generator.py"])
    
    # 두 번째 프로그램 실행
    subprocess.run(["python", "sound.py"])

if __name__ == "__main__":
    run_programs()
