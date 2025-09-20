#!/usr/bin/env python3
# YouTube Audio Downloader for Audiophiles
# Enhanced with anti-detection measures
# Developed by 0xdev

import os
import subprocess
import sys
import time
import random
import yt_dlp as youtube_dl
from pathlib import Path
from urllib.parse import urlparse

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
    #############################################
    #      YouTube Audio Downloader by og0xdev  #
    #         Audiophile Edition v0.9           #
    #      Enhanced with Anti-Detection         #
    #############################################
    """
    print(banner)

def get_user_agents():
    #Return a list of realistic user agents to rotate through#
    return [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]

def get_ydl_options():
    #Return yt-dlp options with anti-detection measures#
    user_agent = random.choice(get_user_agents())
    
    return {
        'quiet': True,
        'no_warnings': False,
        'extract_flat': False,
        'user_agent': user_agent,
        'referer': 'https://www.youtube.com/',
        'socket_timeout': 30,
        'retries': 10,
        'fragment_retries': 10,
        'ignoreerrors': False,
        'force_ipv4': True,
        'geo_bypass': True,
        'geo_bypass_country': 'US',
        'http_headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        },
        # Simulate a real browser's behavior
        'throttledratelimit': 2048 * 2048,  # 4 MB/s
    }

def get_available_formats(url):
    #Retrieve available formats with anti-detection measures#
    ydl_opts = get_ydl_options()
    
    try:
        # Add random delay to simulate human behavior
        time.sleep(random.uniform(1, 3))
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            audio_formats = []
            
            for f in formats:
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    audio_format = {
                        'format_id': f['format_id'],
                        'ext': f['ext'],
                        'bitrate': f.get('abr', 0),
                        'format_note': f.get('format_note', ''),
                        'filesize': f.get('filesize', 0)
                    }
                    audio_formats.append(audio_format)
            
            # Sort by bitrate (highest first)
            audio_formats.sort(key=lambda x: x['bitrate'], reverse=True)
            return audio_formats, info
    except Exception as e:
        print(f"Error retrieving formats: {e}")
        print("This might be due to YouTube's bot detection. Trying again with different parameters...")
        return None, None

def download_audio(url, format_id, output_path="downloads"):
    #Download audio with anti-detection measures#
    Path(output_path).mkdir(exist_ok=True)
    
    ydl_opts = get_ydl_options()
    ydl_opts.update({
        'format': format_id,
        'outtmpl': f'{output_path}/%(title).100B.%(ext)s',
        'quiet': False,
        'no_warnings': False,
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'best',
            'preferredquality': '0',
        }],
        # Limit download speed to appear more human-like
        'ratelimit': 1024 * 1024,  # 1 MB/s
    })
    
    try:
        # Add random delay before download
        time.sleep(random.uniform(2, 5))
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Starting download...")
            ydl.download([url])
            print("Download completed successfully!")
    except Exception as e:
        print(f"Download error: {e}")
        print("If this persists, try again later or use a VPN.")

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d.get('_percent_str', 'N/A')} complete", end='\r')
    elif d['status'] == 'finished':
        print("\nPost-processing...")

def convert_audio(input_file, output_format):
    if not os.path.exists(input_file):
        print("File not found!")
        return False
    
    output_file = os.path.splitext(input_file)[0] + f'.{output_format}'
    
    try:
        cmd = [
            'ffmpeg', '-i', input_file,
            '-vn', '-ar', '44100', '-ac', '2', '-b:a', '320k',
            '-y', output_file
        ]
        
        subprocess.run(cmd, check=True)
        print(f"Conversion successful: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e}")
        return False
    except FileNotFoundError:
        print("FFmpeg not found. Please install FFmpeg to use conversion features.")
        return False

def validate_youtube_url(url):
    #Validate if the URL is a proper YouTube URL#
    parsed = urlparse(url)
    if not parsed.netloc:
        return False
        
    valid_domains = ['youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtu.be']
    if not any(domain in parsed.netloc for domain in valid_domains):
        return False
        
    return True

def single_download():
    url = input("Enter YouTube URL: ").strip()
    if not url or not validate_youtube_url(url):
        print("Invalid YouTube URL")
        return
    
    formats, info = get_available_formats(url)
    if not formats:
        print("No audio formats found or YouTube is blocking the request")
        print("Try again later or use a VPN")
        return
    
    print(f"\nAvailable audio formats for: {info.get('title', 'Unknown')}")
    print("Index | Format ID | Extension | Bitrate | Quality")
    print("-" * 50)
    
    for i, fmt in enumerate(formats, 1):
        print(f"{i:5} | {fmt['format_id']:9} | {fmt['ext']:9} | {fmt['bitrate']:7} | {fmt['format_note']}")
    
    try:
        choice = int(input("\nSelect format by index: "))
        if 1 <= choice <= len(formats):
            selected_format = formats[choice-1]['format_id']
            download_audio(url, selected_format)
        else:
            print("Invalid selection")
    except ValueError:
        print("Please enter a valid number")

def playlist_download():
    url = input("Enter YouTube playlist URL: ").strip()
    if not url or not validate_youtube_url(url):
        print("Invalid YouTube URL")
        return
    
    formats, info = get_available_formats(url)
    if not formats:
        print("No audio formats found or YouTube is blocking the request")
        print("Try again later or use a VPN")
        return
    
    print(f"\nPlaylist: {info.get('title', 'Unknown')}")
    print("Available audio formats:")
    print("Index | Format ID | Extension | Bitrate | Quality")
    print("-" * 50)
    
    for i, fmt in enumerate(formats[:5], 1):  # Show top 5 formats
        print(f"{i:5} | {fmt['format_id']:9} | {fmt['ext']:9} | {fmt['bitrate']:7} | {fmt['format_note']}")
    
    try:
        choice = int(input("\nSelect format by index: "))
        if 1 <= choice <= len(formats[:5]):
            selected_format = formats[choice-1]['format_id']
            
            ydl_opts = get_ydl_options()
            ydl_opts.update({
                'format': selected_format,
                'outtmpl': 'downloads/%(playlist_index)s - %(title)s.%(ext)s',
                'quiet': False,
                'no_warnings': False,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'best',
                }],
                # Add delay between playlist items to avoid detection
                'sleep_interval': random.randint(5, 15),
            })
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Starting playlist download...")
                ydl.download([url])
                print("Playlist download completed!")
        else:
            print("Invalid selection")
    except ValueError:
        print("Please enter a valid number")

def converter_menu():
    input_file = input("Enter input file path: ").strip()
    if not os.path.exists(input_file):
        print("File not found!")
        return
    
    print("\nAvailable output formats:")
    formats = ['mp3', 'flac', 'wav', 'aac', 'm4a', 'ogg']
    for i, fmt in enumerate(formats, 1):
        print(f"{i}. {fmt.upper()}")
    
    try:
        choice = int(input("\nSelect output format: "))
        if 1 <= choice <= len(formats):
            output_format = formats[choice-1]
            convert_audio(input_file, output_format)
        else:
            print("Invalid selection")
    except ValueError:
        print("Please enter a valid number")

def main_menu():
    while True:
        clear_screen()
        print_banner()
        print("Main Menu:")
        print("1. Single Audio Download (Highest Quality)")
        print("2. Playlist Download")
        print("3. Audio Format Converter")
        print("4. Exit")
        
        try:
            choice = int(input("\nSelect an option: "))
            
            if choice == 1:
                single_download()
            elif choice == 2:
                playlist_download()
            elif choice == 3:
                converter_menu()
            elif choice == 4:
                print("Thank you for using YouTube Audio Downloader by 0xdev!")
                break
            else:
                print("Invalid option. Please try again.")
            
            input("\nPress Enter to continue...")
            
        except ValueError:
            print("Please enter a valid number")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
