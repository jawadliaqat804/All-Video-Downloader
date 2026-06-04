# --- Logic Data Saver 2: Required Modules ---
import os
import tempfile
import uuid
import threading
import subprocess
# Import the required modules for the proxy download
import requests
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import yt_dlp
import re

app = Flask(__name__)
# This allows our JS and Python to talk to each other
CORS(app)

@app.route('/')
def home():
    return "Mera Python Server Chal Raha Hai!"
# New Route: Force browser to download instead of playing
@app.route('/api/proxy_download')
def proxy_download():
    video_url = request.args.get('url')
    # 🔥 NEW: جاوا سکرپٹ سے ٹائٹل پکڑیں
    safe_title = request.args.get('title', 'video_download') 

    headers_req = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36'}
    req = requests.get(video_url, stream=True, headers=headers_req)

    if req.status_code != 200:
        req = requests.get(video_url, stream=True)

    if req.status_code != 200:
        return jsonify({"error": "Download blocked by source server. Try again."}), 400

    file_size = req.headers.get('content-length')
    # 🔥 NEW: ویڈیو کا اصلی نام لگا کر ڈاؤن لوڈ کروائیں
    headers = {'Content-Disposition': f'attachment; filename={safe_title}.mp4'}
    if file_size:
        headers['Content-Length'] = file_size

    return Response(stream_with_context(req.iter_content(chunk_size=1024)),
                    content_type=req.headers.get('content-type', 'video/mp4'),
                    headers=headers)
# This is our main API where JS will send the video URL
@app.route('/api/download', methods=['POST'])
def get_video_info():
    # Make sure these lines are indented with 4 spaces (Tab)
    data = request.get_json()
    video_url = data.get('url')

    # The IF block must be inside the function (indented at the same level)
    if not video_url:
        return jsonify({"error": "No URL provided!"}), 400

    # 🔥 MASTER NEW LOGIC (Third-Party API for TikTok ONLY)
    if 'tiktok.com' in video_url.lower():
        try:
            api_url = f"https://www.tikwm.com/api/?url={video_url}"
            res = requests.get(api_url).json()
            
            if res.get('code') == 0:
                tk_data = res.get('data', {})
                title = tk_data.get('title', 'TikTok Video')
                thumbnail = tk_data.get('cover')
                
                clean_formats = []
                
                # 1. Video - HD No Watermark
                if tk_data.get('hdplay'):
                    clean_formats.append({"label": "Video - HD No Watermark", "url": tk_data['hdplay']})
                # 2. Video - Normal No Watermark
                elif tk_data.get('play'):
                    clean_formats.append({"label": "Video - No Watermark", "url": tk_data['play']})
                
                # 3. Video - With Watermark
                if tk_data.get('wmplay'):
                    clean_formats.append({"label": "Video - With Watermark", "url": tk_data['wmplay']})
                    
                # 4. Audio Only
                if tk_data.get('music'):
                    clean_formats.append({"label": "Audio Only", "url": tk_data['music']})
                    
                return jsonify({
                    "success": True,
                    "title": title,
                    "thumbnail": thumbnail,
                    "formats": clean_formats
                })
            else:
                return jsonify({"error": "TikTok API Failed. Video might be private."}), 400
        except Exception as e:
            return jsonify({"error": f"TikTok API Error: {str(e)}"}), 500

    # 🛡️ PROTECTIVE SHIELD: YT, FB, Insta will continue to use yt-dlp smoothly below
    # Configure yt-dlp to only extract info, not download to laptop

    # Configure yt-dlp to only extract info, not download to laptop
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
       
        # Added Headers to fix Instagram "There is no video in this post" alert
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36',
            'Referer': 'https://www.tiktok.com/'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # --- LOGIC 7 (Part 1): The Smart Detective ---
            # 1. Gather all text (Title, Description, Tags, Category)
            title = (info.get('title') or "").lower()
            desc = (info.get('description') or "").lower()
            tags = " ".join(info.get('tags') or []).lower()
            categories = " ".join(info.get('categories') or []).lower()
            
            full_text = f"{title} {desc} {tags} {categories}"
          # 2. Ultra-Strict Blacklist (Ganda Content, Dramas, Web Series & Vulgarity)
            strict_blacklist = [
                'movie', 'bollywood', 'hollywood', 'lollywood', 'tollywood', 
                'indian drama', 'pakistani drama', 'web series', 'netflix', 'ullu', 
                'episode', 'trailer', 'teaser', 'romantic', 'kiss', 'hot', 'sexy', 
                'porn', '18+', 'nude', 'naked', 'adult', 'erotic', 'xxx', 'mms', 
                'leaked', 'desi hot', 'mujra', 'item song', 'thumka', 'turkish romance'
            ]
            for bad_word in strict_blacklist:
               if re.search(r'\b' + re.escape(bad_word) + r'\b', full_text):
                    # Logic 7: Emotional and Islamic Guideline Message
                    islamic_message = (
                        "Restricted Content Blocked!\n\n"
                        "Downloading movies, dramas, music, or inappropriate content goes against Islamic guidelines "
                        "and is strictly NOT ALLOWED on this platform. Please respect the purpose of this app.\n\n"
                        f"(System caught the keyword: '{bad_word}')"
                    )
                    return jsonify({"error": islamic_message})
            # 3. Music Check with Whitelist (Nasheed exceptions)
            music_words = ['music', 'song', 'bgm', 'instrumental', 'dance', 'dj', 'remix', 'mashup', 'cover', 'lofi', 'beats',  'reverb', 'choreography', 'choreo' 'twerk', 'soundtrack']
          # Optimized Whitelist using Global Titles
            whitelist = [
                'naat', 'nasheed', 'tilawat', 'quran', 'islamic', 'bayan', 
                'mufti', 'molvi', 'molana', 'maulana', 'qari', 'hafiz', 'sheikh', 'shaikh',
                'khutba', 'dua', 'hamd', 'hadees', 'hadith', 'tafseer',
                'vocal only', 'vocals only', 'no music', 'tasbeeh', 'dhikr', 'Farsi Noha', 'urdu noha', 'arabic nasheed', 'english nasheed', 'urdu nasheed', 'farsi nasheed', 'islamic nasheed', 'SoulFul Naats', 'Spiritual Nasheeds', 'Quran Recitation', 'Tilawat-e-Quran', 'Islamic Hamd', 'Hadees-e-Nabawi', 'Tafseer-e-Quran', 'No Music', 'Vocal Only', 'Vocals Only', 'urdu translations', 'farsi translations', 'arabic translations', 'english translations', 'islamic translations', 'quran translations', 'naat lyrics', 'nasheed lyrics', 'quran lyrics', 'islamic lyrics', 'hamd lyrics', 'hadees lyrics', 'tafseer lyrics', 'dua lyrics', 'dhikr lyrics', 'tasbeeh lyrics', 'azan', 'adhan', 'call to prayer', 'islamic call to prayer'
            ]
            # Check EXACT music words to avoid false alarms (like 'dance' in 'guidance')
            has_music = any(re.search(r'\b' + re.escape(m) + r'\b', full_text) for m in music_words)
            is_safe_nasheed = any(re.search(r'\b' + re.escape(w) + r'\b', full_text) for w in whitelist)
            
            # If it has music words BUT is NOT a nasheed/quran, block it!
            if has_music and not is_safe_nasheed:
                return jsonify({"error": "System Alert: Music/BGM Detected! Not allowed unless it is a 'Nasheed' or marked 'No Music'."})
            
           # --- If everything is clean, send data to JS ---
            # LOGIC 8: Collect formats & FIX TikTok/FB Corrupt Files / Max 2 Audios
            raw_formats = info.get('formats') or [info] # Fallback if formats array is missing
            clean_formats = []
            audio_count = 0 # STRICTLY max 2 audio formats
            best_direct_url = info.get('url') # Fallback direct URL if formats are missing
            
            for f in raw_formats:
                height = f.get('height')
                vcodec = f.get('vcodec', 'none')
                acodec = f.get('acodec', 'none')
                url = f.get('url')
                ext = f.get('ext', 'mp4')
                protocol = f.get('protocol', '')
                
                # 🔥 100% FIX for Corrupt File: Strictly block ALL non-http protocols (like m3u8 playlists)
                if protocol not in ['http', 'https']:
                    continue
                
                # --- LOGIC MASTERSTROKE: Get filesize and convert to MB ---
                filesize = f.get('filesize') or f.get('filesize_approx') or 0
                mb_size = round(filesize / (1024 * 1024), 1)
                size_tag = f" ({mb_size} MB)" if mb_size > 0 else ""
                
                if not url: continue
                
                label = ""
                # 🛡️ PROTECTIVE SHIELD: Identify if it is TikTok
                is_tiktok = 'tiktok' in (info.get('extractor') or '').lower()
                
                # 🔥 LOGIC FIX for Muted Video & TikTok Watermark Options!
                if vcodec != 'none' and acodec != 'none' and height and ext == 'mp4':
                    if is_tiktok:
                        # Only apply Watermark logic to TikTok
                        if 'watermark' in url.lower() or 'wm' in url.lower() or 'bytevc1' in url.lower():
                            label = f"Video - With Watermark{size_tag}"
                        else:
                            label = f"Video - No Watermark{size_tag}"
                    else:
                        # 🛡️ This keeps Facebook, Insta, and YouTube working EXACTLY as before!
                        label = f"Video - {height}p{size_tag}"
                # --- EXACTLY 2 AUDIO FORMATS ---
                elif acodec != 'none' and vcodec == 'none':
                    if audio_count < 2:
                        label = f"Audio Only{size_tag}"
                        audio_count += 1
                    else:
                        continue # Skip extra audios
                    
                # Add to list if not already added (to avoid clutter)
                if label and not any(d['label'] == label for d in clean_formats):
                    clean_formats.append({"label": label, "url": url})
            
            # 🔥 Fallback: If FB/Insta completely hid the formats, use the main direct video link
            if not any("Video" in d['label'] for d in clean_formats) and best_direct_url:
                clean_formats.append({"label": "Video - Best Quality", "url": best_direct_url})
                
            # Reverse list to show highest qualities at the top
            clean_formats.reverse()
            
            return jsonify({
                "success": True,
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "formats": clean_formats  # Sending the full quality menu to JS
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# --- LOGIC DATA SAVER 2 (BACKGROUND JOBS) ---
# ==========================================
compression_jobs = {}

def process_compression(job_id, video_url):
    # Set status to processing
    compression_jobs[job_id] = {'status': 'processing'}
    
    output_filename = f"compressed_{job_id}.mp4"
    output_path = os.path.join(tempfile.gettempdir(), output_filename)
    
    # 🔥 NEW IDEA 1: Outro Video Path (Assets Folder)
    outro_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'outro.mp4')
    
    # 🕵️ JASOOS LINE: Terminal path check
    print(f"\n🕵️ CHECKING PATH: {outro_path}") 
    
    try:
        # 🔥 SMART LOGIC: If outro exists, resize it to match the main video and merge them!
        if os.path.exists(outro_path):
            print("✅ OUTRO VIDEO FOUND! JORNA SHURU KAREIN!") # If file is found
            try:
                # Fixed: "Logic Kam Size" - Kept your exact video/logo layout untouched!
                # Only changed CRF to 34 (forces size down) and Preset to ultrafast (fixes the 3-minute delay).
                command = [
                    'ffmpeg', '-y', 
                    '-i', video_url, 
                    '-i', outro_path,
                    '-filter_complex', 
                    "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[main_v];"
                    "[1:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[outro_v];"
                    "[main_v][0:a][outro_v][1:a]concat=n=2:v=1:a=1[v][a]",
                    '-map', '[v]', '-map', '[a]',
                    '-vcodec', 'libx264', '-crf', '34', '-preset', 'ultrafast',
                    output_path
                ]
                subprocess.run(command, check=True, stderr=subprocess.PIPE)
                print("🎉 CONCAT SUCCESSFUL! VIDEO JUR GAYI!") 
                
            except subprocess.CalledProcessError as e:
                # Write error to text file so we can read it
                error_msg = e.stderr.decode('utf-8', errors='ignore')
                with open("ffmpeg_error.txt", "w", encoding="utf-8") as f:
                    f.write("FFMPEG ERROR:\n" + error_msg)
                
                # 🛡️ PROTECTIVE SHIELD
                command = [
                    'ffmpeg', '-y', '-i', video_url,
                    '-vcodec', 'libx264', '-crf', '28', '-preset', 'veryfast',
                    output_path
                ]
                subprocess.run(command, check=True)
        else:
            print("❌ OUTRO FILE MISSING! NORMAL COMPRESSION RUNNING.") # If file is missing
            # Normal compression if assets/outro.mp4 is missing
            command = [
                'ffmpeg', '-y', '-i', video_url,
                '-vcodec', 'libx264', '-crf', '28', '-preset', 'veryfast',
                output_path
            ]
            subprocess.run(command, check=True)
            
        final_size_bytes = os.path.getsize(output_path)
        final_size_mb = round(final_size_bytes / (1024 * 1024), 1)
        
        # Mark as completed and save the file path
        compression_jobs[job_id] = {
            'status': 'completed', 
            'file_path': output_filename,
            'final_mb': final_size_mb
        }
    except Exception as e:
        compression_jobs[job_id] = {'status': 'error', 'message': str(e)}


# Route 1: Start the compression job without freezing the server
@app.route('/api/start_compression', methods=['POST'])
def start_compression():
    data = request.get_json()
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400
        
    job_id = str(uuid.uuid4())
    
    # Start a background thread so the server doesn't hang!
    thread = threading.Thread(target=process_compression, args=(job_id, video_url))
    thread.start()
    
    return jsonify({"success": True, "job_id": job_id})

# Route 2: Check if the video is ready (Polling)
@app.route('/api/check_compression/<job_id>', methods=['GET'])
def check_compression(job_id):
    job = compression_jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)

# Route 3: Download the final compressed video
@app.route('/api/download_compressed/<filename>', methods=['GET'])
def download_compressed(filename):
    import os
    path = os.path.join(tempfile.gettempdir(), filename)
    
    def generate():
        with open(path, "rb") as f:
            while chunk := f.read(4096):
                yield chunk
                
    try:
        # Added Content-Length to force direct download without screen refresh
        file_size = os.path.getsize(path)
        headers = {
            'Content-Disposition': f'attachment; filename=DataSaver_{filename}',
            'Content-Length': str(file_size)
        }
        return Response(stream_with_context(generate()), content_type='video/mp4', headers=headers)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    # Bind to 0.0.0.0 and dynamic port so Render can expose the server to the internet
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
