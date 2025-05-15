import os
from pytubefix import YouTube
import ffmpeg

def get_video_size(stream):
    return stream.filesize / (1024 * 1024)  # MB 단위로 변환

def download_youtube_video(url, save_dir='Input'):
    try:
        yt = YouTube(url)

        # 가장 해상도 높은 비디오 스트림 가져오기 (Adaptive 우선)
        video_streams = yt.streams.filter(type="video").order_by('resolution').desc()
        audio_stream = yt.streams.filter(only_audio=True).first()

        # 사용 가능한 비디오 스트림 출력
        print("Available video streams:")
        for i, stream in enumerate(video_streams):
            size = get_video_size(stream)
            stream_type = "Progressive" if stream.is_progressive else "Adaptive"
            print(f"{i}. Resolution: {stream.resolution}, Size: {size:.2f} MB, Type: {stream_type}")

        # 가장 첫 번째(해상도 높은) 스트림 선택
        selected_stream = video_streams[0]

        # 저장 디렉토리 없으면 생성
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        print(f"\n Downloading video: '{yt.title}' ...")
        video_file = selected_stream.download(output_path=save_dir, filename_prefix="video_")

        # Adaptive 스트림이면 오디오 따로 다운로드 후 병합
        if not selected_stream.is_progressive:
            print("Downloading audio stream...")
            audio_file = audio_stream.download(output_path=save_dir, filename_prefix="audio_")

            print("Merging video and audio...")
            output_file = os.path.join(save_dir, f"{yt.title}_merged.mp4")

            video_input = ffmpeg.input(video_file)
            audio_input = ffmpeg.input(audio_file)
            ffmpeg.output(video_input, audio_input, output_file,
                          vcodec='libx264', acodec='aac', strict='experimental').run(overwrite_output=True)

            # 병합 후 임시 파일 삭제
            os.remove(video_file)
            os.remove(audio_file)
        else:
            # Progressive면 바로 완료
            output_file = video_file

        print(f"Download and merge completed: {output_file}")
        return output_file

    except Exception as e:
        # 오류 발생 시 출력
        print(f"❌ Error occurred: {str(e)}")
        print("Please make sure pytube and ffmpeg are installed correctly.")
        return None

