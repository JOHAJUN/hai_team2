from Module.YoutubeDownloader import download_youtube_video

def main():
    url = input("Enter YouTube video URL: ").strip()

    output_path = download_youtube_video(url)

    if output_path:
        print(f"\nDownload complete! Saved to: {output_path}")
    else:
        print("\nDownload or merge failed.")

if __name__ == "__main__":
    main()
