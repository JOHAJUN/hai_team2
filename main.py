from Module.YoutubeDownloader import download_youtube_video
from Module.Transcription import *

def main():
    url = input("Enter YouTube video URL: ").strip()

    merged_path, _, audio_path = download_youtube_video(url)

    if merged_path:
        print(f"\nDownload complete! Saved to: {merged_path}")
    else:
        print("\nDownload or merge failed.")
        
    print('\nTranscribing audio...')    
    transcription, audio = audio_transcribe(audio_path)
    save_transcript_json(transcription, audio)
    save_transcript_srt(transcription, audio)
    
    if transcription:
        print("\nTranscription complete!")
    else:
        print("\nTranscription failed.")
    
if __name__ == "__main__":
    main()
