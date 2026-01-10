# READ THE YT VIDEO LINKS FROM A CSV FILE (dilmah_videos.csv)
# FOR EACH VIDEO, DOWNLOAD THE AUDIO USING YT-DLP
# TRANSCRIBE THE AUDIO USING GROQ WHISPER API
# SAVE THE TRANSCRIPTIONS TO A NEW CSV FILE (dilmah_videos_transcription.csv)

import os
import csv
import time
import yt_dlp
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def download_youtube_audio(url, output_dir="audio_files"):
    """Download audio from YouTube video and return the filename."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Simplified options - download best audio without conversion
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading audio from: {url}")
            info = ydl.extract_info(url, download=True)
            title = info['title']
            # After post-processing, the file will be .mp3
            filename = os.path.join(output_dir, f"{title}.mp3")
            
            # Check if file exists, if not try to find it
            if not os.path.exists(filename):
                import glob
                # List all mp3 files in the directory
                all_mp3s = glob.glob(os.path.join(output_dir, "*.mp3"))
                
                # Try to find by matching the base title (first part before colon)
                # This handles cases where YouTube uses different colon characters
                base_title = title.split(':')[0].strip() if ':' in title else title
                
                for mp3_file in all_mp3s:
                    mp3_basename = os.path.basename(mp3_file)
                    if base_title in mp3_basename and mp3_file not in [filename]:
                        filename = mp3_file
                        print(f"Found matching file: {filename}")
                        break
            
            if os.path.exists(filename):
                print(f"Audio downloaded: {filename}")
                return filename, title
            else:
                print(f"Warning: Could not find downloaded file")
                return None, None
                
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None, None

def transcribe_audio(filename):
    """Transcribe audio file using Groq Whisper API."""
    try:
        # Check if file exists
        if not os.path.exists(filename):
            print(f"Error: File not found: {filename}")
            # Try to find similar files
            import glob
            dir_path = os.path.dirname(filename)
            base_name = os.path.basename(filename)
            print(f"Looking for similar files in {dir_path}")
            all_files = glob.glob(os.path.join(dir_path, "*.mp3"))
            print(f"Available mp3 files: {all_files}")
            return None
        
        print(f"Transcribing: {filename}")
        
        # Check file size (Groq has a 25MB limit)
        file_size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f} MB")
        
        if file_size_mb > 25:
            print("Warning: File exceeds 25MB limit. Transcription may fail.")
        
        with open(filename, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(filename), file.read()),
                model="whisper-large-v3-turbo",
                temperature=0,
                response_format="verbose_json",
            )
        print("Transcription complete!")
        return transcription.text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def cleanup_audio_file(filename, keep_files=False):
    """Delete audio file after processing to save space."""
    if not keep_files and filename and os.path.exists(filename):
        try:
            os.remove(filename)
            print(f"Cleaned up: {filename}")
        except Exception as e:
            print(f"Could not delete file: {e}")

def process_videos(input_csv, output_csv, sleep_time=5, keep_audio_files=False):
    """Main pipeline to process all videos from CSV."""
    results = []
    
    # Read input CSV
    print(f"Reading input CSV: {input_csv}")
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        videos = list(reader)
    
    print(f"Found {len(videos)} videos to process\n")
    
    # Process each video
    for idx, row in enumerate(videos, 1):
        title = row['Video Title']
        url = row['Video URL']
        
        print(f"\n{'='*60}")
        print(f"Processing {idx}/{len(videos)}: {title}")
        print(f"{'='*60}")
        
        audio_file = None
        
        try:
            # Download audio
            audio_file, downloaded_title = download_youtube_audio(url)
            
            if audio_file and os.path.exists(audio_file):
                # Transcribe audio
                transcript = transcribe_audio(audio_file)
                
                if transcript:
                    results.append({
                        'Video Title': title,
                        'Video URL': url,
                        'Transcript': transcript,
                        'Status': 'Success'
                    })
                else:
                    results.append({
                        'Video Title': title,
                        'Video URL': url,
                        'Transcript': '',
                        'Status': 'Transcription Failed'
                    })
            else:
                results.append({
                    'Video Title': title,
                    'Video URL': url,
                    'Transcript': '',
                    'Status': 'Download Failed'
                })
        
        except Exception as e:
            print(f"Unexpected error processing video: {e}")
            results.append({
                'Video Title': title,
                'Video URL': url,
                'Transcript': '',
                'Status': f'Error: {str(e)}'
            })
        
        finally:
            # Clean up audio file unless we want to keep them
            cleanup_audio_file(audio_file, keep_audio_files)
        
        # Sleep between requests (except after the last one)
        if idx < len(videos):
            print(f"\nWaiting {sleep_time} seconds before next video...")
            time.sleep(sleep_time)
    
    # Save results to output CSV
    print(f"\n{'='*60}")
    print(f"Saving results to: {output_csv}")
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Video Title', 'Video URL', 'Transcript', 'Status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Processing complete! Results saved to {output_csv}")
    
    # Summary
    success_count = sum(1 for r in results if r['Status'] == 'Success')
    print(f"\nSummary:")
    print(f"Total videos: {len(videos)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(videos) - success_count}")

if __name__ == "__main__":
    # Configuration
    INPUT_CSV = "dilmah_videos.csv"
    OUTPUT_CSV = "dilmah_videos_transcription.csv"
    SLEEP_TIME = 5  # seconds between each video processing
    KEEP_AUDIO_FILES = False  # Set to True if you want to keep downloaded audio files
    
    # Run the pipeline
    process_videos(INPUT_CSV, OUTPUT_CSV, SLEEP_TIME, KEEP_AUDIO_FILES)