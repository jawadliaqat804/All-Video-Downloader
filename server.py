# --- Logic Data Saver 2: Required Modules ---
import os
import tempfile
import uuid
import threading
import subprocess
import requests
from flask import Flask, request, jsonify, Response, stream_with_context, render_template, send_from_directory
from flask_cors import CORS
import yt_dlp
import re
import random

# --- Proxy Rotation Setup ---
PROXY_LIST = [
    {"http": "http://195.158.8.123:3128"},
    {"http": "http://117.236.124.166:3128"},
    {"http": "http://79.137.205.130:7443"},
    {"http": "http://138.124.113.102:7443"},
]

def get_proxy():
    return random.choice(PROXY_LIST) if PROXY_LIST else None

app = Flask(__name__, template_folder=".")
CORS(app)
compression_jobs = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/proxy_download')
def proxy_download():
    video_url = request.args.get('url')
    safe_title = request.args.get('title', 'video_download') 

    headers_req = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36'}
    req = requests.get(video_url, stream=True, headers=headers_req)

    if req.status_code != 200:
        req = requests.get(video_url, stream=True)

    if req.status_code != 200:
        return jsonify({"error": "Download blocked by source server. Try again."}), 400

    file_size = req.headers.get('content-length')
    headers = {'Content-Disposition': f'attachment; filename={safe_title}.mp4'}
    if file_size:
        headers['Content-Length'] = file_size

    return Response(stream_with_context(req.iter_content(chunk_size=1024)),
                    content_type=req.headers.get('content-type', 'video/mp4'),
                    headers=headers)

@app.route('/api/download', methods=['POST'])
def get_video_info():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({"error": "No URL provided!"}), 400

    # 🧹 UNIVERSAL SAFAI CHAT STRICT FILTER 🧹
    bad_words = ['movie', 'song', 'music', 'dance', 'mujra', 'kiss', 'hot', 'sexy', 'porn', '18+', 'nude', 'item song', 'viralsong','videosong', 'romantic', 'erotic', 'web series', 'drama', 'trailer', 'teaser', 'bollywood', 'hollywood', 'tollywood', 'lollywood', 'netflix', 'ullu', 'turkish romance', 'desi hot', 'mms', 'leaked', 'thumka', 'thumke', 'thumke ki', 'thumka ki', 'thumka laga ke', 'thumka lagake', 'choreography', 'choreo', 'twerk', 'soundtrack', 'remix', 'mashup', 'cover', 'lofi', 'beats', 'reverb', 'dailyvloger', 'songs', 'music video', 'full hd movie', 'full hd video', 'hd movie', 'hd video', 'full movie', 'full video', 'hd song', 'full hd song', 'hd music', 'full hd music', 'best song', 'best music', 'best video', 'best movie', 'new song', 'new music', 'new video', 'new movie', 'mashup', 'remix', 'cover', 'lofi', 'beats', 'reverb', 'videosong', 'stagedrama']
    if any(word in video_url.lower() for word in bad_words):
        return jsonify({"error": "System Alert: Restricted Content Blocked! (Safai Chat Rules)"})

    # Identifying the platform
    is_youtube = 'youtube.com' in video_url.lower() or 'youtu.be' in video_url.lower()
    is_facebook = 'facebook.com' in video_url.lower() or 'fb.watch' in video_url.lower() or 'fb.com' in video_url.lower()
    is_instagram = 'instagram.com' in video_url.lower()
    is_tiktok = 'tiktok.com' in video_url.lower()

    # 🚀 SHARED COBALT API CONFIGURATION (For Facebook/Instagram Backup)
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
    # 🔥 MASTER NEW LOGIC (TikTok ONLY)
    # ==========================================
    if is_tiktok:
        try:
            api_url = f"https://www.tikwm.com/api/?url={video_url}"
            res = requests.get(api_url).json()
            if res.get('code') == 0:
                tk_data = res.get('data', {})
                title = tk_data.get('title', 'TikTok Video')
                if any(word in title.lower() for word in bad_words):
                    return jsonify({"error": "System Alert: Restricted Content Blocked! (Safai Chat Rules)"})
                thumbnail = tk_data.get('cover') if tk_data.get('cover') else 'https://cdn-icons-png.flaticon.com/512/174/174855.png'
                clean_formats = []
                if tk_data.get('hdplay'):
                    clean_formats.append({"label": "Video - HD No Watermark", "url": tk_data['hdplay']})
                elif tk_data.get('play'):
                    clean_formats.append({"label": "Video - No Watermark", "url": tk_data['play']})
                if tk_data.get('wmplay'):
                    clean_formats.append({"label": "Video - With Watermark", "url": tk_data['wmplay']})
                if tk_data.get('music'):
                    clean_formats.append({"label": "Audio Only", "url": tk_data['music']})
                return jsonify({"success": True, "title": title, "thumbnail": thumbnail, "formats": clean_formats})
            else:
                return jsonify({"error": "TikTok API Failed. Video might be private."}), 400
        except Exception as e:
            return jsonify({"error": f"TikTok API Error: {str(e)}"}), 500

    # ==========================================
    # 🔴 LAYER 1: YOUTUBE API (🔥 RAPID-API MAIN BYPASS)
    # ==========================================
    elif is_youtube:
        try:
            video_id = None
            if "v=" in video_url:
                video_id = video_url.split("v=")[1][:11]
            elif "youtu.be/" in video_url:
                video_id = video_url.split("youtu.be/")[1][:11]
            elif "/shorts/" in video_url:
                video_id = video_url.split("/shorts/")[1][:11]
            else:
                yt_id_match = re.search(r'(?:v=|\/shorts\/|\.be\/|\/)([0-9A-Za-z_-]{11})', video_url)
                if yt_id_match:
                    video_id = yt_id_match.group(1)

            if video_id:
                print(f"🎯 RAPID-API ALERT: EXTRACTED YOUTUBE ID: {video_id}")
                rapid_url = "https://yt-api.p.rapidapi.com/video/info"
                querystring = {"id": video_id}
                rapid_headers = {
                    "x-rapidapi-key": "095de3a4b8mshaa3f96983077ee0p10f23ejsn3320116b82dc",
                    "x-rapidapi-host": "yt-api.p.rapidapi.com",
                    "Content-Type": "application/json"
                }
                res = requests.get(rapid_url, headers=rapid_headers, params=querystring, timeout=15)
                
                if res.status_code == 200:
                    print("✅ RAPID-API SUCCESS! DATA RECEIVED.")
                    yt_data = res.json()
                    title = yt_data.get('title', 'YouTube Video')
                    if any(word in title.lower() for word in bad_words):
                        return jsonify({"error": "System Alert: Restricted Content Blocked! (Safai Chat Rules)"})
                    
                    thumb_url = 'https://cdn-icons-png.flaticon.com/512/1384/1384060.png'
                    if 'thumbnail' in yt_data and isinstance(yt_data['thumbnail'], list) and len(yt_data['thumbnail']) > 0:
                        thumb_url = yt_data['thumbnail'][-1].get('url', thumb_url)
                        
                    clean_formats = []
                    all_formats = yt_data.get('formats', [])
                    if 'streamingData' in yt_data:
                        all_formats += yt_data['streamingData'].get('formats', [])
                        all_formats += yt_data['streamingData'].get('adaptiveFormats', [])
                        
                    for f in all_formats:
                        f_url = f.get('url')
                        if not f_url: continue
                        quality = f.get('qualityLabel') or f.get('quality') or 'Video'
                        mimeType = f.get('mimeType', '').lower()
                        
                        if 'audio' in mimeType:
                            label = "Audio Only (MP3)"
                        else:
                            label = f"Video - {quality} (Direct Download)"
                        if not any(d['label'] == label for d in clean_formats):
                            clean_formats.append({"label": label, "url": f_url})
                    
                    if clean_formats:
                        return jsonify({"success": True, "title": title, "thumbnail": thumb_url, "formats": clean_formats})
                else:
                    print(f"❌ RAPID-API FAILED! Status: {res.status_code}")
        except Exception as e:
            print("❌ RAPID-API PYTHON ERROR:", e)
            pass

    # ==========================================
    # 🔵 LAYER 2: FACEBOOK API ONLY
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
    # 🟣 LAYER 3: INSTAGRAM API ONLY
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

    # ==========================================
    # 🛡️ BACKUP METHOD: YT-DLP FALLBACK LAYER
    # ==========================================
    ydl_opts = {
        'quiet': True,
        'skip_download': True, 
        'nocheckcertificate': True,
        'format': 'best', 
        'merge_output_format': 'mp4',        
        'cookiefile': 'cookies.txt',         
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate'
        }
    }

    if is_facebook:
        ydl_opts['format'] = 'best'
        ydl_opts['extractor_args'] = {'facebook': {}}
    elif is_instagram:
        ydl_opts['format'] = 'best[ext=mp4]/best'
        ydl_opts['extractor_args'] = {'instagram': {'query_comment_count': 0}}
    elif is_tiktok:
        ydl_opts['http_headers']['Referer'] = 'https://www.tiktok.com/'
        ydl_opts['format'] = 'best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = (info.get('title') or "").lower()
            desc = (info.get('description') or "").lower()
            tags = " ".join(info.get('tags') or []).lower()
            categories = " ".join(info.get('categories') or []).lower()
            full_text = f"{title} {desc} {tags} {categories}"
            
            music_words = ['music', 'bgm', 'instrumental', 'dance', 'dj', 'remix', 'mashup', 'cover', 'lofi', 'beats', 'reverb', 'choreography', 'choreo', 'twerk', 'soundtrack']
            whitelist = ['naat', 'nasheed', 'tilawat', 'quran', 'islamic', 'bayan', 'mufti', 'molvi', 'molana', 'maulana', 'qari', 'hafiz', 'sheikh', 'shaikh', 'khutba', 'dua', 'hamd', 'hadees', 'hadith', 'tafseer', 'vocal only', 'vocals only', 'no music', 'tasbeeh', 'dhikr', 'azan', 'adhan', 'call to prayer', 'tuaha ibn jalil', 'youth club', 'musfirahfamily', 'islamic tarana', 'jihaditarana', 'soulful naats', 'spiritual nasheeds', 'Farsi Noha', 'urdu noha', 'arabic nasheed', 'english nasheed', 'urdu nasheed', 'farsi nasheed', 'islamic nasheed', 'SoulFul Naats', 'Spiritual Nasheeds', 'Quran Recitation', 'Tilawat-e-Quran', 'Islamic Hamd', 'Hadees-e-Nabawi', 'Tafseer-e-Quran', 'No Music', 'Vocal Only', 'Vocals Only', 'urdu translations', 'farsi translations', 'arabic translations', 'english translations', 'islamic translations', 'quran translations', 'naat lyrics', 'nasheed lyrics', 'quran lyrics', 'islamic lyrics', 'hamd lyrics', 'hadees lyrics', 'tafseer lyrics', 'dua lyrics', 'dhikr lyrics', 'tasbeeh lyrics', 'islamic call to prayer', 'islamic azan', 'islamic adhan', 'arshad Reels', 'misha bashir Reels', 'misha bashir shorts', 'islamic lectures for youth', 'islamic videos for youth', 'youth islamic videos', 'youth islamic lectures']
            
            safe_count = sum(full_text.count(w) for w in whitelist)
            title_safe_count = sum(title.count(w) for w in whitelist)
            total_safe_score = safe_count + (title_safe_count * 2)

            found_bad_words = [b for b in bad_words + music_words if b in full_text]
            total_bad_score = sum(full_text.count(b) for b in bad_words + music_words)
            
            if total_bad_score > 0 and total_bad_score > total_safe_score:
                caught_words = ", ".join(found_bad_words[:3]) 
                islamic_message = f"Restricted Content Blocked!\n\nDownloading movies, dramas, music, or inappropriate content goes against Islamic guidelines and is strictly NOT ALLOWED on this platform.\n\n(System caught the keyword: '{caught_words}')\n(Score Check: Bad={total_bad_score}, Safe={total_safe_score})"
                return jsonify({"error": islamic_message})
            
            has_music = any(re.search(r'\b' + re.escape(m) + r'\b', full_text) for m in music_words)
            is_safe_nasheed = any(re.search(r'\b' + re.escape(w) + r'\b', full_text) for w in whitelist)
            if has_music and not is_safe_nasheed:
                return jsonify({"error": "System Alert: Music/BGM Detected! Not allowed unless it is a 'Nasheed' or marked 'No Music'."})
            
            raw_formats = info.get('formats') or [info] 
            clean_formats = []
            audio_count = 0 
            best_direct_url = info.get('url')
            best_thumbnail = info.get('thumbnail')
            if info.get('thumbnails'): best_thumbnail = info['thumbnails'][-1]['url'] 
                
            if is_instagram and best_thumbnail and 'http' in best_thumbnail:
                import urllib.parse
                encoded_thumb = urllib.parse.quote(best_thumbnail, safe='')
                best_thumbnail = f"https://wsrv.nl/?url={encoded_thumb}"
                
            if not best_thumbnail or best_thumbnail == '':
                if is_instagram: best_thumbnail = 'https://cdn-icons-png.flaticon.com/512/174/174855.png'
                elif is_facebook: best_thumbnail = 'https://cdn-icons-png.flaticon.com/512/124/124010.png'
                else: best_thumbnail = 'https://cdn-icons-png.flaticon.com/512/4211/4211158.png'

            for f in raw_formats:
                height = f.get('height') or 'HD'
                vcodec = f.get('vcodec', 'none')
                acodec = f.get('acodec', 'none')
                url = f.get('url')
                protocol = f.get('protocol', '')
                
                if protocol not in ['http', 'https', 'm3u8', 'm3u8_native', 'dash', 'dashy', 'dash_native', 'http_dash_segments']: continue
                if not url: continue
                
                filesize = f.get('filesize') or f.get('filesize_approx') or 0
                mb_size = round(filesize / (1024 * 1024), 1)
                size_tag = f" ({mb_size} MB)" if mb_size > 0 else ""
                label = ""
                
                if vcodec != 'none':
                    if 'tiktok' in (info.get('extractor') or '').lower():
                        if 'watermark' in url.lower() or 'wm' in url.lower() or 'bytevc1' in url.lower(): label = f"Video - With Watermark{size_tag}"
                        else: label = f"Video - No Watermark{size_tag}"
                    else:
                        if acodec == 'none': continue
                        else: label = f"Video - {height}p{size_tag} (With Audio)"
                elif acodec != 'none' and vcodec == 'none':
                    if audio_count < 2:
                        label = f"Audio Only{size_tag}"
                        audio_count += 1
                    else: continue 
                    
                if label and not any(d['label'] == label for d in clean_formats): clean_formats.append({"label": label, "url": url})
            
            if best_direct_url:
                mb_size_best = round((info.get('filesize') or info.get('filesize_approx') or 0) / (1024 * 1024), 1)
                size_tag_best = f" ({mb_size_best} MB)" if mb_size_best > 0 else ""
                best_height = info.get('height') or 'HD'
                if not any(d['url'] == best_direct_url for d in clean_formats): clean_formats.append({"label": f"Video ({best_height}p){size_tag_best}", "url": best_direct_url})
            
            clean_formats.reverse()
            return jsonify({"success": True, "title": info.get('title') or "Downloaded Video", "thumbnail": best_thumbnail, "formats": clean_formats})
    except Exception as e:
        error_msg = str(e)
        if "Empty media response" in error_msg or "Private video" in error_msg:
            return jsonify({"error": "System Alert: Instagram Privacy Block! This video is private or restricted. Please try a public reel."}), 400
        return jsonify({"error": error_msg}), 500

def process_compression(job_id, video_url):
    compression_jobs[job_id] = {'status': 'processing'}
    output_filename = f"compressed_{job_id}.mp4"
    output_path = os.path.join(tempfile.gettempdir(), output_filename)
    outro_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outro.mp4')
    print(f"\n🕵️ CHECKING PATH: {outro_path}") 
    
    try:
        try:
            probe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_type', '-of', 'default=noprint_wrappers=1:nokey=1', video_url]
            has_video = subprocess.check_output(probe_cmd).decode('utf-8').strip() == 'video'
        except: has_video = False

        if has_video and os.path.exists(outro_path):
            print("✅ OUTRO VIDEO FOUND! JORNA SHURU KAREIN!")
            try:
                command = [
                    'ffmpeg', '-y', '-i', video_url, '-i', outro_path,
                    '-filter_complex', 
                    "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1:1,fps=30[main_v];"
                    "[1:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1:1,fps=30[outro_v];"
                    "[0:a]aformat=sample_rates=44100:channel_layouts=stereo[main_a];"
                    "[1:a]aformat=sample_rates=44100:channel_layouts=stereo[outro_a];"
                    "[main_v][main_a][outro_v][outro_a]concat=n=2:v=1:a=1[v][a]",
                    '-map', '[v]', '-map', '[a]', '-vcodec', 'libx264', '-crf', '34', '-preset', 'ultrafast', output_path
                ]
                subprocess.run(command, check=True, stderr=subprocess.PIPE)
                print("🎉 CONCAT SUCCESSFUL! VIDEO JUR GAYI!") 
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.decode('utf-8', errors='ignore')
                with open("ffmpeg_error.txt", "w", encoding="utf-8") as f: f.write("FFMPEG ERROR:\n" + error_msg)
                command = ['ffmpeg', '-y', '-i', video_url, '-vcodec', 'libx264', '-crf', '28', '-preset', 'veryfast', output_path]
                subprocess.run(command, check=True)
        else:
            print("❌ OUTRO FILE MISSING OR AUDIO ONLY! NORMAL COMPRESSION RUNNING.") 
            if has_video: command = ['ffmpeg', '-y', '-i', video_url, '-vcodec', 'libx264', '-crf', '28', '-preset', 'veryfast', output_path]
            else: command = ['ffmpeg', '-y', '-i', video_url, '-c', 'copy', output_path]
            subprocess.run(command, check=True)
            
        final_size_bytes = os.path.getsize(output_path)
        final_size_mb = round(final_size_bytes / (1024 * 1024), 1)
        compression_jobs[job_id] = {'status': 'completed', 'file_path': output_filename, 'final_mb': final_size_mb}
    except Exception as e:
        compression_jobs[job_id] = {'status': 'error', 'message': str(e)}

@app.route('/api/start_compression', methods=['POST'])
def start_compression():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url: return jsonify({"error": "No URL provided"}), 400
    job_id = str(uuid.uuid4())
    thread = threading.Thread(target=process_compression, args=(job_id, video_url))
    thread.start()
    return jsonify({"success": True, "job_id": job_id})

@app.route('/api/check_compression/<job_id>', methods=['GET'])
def check_compression(job_id):
    job = compression_jobs.get(job_id)
    if not job: return jsonify({"error": "Job not found"}), 404
    return jsonify(job)

@app.route('/api/download_compressed/<filename>', methods=['GET'])
def download_compressed(filename):
    path = os.path.join(tempfile.gettempdir(), filename)
    def generate():
        with open(path, "rb") as f:
            while chunk := f.read(4096): yield chunk
    try:
        file_size = os.path.getsize(path)
        headers = {'Content-Disposition': f'attachment; filename=DataSaver_{filename}', 'Content-Length': str(file_size)}
        return Response(stream_with_context(generate()), content_type='video/mp4', headers=headers)
    except Exception as e: return str(e)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
