# --- Logic Data Saver 2: Required Modules ---
import os
import tempfile
import uuid
import threading
import subprocess
# Import the required modules for the proxy download
import requests
# Import render_template for HTML and send_from_directory for CSS/JS files
from flask import Flask, request, jsonify, Response, stream_with_context, render_template, send_from_directory
from flask_cors import CORS
import yt_dlp
import re

# --- Proxy Rotation Setup ---
# You can add more public proxies here or use a service like BrightData/IPRoyal
PROXY_LIST = [
    {"http": "http://195.158.8.123:3128"},
      {"http": "http://117.236.124.166:3128"},
        {"http": "http://79.137.205.130:7443"},
          {"http": "http://138.124.113.102:7443"},
    # Add more proxies here to rotate
]

import random

def get_proxy():
    # If PROXY_LIST is empty, returns None (Direct connection)
    return random.choice(PROXY_LIST) if PROXY_LIST else None

# Configure Flask to look for templates in the current root directory (.)
app = Flask(__name__, template_folder=".")
# This allows our JS and Python to talk to each other
CORS(app)
compression_jobs = {}

@app.route('/')
def home():
    # Serve the main index.html file
    return render_template('index.html')

# Serve static files like style.css, script.js, and logo.png from the root directory
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# New Route: Force browser to download instead of playing
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

    # 🧹 UNIVERSAL SAFAI CHAT STRICT FILTER (GLOBAL LIST FOR ALL PLATFORMS) 🧹
    bad_words = ['movie', 'song', 'music', 'dance', 'mujra', 'kiss', 'hot', 'sexy', 'porn', '18+', 'nude', 'item song', 'viralsong','videosong', 'romantic', 'erotic', 'web series', 'drama', 'trailer', 'teaser', 'bollywood', 'hollywood', 'tollywood', 'lollywood', 'netflix', 'ullu', 'turkish romance', 'desi hot', 'mms', 'leaked', 'thumka', 'thumke', 'thumke ki', 'thumka ki', 'thumka laga ke', 'thumka lagake', 'choreography', 'choreo', 'twerk', 'soundtrack', 'remix', 'mashup', 'cover', 'lofi', 'beats', 'reverb', 'dailyvloger', 'songs', 'music video', 'full hd movie', 'full hd video', 'hd movie', 'hd video', 'full movie', 'full video', 'hd song', 'full hd song', 'hd music', 'full hd music', 'best song', 'best music', 'best video', 'best movie', 'new song', 'new music', 'new video', 'new movie', 'mashup', 'remix', 'cover', 'lofi', 'beats', 'reverb', 'videosong', 'stagedrama', ]
    if any(word in video_url.lower() for word in bad_words):
        return jsonify({"error": "System Alert: Restricted Content Blocked! (Safai Chat Rules)"})

    # 🔥 MASTER NEW LOGIC (Third-Party API for TikTok ONLY)
    if 'tiktok.com' in video_url.lower():
        try:
            api_url = f"https://www.tikwm.com/api/?url={video_url}"
            res = requests.get(api_url).json()
            
            if res.get('code') == 0:
                tk_data = res.get('data', {})
                title = tk_data.get('title', 'TikTok Video')
                
                # 🧹 DEEP SCAN: Check TikTok Title for Bad Words!
                if any(word in title.lower() for word in bad_words):
                    return jsonify({"error": "System Alert: Restricted Content Blocked! (Safai Chat Rules)"})
                    
                # 🔥 FIX: Thumbnail Fallback
                thumbnail = tk_data.get('cover') if tk_data.get('cover') else 'https://cdn-icons-png.flaticon.com/512/174/174855.png'
                
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
       # 🛡️ PROTECTIVE SHIELD: THE "API MAGIC" LAYER
    # Identifying the platform
    is_youtube = 'youtube.com' in video_url.lower() or 'youtu.be' in video_url.lower()
    is_facebook = 'facebook.com' in video_url.lower() or 'fb.watch' in video_url.lower() or 'fb.com' in video_url.lower()
    is_instagram = 'instagram.com' in video_url.lower()
    is_tiktok = 'tiktok.com' in video_url.lower()

    # 🚀 SHARED API CONFIGURATION (یہ سب کے لیے مشترکہ ہے)
    api_endpoints = [
        "https://api.cobalt.tools/api/json",
        "https://co.wuk.sh/api/json",
        "https://cobalt.qwyre.com/api/json"
    ]
    api_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    api_payload = {"url": video_url, "vQuality": "720", "filenamePattern": "classic"}

    # ==========================================
    # 🔴 LAYER 1: YOUTUBE API ONLY (صرف یوٹیوب کا بلاک)
    # ==========================================
    if is_youtube:
        for endpoint in api_endpoints:
            try:
                res = requests.post(endpoint, json=api_payload, headers=api_headers, timeout=15, proxies=get_proxy())
                if res.status_code == 200:
                    data = res.json()
                    title = data.get('title', '').lower()
                    if any(word in title for word in bad_words):
                        return jsonify({"error": "System Alert: Restricted Content Blocked! (Safai Chat Rules)"})
                    
                    direct_url = data.get('url')
                    if direct_url:
                        api_thumb = data.get('thumbnail')
                        thumb_url = api_thumb if api_thumb else 'https://cdn-icons-png.flaticon.com/512/1384/1384060.png'
                        formats = [{"label": "Video (720p/1080p) - Fast Download", "url": direct_url}]
                        
                        try:
                            audio_res = requests.post(endpoint, json={"url": video_url, "isAudioOnly": True}, headers=api_headers, timeout=10)
                            if audio_res.status_code == 200 and audio_res.json().get('url'):
                                formats.append({"label": "Audio Only (MP3)", "url": audio_res.json().get('url')})
                        except: pass
                        
                        return jsonify({"success": True, "title": title if title else "YouTube Video Ready!", "thumbnail": thumb_url, "formats": formats})
            except Exception as e: continue



    # ==========================================
    # 🔵 LAYER 2: FACEBOOK API ONLY (صرف فیس بک کا بلاک)
    # ==========================================
    elif is_facebook:
        for endpoint in api_endpoints:
            try:
                res = requests.post(endpoint, json=api_payload, headers=api_headers, timeout=15, proxies=get_proxy())
                if res.status_code == 200:
                    data = res.json()
                    title = data.get('title', '').lower()
                    if any(word in title for word in bad_words):
                        return jsonify({"error": "System Alert: Restricted Content Blocked! (Safai Chat Rules)"})
                    
                    direct_url = data.get('url')
                    if not direct_url and data.get('picker'): direct_url = data.get('picker')[0].get('url')
                    
                    if direct_url:
                        api_thumb = data.get('thumbnail')
                        thumb_url = api_thumb if api_thumb else 'https://cdn-icons-png.flaticon.com/512/124/124010.png'
                        formats = [{"label": "Video (720p/1080p) - Fast Download", "url": direct_url}]
                        
                        try:
                            audio_res = requests.post(endpoint, json={"url": video_url, "isAudioOnly": True}, headers=api_headers, timeout=10)
                            if audio_res.status_code == 200 and audio_res.json().get('url'):
                                formats.append({"label": "Audio Only (MP3)", "url": audio_res.json().get('url')})
                        except: pass
                        
                        return jsonify({"success": True, "title": title if title else "Facebook Video Ready!", "thumbnail": thumb_url, "formats": formats})
            except Exception as e: continue

    # ==========================================
    # 🟣 LAYER 3: INSTAGRAM API ONLY (صرف انسٹاگرام کا بلاک)
    # ==========================================
    elif is_instagram:
        for endpoint in api_endpoints:
            try:
                res = requests.post(endpoint, json=api_payload, headers=api_headers, timeout=15, proxies=get_proxy())
                if res.status_code == 200:
                    data = res.json()
                    title = data.get('title', '').lower()
                    if any(word in title for word in bad_words):
                        return jsonify({"error": "System Alert: Restricted Content Blocked! (Safai Chat Rules)"})
                    
                    direct_url = data.get('url')
                    if not direct_url and data.get('picker'): direct_url = data.get('picker')[0].get('url')
                    
                    if direct_url:
                        api_thumb = data.get('thumbnail')
                        # 🔥 FIX: Switched from DuckDuckGo to wsrv.nl proxy for better Instagram CDN bypass
                        import urllib.parse
                        encoded_thumb = urllib.parse.quote(api_thumb, safe='') if api_thumb else ''
                        thumb_url = f"https://wsrv.nl/?url={encoded_thumb}" if api_thumb else 'https://cdn-icons-png.flaticon.com/512/174/174855.png'
                        formats = [{"label": "Video (720p/1080p) - Fast Download", "url": direct_url}]
                        
                        try:
                            audio_res = requests.post(endpoint, json={"url": video_url, "isAudioOnly": True}, headers=api_headers, timeout=10)
                            if audio_res.status_code == 200 and audio_res.json().get('url'):
                                formats.append({"label": "Audio Only (MP3)", "url": audio_res.json().get('url')})
                        except: pass
                        
                        return jsonify({"success": True, "title": title if title else "Instagram Video Ready!", "thumbnail": thumb_url, "formats": formats})
            except Exception as e: continue
                
    
    ydl_opts = {
        'quiet': True,
        'skip_download': False, 
        'nocheckcertificate': True,
       
        'format': 'bestvideo+bestaudio/best', # This forces both streams to download
        'merge_output_format': 'mp4',        # This merges them automatically
        'cookiefile': 'cookies.txt',         # 🔥 FIX: Global Cookies for Private FB/Insta Videos
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', # 🔥 FIX: Bypass FB Parser Error
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate'
        }
    }
    # 1. 🔴 YOUTUBE LOGIC (NEW REVISED CLIENT BYPASS)
    if is_youtube:
        # 🔥 FIX: Re-enabled cookies to fix "Sign in to confirm you're not a bot" error
        ydl_opts['cookiefile'] = 'cookies.txt'
        # 🔥 FIX: Simplified format to safely grab both video and audio streams
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        # 🔥 FIX: Updated player clients to bypass bot detection safely (iOS works best currently)
        ydl_opts['extractor_args'] = {
            'youtube': {
                'player_client': ['ios', 'android', 'web']
            }
        }

    # 1. 🔵 FACEBOOK LOGIC (🔥 NEW ADVANCED AUDIO MERGE & BYPASS)
    if is_facebook:
        ydl_opts['cookiefile'] = 'cookies.txt' 
        # 🔥 FIX: Removed strict [ext=mp4] constraints so it downloads whatever stream is actually available
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        # 🔥 FIX: Removed 'api': 'none' which was causing the "Cannot parse data" crash
        ydl_opts['extractor_args'] = {
            'facebook': {}
        }
        # Force desktop headers to bypass mobile login walls
        ydl_opts['http_headers'].update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        })

    # 3. 🟣 INSTAGRAM LOGIC
    elif is_instagram:
        ydl_opts['cookiefile'] = 'cookies.txt' 
        ydl_opts['format'] = 'best[ext=mp4]/best'
        ydl_opts['extractor_args'] = {'instagram': {'query_comment_count': 0}}
        
    # 4. ⚫ TIKTOK LOGIC 
    elif is_tiktok:
        ydl_opts['http_headers']['Referer'] = 'https://www.tiktok.com/'
        ydl_opts['format'] = 'best'

    # 5. ⚪ OTHER PLATFORMS
    else:
        ydl_opts['format'] = 'best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # --- LOGIC 7 (Part 1): The Smart Detective ---
            title = (info.get('title') or "").lower()
            desc = (info.get('description') or "").lower()
            tags = " ".join(info.get('tags') or []).lower()
            categories = " ".join(info.get('categories') or []).lower()
            
            full_text = f"{title} {desc} {tags} {categories}"
           # 🔥 THE SMART RATIO SCANNER DEEP SCAN 🔥
            music_words = ['music', 'bgm', 'instrumental', 'dance', 'dj', 'remix', 'mashup', 'cover', 'lofi', 'beats', 'reverb', 'choreography', 'choreo', 'twerk', 'soundtrack']
            
            # Moved whitelist up so Python reads it before counting
            whitelist = [
                'naat', 'nasheed', 'tilawat', 'quran', 'islamic', 'bayan', 
                'mufti', 'molvi', 'molana', 'maulana', 'qari', 'hafiz', 'sheikh', 'shaikh',
                'khutba', 'dua', 'hamd', 'hadees', 'hadith', 'tafseer',
                'vocal only', 'vocals only', 'no music', 'tasbeeh', 'dhikr', 'azan', 'adhan', 'call to prayer',
                'tuaha ibn jalil', 'youth club', 'musfirahfamily', 'islamic tarana', 'jihaditarana', 'soulful naats', 'spiritual nasheeds'
            ]
            
            # 1. Count Safe Words (Naat aur Islami alfaaz ki ginti)
            safe_count = sum(full_text.count(w) for w in whitelist)
            title_safe_count = sum(title.count(w) for w in whitelist)
            total_safe_score = safe_count + (title_safe_count * 2) # Title wale lafz ko double power milegi

            # 2. Find and Count Bad/Music Words (Music wale alfaaz ki ginti aur nishandahi)
            found_bad_words = [b for b in bad_words + music_words if b in full_text]
            total_bad_score = sum(full_text.count(b) for b in bad_words + music_words)
            
            # 3. The Ratio Decision (Faisla)
            if total_bad_score > 0 and total_bad_score > total_safe_score:
                # Pakray gaye alfaaz ko comma (,) laga kar ek saath jorein taake user ko pata chale
                caught_words = ", ".join(found_bad_words[:3]) 
                
                islamic_message = (
                    "Restricted Content Blocked!\n\n"
                    "Downloading movies, dramas, music, or inappropriate content goes against Islamic guidelines "
                    "and is strictly NOT ALLOWED on this platform. Please respect the purpose of this app.\n\n"
                    f"(System caught the keyword: '{caught_words}')\n"
                    f"(Score Check: Bad={total_bad_score}, Safe={total_safe_score})"
                )
                return jsonify({"error": islamic_message})
            
            whitelist = [
                'naat', 'nasheed', 'tilawat', 'quran', 'islamic', 'bayan', 
                'mufti', 'molvi', 'molana', 'maulana', 'qari', 'hafiz', 'sheikh', 'shaikh',
                'khutba', 'dua', 'hamd', 'hadees', 'hadith', 'tafseer',
                'vocal only', 'vocals only', 'no music', 'tasbeeh', 'dhikr', 'Farsi Noha', 'urdu noha', 'arabic nasheed', 'english nasheed', 'urdu nasheed', 'farsi nasheed', 'islamic nasheed', 'SoulFul Naats', 'Spiritual Nasheeds', 'Quran Recitation', 'Tilawat-e-Quran', 'Islamic Hamd', 'Hadees-e-Nabawi', 'Tafseer-e-Quran', 'No Music', 'Vocal Only', 'Vocals Only', 'urdu translations', 'farsi translations', 'arabic translations', 'english translations', 'islamic translations', 'quran translations', 'naat lyrics', 'nasheed lyrics', 'quran lyrics', 'islamic lyrics', 'hamd lyrics', 'hadees lyrics', 'tafseer lyrics', 'dua lyrics', 'dhikr lyrics', 'tasbeeh lyrics', 'azan', 'adhan', 'call to prayer', 'islamic call to prayer', 'islamic azan', 'islamic adhan', 'quran recitation', 'tilawat-e-quran', 'hamd', 'hadees-e-nabawi', 'tafseer-e-quran', 'arshad Reels', 'misha bashir Reels', 'misha bashir shorts', 'soulful naats', 'spiritual nasheeds', 'quran recitation', 'tilawat-e-quran', 'islamic hamd', 'hadees-e-nabawi', 'tafseer-e-quran', 'tuaha ibn jalil', 'youth club', 'islamic youth club', 'islamic lectures for youth', 'islamic videos for youth', 'youth islamic videos', 'youth islamic lectures', 'musfirahfamily', 'islamic tarana', 'jihaditarana', 'islamic tarana'
            ]
            
            has_music = any(re.search(r'\b' + re.escape(m) + r'\b', full_text) for m in music_words)
            is_safe_nasheed = any(re.search(r'\b' + re.escape(w) + r'\b', full_text) for w in whitelist)
            
            if has_music and not is_safe_nasheed:
                return jsonify({"error": "System Alert: Music/BGM Detected! Not allowed unless it is a 'Nasheed' or marked 'No Music'."})
            
            # --- If everything is clean, send data to JS ---
            raw_formats = info.get('formats') or [info] 
            clean_formats = []
            audio_count = 0 
            best_direct_url = info.get('url')
            
            best_thumbnail = info.get('thumbnail')
            if info.get('thumbnails'):
                best_thumbnail = info['thumbnails'][-1]['url'] 
                
            # 🔥 INSTA THUMBNAIL MAGIC (yt-dlp fallback ke liye proxy)
            if is_instagram and best_thumbnail and 'http' in best_thumbnail:
                # 🔥 FIX: Switched to wsrv.nl proxy for reliable Instagram thumbnail loading
                import urllib.parse
                encoded_thumb = urllib.parse.quote(best_thumbnail, safe='')
                best_thumbnail = f"https://wsrv.nl/?url={encoded_thumb}"
                
            # 🔥 FIX: Fallback for missing Instagram/FB Thumbnails
            if not best_thumbnail or best_thumbnail == '':
                if is_instagram:
                    best_thumbnail = 'https://cdn-icons-png.flaticon.com/512/174/174855.png' # Insta Logo
                elif is_facebook:
                    best_thumbnail = 'https://cdn-icons-png.flaticon.com/512/124/124010.png' # FB Logo
                else:
                    best_thumbnail = 'https://cdn-icons-png.flaticon.com/512/4211/4211158.png' # Default Video Icon

            for f in raw_formats:
                height = f.get('height') or 'HD'
                vcodec = f.get('vcodec', 'none')
                acodec = f.get('acodec', 'none')
                url = f.get('url')
                ext = f.get('ext', 'mp4')
                protocol = f.get('protocol', '')
                
                # 🔥 REVISED PROTOCOL FILTER (FB Dash segments fix)
                if protocol not in ['http', 'https', 'm3u8', 'm3u8_native', 'dash', 'dashy', 'dash_native', 'http_dash_segments']:
                    continue
                
                filesize = f.get('filesize') or f.get('filesize_approx') or 0
                mb_size = round(filesize / (1024 * 1024), 1)
                size_tag = f" ({mb_size} MB)" if mb_size > 0 else ""
                
                if not url: continue
                
                label = ""
                is_tiktok = 'tiktok' in (info.get('extractor') or '').lower()
                
                # Treat as video if vcodec exists
                if vcodec != 'none':
                    if is_tiktok:
                        if 'watermark' in url.lower() or 'wm' in url.lower() or 'bytevc1' in url.lower():
                            label = f"Video - With Watermark{size_tag}"
                        else:
                            label = f"Video - No Watermark{size_tag}"
                    else:
                         # 🔥 FIX: Explicitly label Mute vs Audio videos for Facebook/YouTube!
                        if acodec == 'none':
                            continue  # Completely remove Mute videos from the list
                        else:
                            label = f"Video - {height}p{size_tag} (With Audio)"
                
                # Max 2 Audio formats
                elif acodec != 'none' and vcodec == 'none':
                    if audio_count < 2:
                        
                        label = f"Audio Only{size_tag}"
                        audio_count += 1
                    else:
                        continue 
                    
                if label and not any(d['label'] == label for d in clean_formats):
                    clean_formats.append({"label": label, "url": url})
            
            if best_direct_url:
                mb_size_best = round((info.get('filesize') or info.get('filesize_approx') or 0) / (1024 * 1024), 1)
                size_tag_best = f" ({mb_size_best} MB)" if mb_size_best > 0 else ""
                # 🔥 FIX: Dynamically fetching exact resolution for the Best Quality label
                best_height = info.get('height') or 'HD'
                if not any(d['url'] == best_direct_url for d in clean_formats):
                    clean_formats.append({"label": f"Video ({best_height}p){size_tag_best}", "url": best_direct_url})
            
            clean_formats.reverse()
            
            return jsonify({
                "success": True,
                "title": info.get('title') or "Downloaded Video",
                "thumbnail": best_thumbnail, 
                "formats": clean_formats  
            })
    except Exception as e:
        error_msg = str(e)
        if "Empty media response" in error_msg or "Private video" in error_msg:
            return jsonify({"error": "System Alert: Instagram Privacy Block! This video is private or restricted by Instagram. Please try a public reel."}), 400
        return jsonify({"error": error_msg}), 500

def process_compression(job_id, video_url):
    # Set status to processing
    compression_jobs[job_id] = {'status': 'processing'}
    
    output_filename = f"compressed_{job_id}.mp4"
    output_path = os.path.join(tempfile.gettempdir(), output_filename)
    
    # 🔥 NEW IDEA 1: Outro Video Path (Root Folder)
    outro_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outro.mp4')
    
    # 🕵️ JASOOS LINE: Terminal path check
    print(f"\n🕵️ CHECKING PATH: {outro_path}") 
    
    try:
        # Check if video has video stream
        try:
            probe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_type', '-of', 'default=noprint_wrappers=1:nokey=1', video_url]
            has_video = subprocess.check_output(probe_cmd).decode('utf-8').strip() == 'video'
        except:
            has_video = False

        # 🔥 SMART LOGIC: If outro exists, resize it to match the main video and merge them!
        if has_video and os.path.exists(outro_path):
            print("✅ OUTRO VIDEO FOUND! JORNA SHURU KAREIN!") # If file is found
            try:
                # 🔥 STRICT FFMPEG LOGIC: Forcing exact Aspect Ratio and Audio Rates before merging
                command = [
                    'ffmpeg', '-y', 
                    '-i', video_url, 
                    '-i', outro_path,
                    '-filter_complex', 
                    "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1:1,fps=30[main_v];"
                    "[1:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1:1,fps=30[outro_v];"
                    "[0:a]aformat=sample_rates=44100:channel_layouts=stereo[main_a];"
                    "[1:a]aformat=sample_rates=44100:channel_layouts=stereo[outro_a];"
                    "[main_v][main_a][outro_v][outro_a]concat=n=2:v=1:a=1[v][a]",
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
            print("❌ OUTRO FILE MISSING OR AUDIO ONLY! NORMAL COMPRESSION RUNNING.") 
            # Normal compression if assets/outro.mp4 is missing or it's just an audio file
            if has_video:
                command = [
                    'ffmpeg', '-y', '-i', video_url,
                    '-vcodec', 'libx264', '-crf', '28', '-preset', 'veryfast',
                    output_path
                ]
            else:
                command = ['ffmpeg', '-y', '-i', video_url, '-c', 'copy', output_path]
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