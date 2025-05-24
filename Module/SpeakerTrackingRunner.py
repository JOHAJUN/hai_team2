
import os
import subprocess
import glob

def run_speaker_tracking_on_folder(input_dir, output_dir, talknet_path="TalkNet-ASD"):
    """
    input_dir 내의 모든 clipXXX.mp4에 대해 TalkNet 화자 추적 실행하고,
    output_dir에 clipXXX_labeled.avi 형식으로 결과 저장
    """
    input_clips = sorted(glob.glob(os.path.join(input_dir, "clip*.mp4")))

    if not input_clips:
        print("❌ No input clips found in", input_dir)
        return

    for clip_path in input_clips:
        clip_name = os.path.splitext(os.path.basename(clip_path))[0]
        video_name = clip_name.replace("clip", "")  # 예: "001"

        print(f"🎬 Processing clip: {clip_name}")

        # TalkNet demo 폴더 생성
        target_path = os.path.join(talknet_path, "demo", f"{video_name}.mp4")
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        os.system(f"cp '{clip_path}' '{target_path}'")
        # TalkNet 실행
        cmd = f"cd {talknet_path} && python demoTalkNet.py --videoName {video_name}"
        subprocess.call(cmd, shell=True)

        # 결과 avi 복사
        result_path = os.path.join(talknet_path, "demo", video_name, "pyavi", "video_out_final.avi")
        output_path = os.path.join(output_dir, f"{clip_name}_labeled.avi")
        if os.path.exists(result_path):
            os.system(f"cp '{result_path}' '{output_path}'")
        else:
            print(f"⚠️ No output found for {clip_name}")

    print("✅ All speaker tracking completed.")
