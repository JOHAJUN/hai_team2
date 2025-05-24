from Module.SpeakerTrackingRunner import run_speaker_tracking_on_folder

if __name__ == "__main__":
    input_dir = "Input"           # clip001.mp4 이 존재하는 폴더
    output_dir = "Output"         # 결과 clip001_labeled.avi 가 저장될 폴더
    talknet_path = "TalkNet-ASD"  # TalkNet 루트 경로

    run_speaker_tracking_on_folder(input_dir, output_dir, talknet_path)
