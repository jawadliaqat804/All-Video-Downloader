// DOM Elements
const themeToggleBtn = document.getElementById('theme-toggle');
const processBtn = document.getElementById('process-btn');
const downloadOptions = document.getElementById('download-options');
const offlineQueueBtn = document.getElementById('offline-queue-btn');
const urlInput = document.getElementById('video-url');

const userIdDisplay = document.getElementById('user-id-display');
const customAlert = document.getElementById('custom-alert');
const alertMessage = document.getElementById('alert-message');
const closeAlertBtn = document.getElementById('close-alert');
const earnCreditsBtn = document.getElementById('earn-credits-btn');
const creditCountDisplay = document.getElementById('credit-count');
// 1. Dark Mode Toggle Logic
themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    // Change icon between moon and sun
    if(document.body.classList.contains('dark-mode')) {
        themeToggleBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
    } else {
        themeToggleBtn.innerHTML = '<i class="fa-solid fa-moon"></i>';
    }
});

// --- Logic 6, Point 1: Strict API Simulated Filter ---

// 1. Array of strict forbidden categories/keywords
const forbiddenTags = ['music', 'song', 'movie', 'dance', 'adult', 'porn', '18+', 'sexy'];

// 2. Fetch Video Action with Strict Simulated API Check
processBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const url = urlInput.value;
    
    if(url.trim() === "") {
        showCustomAlert("Please enter a valid video link first!");
        return;
    }

   processBtn.innerText = "Checking Content...";
  

    // --- RESET UI (Logic 6: Hide and clear old data immediately after click) ---
    downloadOptions.classList.add('hidden'); // Hide the box
    const currentThumbnail = downloadOptions.querySelector('img');
    if (currentThumbnail) currentThumbnail.src = ''; // Clear old image from previous search
    
   // --- 1. FIRST LINE OF DEFENSE (Frontend Quick Check) ---
    
   // --- 1. FIRST LINE OF DEFENSE (Frontend Quick Check) ---
    const fakeApiCategory = url.toLowerCase(); 
    let isClean = true;
    for (let tag of forbiddenTags) {
        if (fakeApiCategory.includes(tag)) {
            isClean = false;
            break;
        }
    }

    if (!isClean) {
        showCustomAlert("Error: Restricted Content Detected!\n\nSorry, downloading music, movies, or inappropriate content is strictly NOT ALLOWED.");
        processBtn.innerText = "Download Video";
        return; // Block immediately!
    }

    // --- 2. SECOND LINE OF DEFENSE (Send to Python for Deep Smart Check) ---
    fetch('https://all-video-downloader-hcqb.onrender.com/api/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }) // Send URL to Python
    })
    .then(response => response.json())
    .then(data => {
            // If Python finds hidden music, Pakistani dramas, or adult tags
            if (data.error) {
            showCustomAlert("System Alert:\n\n" + data.error);
            processBtn.innerText = "Download Video";
            
            return;
        }

        // If Python gives the green light, show download buttons
        downloadOptions.classList.remove('hidden');
        processBtn.innerText = "Video Found!";
        
      // --- LOGIC 6: Professional ID Targeting ---
        const thumbnailImage = document.getElementById('video-thumbnail');
        const titleText = document.getElementById('video-title');

      if (thumbnailImage && data.thumbnail) {
            thumbnailImage.src = data.thumbnail;
            thumbnailImage.referrerPolicy = "no-referrer"; 
            // 🔥 LOGIC FIX: If Insta blocks the image, show a beautiful fallback instead of a crack!
            thumbnailImage.onerror = function() {
                this.src = "https://via.placeholder.com/300x170/1a1a1a/00f2fe?text=Video+Found+Successfully";
            };
        }
        if (titleText && data.title) {
            titleText.innerText = data.title;
        }
        
        
        console.log("Success! Data from Python: ", data);

        // --- LOGIC 8: Dynamic Quality Dropdown & USB Animation ---
        const standardBtn = document.querySelector('.normal-btn');
        const standardCard = standardBtn.parentElement;

        // 1. Remove old dropdown
        const oldDropdown = document.getElementById('quality-dropdown');
        if (oldDropdown) oldDropdown.remove();

        // 2. Create new dropdown menu
        if (data.formats && data.formats.length > 0) {
            const selectHTML = document.createElement('select');
            selectHTML.id = 'quality-dropdown';
            selectHTML.style.cssText = "width: 100%; margin: 10px 0; padding: 8px; border-radius: 5px; background: var(--bg-color); color: var(--text-color); border: 1px solid var(--primary-color); font-weight: bold; cursor: pointer;";
            data.formats.forEach(format => {
                const option = document.createElement('option');
                option.value = format.url;
                option.innerText = format.label;
                selectHTML.appendChild(option);
            });
            standardCard.insertBefore(selectHTML, standardBtn);
        }

        // 3. Clean old listeners
        const newStandardBtn = standardBtn.cloneNode(true);
        standardBtn.parentNode.replaceChild(newStandardBtn, standardBtn);

        // 4. Attach Click Event (Logic 8 - USB Animation Download)
        newStandardBtn.addEventListener('click', () => {
            // 🌟 Smartlink Integration: Add this line
    window.open("https://www.effectivecpmnetwork.com/k8at6mgk8q?key=0971d0ad6934851cbccd39db70134434", "_blank");
           

            const dropdown = document.getElementById('quality-dropdown');
            const selectedUrl = dropdown ? dropdown.value : data.video_url;

            if (!selectedUrl) {
                showCustomAlert("Error: Could not find download link.");
                return;
            }

            // Hide original button and dropdown
            newStandardBtn.style.display = 'none';
            if (dropdown) dropdown.style.display = 'none';

            // --- INJECT DYNAMIC HTML & CSS FOR USB TRANSFER ANIMATION ---
            const animBox = document.createElement('div');
            animBox.id = 'download-anim-box';
            animBox.innerHTML = `
                <style>
                    .usb-wrapper { width: 100%; background: var(--bg-color); border: 2px solid var(--primary-color); border-radius: 12px; padding: 15px; position: relative; overflow: hidden; margin-top: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
                    .usb-slot { width: 100%; height: 45px; background: #1a1a1a; border-radius: 8px; position: relative; overflow: hidden; border: 2px solid #444; box-shadow: inset 0 0 10px rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: flex-start; padding: 0 5px; }
                    .usb-data-block { height: 30px; width: 0%; background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); border-radius: 5px; box-shadow: 0 0 10px #00f2fe; transition: width 0.1s linear; position: relative; }
                    .usb-data-block::after { content: ''; position: absolute; right: 0; top: 0; bottom: 0; width: 10px; background: rgba(255,255,255,0.5); }
                    .usb-head { width: 35px; height: 30px; border: 2px solid #888; border-radius: 4px 0 0 4px; background: #ccc; position: absolute; right: 5px; display: flex; flex-direction: column; justify-content: space-evenly; align-items: center; z-index: 2; }
                    .usb-head .pin { width: 15px; height: 3px; background: #333; }
                    .status-text { color: var(--text-color); font-weight: bold; margin-top: 10px; text-align: center; font-size: 16px; font-family: monospace; }
                </style>
                <div class="usb-wrapper">
                    <div class="usb-slot">
                        <div class="usb-data-block" id="usb-data"></div>
                        <div class="usb-head">
                            <div class="pin"></div>
                            <div class="pin"></div>
                        </div>
                    </div>
                    <div class="status-text" id="prog-text">0% - Transferring...</div>
                </div>
            `;
            standardCard.insertBefore(animBox, newStandardBtn);

            let progress = 0;
            const usbData = animBox.querySelector('#usb-data');
            const progText = animBox.querySelector('#prog-text');

            // --- START 1% TO 100% ANIMATION ---
            const interval = setInterval(() => {
                progress += 2; 
                if (progress > 100) progress = 100;
                
               // Replace with correct template literal syntax
usbData.style.width = `calc(${progress}% - 40px)`;
progText.innerText = `${progress}% - Preparing Video...`;

                // --- WHEN 100% IS REACHED ---
                if (progress === 100) {
                    clearInterval(interval);
                    progText.innerHTML = "Sending to Gallery/Downloads ✅";
                    // 🔥 MASTER STROKE FIX: Use window.location to bypass File Manager security blocks
                    const safeTitle = (data.title || "video").replace(/[^a-zA-Z0-9]/g, "_");
                    const downloadProxyUrl = `https://all-video-downloader-hcqb.onrender.com/api/proxy_download?url=${encodeURIComponent(selectedUrl)}&title=${encodeURIComponent(safeTitle)}`;
                    window.location.href = downloadProxyUrl;

                    // 🔥 NEW: Save real data to database!
                    saveToHistory(data.title, "Standard Download");

                    setTimeout(() => {
                        const historyBtn = Array.from(document.querySelectorAll('.nav-btn')).find(b => b.innerText === 'History');
                        if (historyBtn) {
                            historyBtn.click(); // This will now naturally load the real history from DB!
                            
                            setTimeout(() => {
                                animBox.remove();
                                newStandardBtn.style.display = 'block';
                                if (dropdown) dropdown.style.display = 'block';
                            }, 100);
                        }
                    }, 1000);
                }
            }, 100); 
        });
    })
    .catch(error => {
        showCustomAlert("Server Error! Please make sure your Python server is running.");
        processBtn.innerText = "Download Video";
    });
});

// ==========================================
// --- LOGIC 15: OFFLINE AUTO-DOWNLOAD (20 CREDITS) ---
// ==========================================

offlineQueueBtn.addEventListener('click', () => {
    // 🌟 Smartlink Integration: Add this line
    window.open("https://www.effectivecpmnetwork.com/k8at6mgk8q?key=0971d0ad6934851cbccd39db70134434", "_blank");
   

    if (navigator.onLine) {
        showCustomAlert("You are currently Online! Please use the Standard or Data Saver buttons.");
        return;
    }

    // 1. Check and Deduct 20 Credits
    if (!deductCredits(20)) {
        showCustomAlert("Not enough credits for Auto-Download! Watch an Ad to earn more.");
        return;
    }

    // 2. Get Video Link and Title
    const dropdown = document.getElementById('quality-dropdown');
    if (!dropdown) {
        showCustomAlert("Please search for a video first before going offline!");
        return;
    }
    const selectedUrl = dropdown.value;
    const videoTitle = document.getElementById('video-title').innerText || "Saved_Video";

    // 3. Save to IndexedDB
    const transaction = db.transaction(['offlineQueue'], 'readwrite');
    const store = transaction.objectStore('offlineQueue');
    const queueItem = {
        url: selectedUrl,
        title: videoTitle,
        timestamp: new Date().getTime()
    };

    store.add(queueItem);

    transaction.oncomplete = function() {
        showCustomAlert("Success! 20 Credits used. \n\nVideo safely added to queue! Leave this tab open, it will auto-download when your internet returns.");
        offlineQueueBtn.innerText = "Added to Queue ✅";
        offlineQueueBtn.disabled = true;
    };

    transaction.onerror = function() {
        showCustomAlert("Error saving to queue. Please try again.");
    };
});

// --- THE MAGIC DETECTOR: Waiting for Internet to return ---
window.addEventListener('online', () => {
    console.log("Internet is back! Checking queue...");
    
    if (!db) return; // Ensure database is ready

    const transaction = db.transaction(['offlineQueue'], 'readwrite');
    const store = transaction.objectStore('offlineQueue');
    const request = store.getAll(); // Get all saved videos

    request.onsuccess = function() {
        const queueItems = request.result;
        
        if (queueItems.length > 0) {
            showCustomAlert("Internet connected! Starting auto-downloads from your queue...");
            
            queueItems.forEach(item => {
                // Force download via Python proxy
                const downloadProxyUrl = 'https://all-video-downloader-hcqb.onrender.com/api/proxy_download?url=' + encodeURIComponent(item.url);
                
                const downloadLink = document.createElement('a');
                downloadLink.href = downloadProxyUrl;
                const safeTitle = item.title.replace(/[^a-zA-Z0-9]/g, "_");
                downloadLink.download = safeTitle + ".mp4"; 
                downloadLink.target = "_blank";
                
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);

                // 🔥 NEW: Add to History when it automatically downloads
                saveToHistory(item.title, "Offline Auto-Download");

                // Remove item from queue after starting download
                const deleteTx = db.transaction(['offlineQueue'], 'readwrite');
                deleteTx.objectStore('offlineQueue').delete(item.id);
            });
            
            // Reset button
            if(offlineQueueBtn) {
                offlineQueueBtn.innerText = "Use 20 Credits & Save";
                offlineQueueBtn.disabled = false;
            }
        }
    };
});

// 4. Initializing IndexedDB (Basic setup for future history/offline queue)
let db;
const request = indexedDB.open("VideoDownloaderDB", 1);

request.onupgradeneeded = function(event) {
    db = event.target.result;
    // Create object stores for History and Offline Queue
    if (!db.objectStoreNames.contains('history')) {
        db.createObjectStore('history', { keyPath: 'id', autoIncrement: true });
    }
    if (!db.objectStoreNames.contains('offlineQueue')) {
        db.createObjectStore('offlineQueue', { keyPath: 'id', autoIncrement: true });
    }
};

request.onsuccess = function(event) {
    db = event.target.result;
    console.log("IndexedDB Initialized Successfully!");
};

request.onerror = function(event) {
    console.error("IndexedDB Error: ", event.target.errorCode);
};

// Logic 2 & 5: Generate ID and Load Credits
function initUser() {
    let guestId = localStorage.getItem('videoDownloader_GuestId');
    let currentCredits = localStorage.getItem('videoDownloader_Credits');

    if (!guestId) {
        const randomStr = Math.random().toString(36).substring(2, 8).toUpperCase();
        guestId = 'GUEST_' + randomStr;
        currentCredits = 50; // Default credits
        localStorage.setItem('videoDownloader_GuestId', guestId);
        localStorage.setItem('videoDownloader_Credits', currentCredits);
    }
    
    userIdDisplay.innerText = guestId;
    creditCountDisplay.innerText = currentCredits;
}

// --- Logic 5: Watch to Earn Credits ---
earnCreditsBtn.addEventListener('click', () => {
    // 1. Show Ad playing alert
    showCustomAlert("Playing Ad... Please wait 5 seconds.");
    earnCreditsBtn.disabled = true; // Disable button while "ad" is playing

    // 2. Simulate Ad duration (5 seconds)
    setTimeout(() => {
        let currentCredits = parseInt(localStorage.getItem('videoDownloader_Credits'));
        currentCredits += 10; // Add 10 credits
        
        // Save new balance to storage and update screen
        localStorage.setItem('videoDownloader_Credits', currentCredits);
        creditCountDisplay.innerText = currentCredits;
        
        // Success message
        showCustomAlert("You earned 10 Credits! Your new balance is " + currentCredits);
        earnCreditsBtn.disabled = false; // Re-enable button
    }, 5000);
});

// --- Logic 5: Spend Credits Function ---
function deductCredits(amount) {
    let currentCredits = parseInt(localStorage.getItem('videoDownloader_Credits'));
    
    if (currentCredits >= amount) {
        currentCredits -= amount; // Deduct amount
        localStorage.setItem('videoDownloader_Credits', currentCredits);
        creditCountDisplay.innerText = currentCredits;
        return true; // Deduction successful
    } else {
        return false; // Not enough credits
    }
}

// Logic 2: Custom Alert Function
function showCustomAlert(message) {
    alertMessage.innerText = message;
    customAlert.classList.remove('hidden');
}

closeAlertBtn.addEventListener('click', () => {
    customAlert.classList.add('hidden');
});


// --- Logic 4: SPA Navigation (All HTML/CSS in JS) ---
const navButtons = document.querySelectorAll('.nav-btn');
const mainContainer = document.querySelector('.container');

// Create dynamic container for new pages
const dynamicContent = document.createElement('div');
dynamicContent.id = 'dynamic-content';
mainContainer.appendChild(dynamicContent);

// Get Home elements to hide/show them
const homeElements = Array.from(mainContainer.children).filter(child => child.id !== 'dynamic-content' && child.id !== 'custom-alert');

navButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        // Remove active class from all
        navButtons.forEach(b => b.classList.remove('active'));
        // Add active class to clicked
        e.target.classList.add('active');

        const pageName = e.target.innerText;

        if (pageName === 'Home') {
            homeElements.forEach(el => el.style.display = '');
            dynamicContent.innerHTML = ''; 
        } else if (pageName === 'History') {
            homeElements.forEach(el => el.style.display = 'none');
            dynamicContent.innerHTML = `<h2>Your Download History</h2><div id="history-container" style="margin-top: 20px;">Loading...</div>`;
            
            if (db) {
                const request = db.transaction(['history'], 'readonly').objectStore('history').getAll();
                request.onsuccess = () => {
                    const items = request.result.sort((a, b) => b.timestamp - a.timestamp); // Newest first
                    const container = document.getElementById('history-container');
                    if (items.length === 0) {
                        container.innerHTML = `<div style="padding: 20px; background: var(--card-bg); border-radius: 10px; border: 1px solid #ddd;"><p style="color: gray;">No history found yet! Downloaded videos will appear here.</p></div>`;
                    } else {
                        let html = '';
                        items.forEach(item => {
                            html += `
                            <div style="padding: 15px; background: var(--card-bg); border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #28a745; text-align: left; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                                <h4 style="margin: 0 0 5px 0; color: var(--text-color);">${item.title}</h4>
                                <p style="margin: 0; font-size: 0.9em; color: gray;"><b>Type:</b> ${item.type} <br> <b>Time:</b> ${item.date}</p>
                            </div>`;
                        });
                        container.innerHTML = html;
                    }
                };
            }
        } else if (pageName === 'Settings') {
            homeElements.forEach(el => el.style.display = 'none');
            dynamicContent.innerHTML = `
                <h2>App Settings</h2>
                <div style="text-align: left; background: var(--card-bg); padding: 20px; border-radius: 10px; margin-top: 20px; border: 1px solid #ddd;">
                    <label style="font-weight: bold; color: var(--text-color);">Default Video Quality:</label>
                    <select style="margin-left: 10px; padding: 5px; border-radius: 5px; background: var(--bg-color); color: var(--text-color); border: 1px solid var(--primary-color);">
                        <option>1080p (High)</option>
                        <option>720p (Medium)</option>
                    </select>
                    <br><br>
                    <button class="btn-3d" style="background: #dc3545; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer;">Clear History</button>
                </div>
            `;
        } else if (pageName === 'About') {
    homeElements.forEach(el => el.style.display = 'none');
    dynamicContent.innerHTML = `
        <div style="background: var(--card-bg); padding: 30px; border-radius: 15px; margin-top: 20px; border: 1px solid #ddd; line-height: 1.6;">
            <h2 style="color: var(--text-color); margin-bottom: 20px;">About All Video Downloader</h2>
            
            <p style="color: var(--text-color);"><strong>Our Mission: Bridging Technology, Convenience, and Islamic Values</strong></p>
            <p style="color: var(--text-color);">My name is Jawad Liaqat, and the core purpose of this platform is to provide a digital environment where modern convenience aligns perfectly with the teachings and ethical boundaries of Islam.</p>
            
            <h3 style="color: var(--text-color); margin-top: 20px;">Our Commitment</h3>
            <p style="color: var(--text-color);">We are dedicated to building a platform that not only meets modern digital demands but also upholds our values with integrity. Our mission is to offer a clean, secure, and ethical space where users can access the content they need without compromising on principles.</p>
            
            <h3 style="color: var(--text-color); margin-top: 20px;">Key Features</h3>
            <ul style="color: var(--text-color); padding-left: 20px;">
                <li><strong>High-Speed Downloading:</strong> Powered by advanced algorithms, your favorite videos are now just a second away.</li>
                <li><strong>Smart Data Saver:</strong> Our application ensures maximum data efficiency, allowing you to access content without worrying about excessive internet consumption.</li>
                <li><strong>Offline Smart Queue:</strong> If your internet connection drops unexpectedly, your efforts won't go to waste. Simply copy the link; our system will secure it. As soon as your internet is restored, your generated link will be ready for download.</li>
            </ul>

            <h3 style="color: var(--text-color); margin-top: 20px;">A Noble Journey</h3>
            <p style="color: var(--text-color);">"This is more than just a tool; it is a Sadqa-e-Jariya. By using this platform, you are not just downloading content—you are becoming a partner in a noble mission to spread Islamic values. We humbly request you to support us, share this website with your friends and family, and help us spread the message of our values to every corner of the internet. Together, we can make a difference."</p>
            
            <p style="color: gray; margin-top: 20px; font-size: 0.9em;">Version 0.0.1</p>
        </div>
    `;
} 
else if (pageName === 'Connect US') {
    // Hide home elements
    homeElements.forEach(el => el.style.display = 'none');
    
    // Inject the new 3D design into dynamicContent
    dynamicContent.innerHTML = `
        <style>
            @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
            .social-3d-container { display: flex; gap: 28px; flex-wrap: wrap; justify-content: center; padding: 40px 0; max-width: 280px; margin: 0 auto; }
            .iso-icon { position: relative; width: 60px; height: 60px; background: #ffffff; display: flex; justify-content: center; align-items: center; text-decoration: none; color: #333333; font-size: 28px; transform: perspective(1000px) rotate(-30deg) skew(25deg) translate(0, 0); transition: all 0.4s ease; box-shadow: -15px 15px 10px rgba(0,0,0,0.2); border-radius: 8px; }
            .iso-icon::before { content: ''; position: absolute; top: 5px; left: -10px; height: 100%; width: 10px; background: #cccccc; transform: skewY(-45deg); transition: all 0.4s ease; border-radius: 4px 0 0 4px; }
            .iso-icon::after { content: ''; position: absolute; bottom: -10px; left: -5px; height: 10px; width: 100%; background: #dddddd; transform: skewX(-45deg); transition: all 0.4s ease; border-radius: 0 0 4px 4px; }
            .iso-icon:hover { transform: perspective(1000px) rotate(-30deg) skew(25deg) translate(15px, -15px); color: #ffffff; }
            .iso-icon.yt:hover { background: #ff0000; box-shadow: -30px 30px 30px rgba(255,0,0,0.3); } .iso-icon.yt:hover::before { background: #cc0000; } .iso-icon.yt:hover::after { background: #e60000; }
            .iso-icon.fb:hover { background: #1877f2; box-shadow: -30px 30px 30px rgba(24,119,242,0.3); } .iso-icon.fb:hover::before { background: #115ab8; } .iso-icon.fb:hover::after { background: #1468d4; }
            .iso-icon.tt:hover { background: #111111; box-shadow: -30px 30px 30px rgba(0,0,0,0.3); } .iso-icon.tt:hover::before { background: #000000; } .iso-icon.tt:hover::after { background: #222222; }
            .iso-icon.ig:hover { background: #e1306c; box-shadow: -30px 30px 30px rgba(225,48,108,0.3); } .iso-icon.ig:hover::before { background: #b02353; } .iso-icon.ig:hover::after { background: #c8295f; }
            .iso-icon.wa:hover { background: #25d366; box-shadow: -30px 30px 30px rgba(37,211,102,0.3); } .iso-icon.wa:hover::before { background: #1b994a; } .iso-icon.wa:hover::after { background: #20b858; }
        </style>

        <div style="background: var(--card-bg); padding: 30px; border-radius: 15px; margin-top: 20px; border: 1px solid #ddd; text-align: center;">
            <h2 style="color: var(--text-color); margin-bottom: 10px;">Stay Connected</h2>
            <p style="color: var(--text-color); margin-bottom: 30px;">Follow our official channels for the latest updates!</p>
            
            <div class="social-3d-container">
                <a href="YOUR_YOUTUBE_LINK" target="_blank" class="iso-icon yt" title="YouTube"><i class="fa-brands fa-youtube"></i></a>
                <a href="YOUR_FACEBOOK_LINK" target="_blank" class="iso-icon fb" title="Facebook"><i class="fa-brands fa-facebook-f"></i></a>
                <a href="YOUR_TIKTOK_LINK" target="_blank" class="iso-icon tt" title="TikTok"><i class="fa-brands fa-tiktok"></i></a>
                <a href="YOUR_INSTAGRAM_LINK" target="_blank" class="iso-icon ig" title="Instagram"><i class="fa-brands fa-instagram"></i></a>
                <a href="YOUR_WHATSAPP_LINK" target="_blank" class="iso-icon wa" title="WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>
            </div>
        </div>
    `;
}
    });
});

// Call this function when page loads to generate Guest ID
initUser();

// ==========================================
// --- LOGIC DATA SAVER 2 (POLLING & AUTO DOWNLOAD) ---
// ==========================================

const dataSaverBtn = document.getElementById('data-saver-btn'); 

if (dataSaverBtn) {
    dataSaverBtn.addEventListener('click', () => {
        // 🌟 Smartlink Integration: Add this line
    window.open("https://www.effectivecpmnetwork.com/k8at6mgk8q?key=0971d0ad6934851cbccd39db70134434", "_blank");
       
        
        // 1. Check & Deduct 10 Credits instantly!
        if (!deductCredits(10)) {
            showCustomAlert("Not enough credits for Data Saver! Watch an Ad to earn more.");
            return;
        }

        // 2. Get the highest quality URL from the generated dropdown
        const dropdown = document.getElementById('quality-dropdown');
        if (!dropdown) {
            showCustomAlert("Please search for a video first!");
            return; 
        }
        const selectedUrl = dropdown.value;
        const selectedText = dropdown.options[dropdown.selectedIndex].text;
        
        // 🔥 LOGIC 14: Extract Original MB from dropdown text (e.g., "Video - 1080p (50.5 MB)")
        let originalMb = 0;
        const match = selectedText.match(/\(([\d.]+)\s*MB\)/);
        if(match) {
            originalMb = parseFloat(match[1]);
        }

        // 3. Change button text so user knows magic is happening
        const originalText = dataSaverBtn.innerText;
        dataSaverBtn.innerText = "Compressing... Please Wait";
        dataSaverBtn.disabled = true;
        dataSaverBtn.style.opacity = "0.7";

        // 4. Send to Python Server to start background task
        fetch('https://all-video-downloader-hcqb.onrender.com/api/start_compression', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: selectedUrl })
        })
        .then(res => res.json())
        .then(data => {
            if (data.job_id) {
                // START POLLING: Pass originalMb to calculate savings later
                startPollingStatus(data.job_id, originalText, originalMb); 
            } else {
                throw new Error("Failed to start job");
            }
        })
        .catch(err => {
            showCustomAlert("Server Error! Compression failed.");
            dataSaverBtn.innerText = originalText;
            dataSaverBtn.disabled = false;
        });
    });
}

// Polling Logic: The function that secretly asks the server "Is it done yet?"
function startPollingStatus(jobId, originalText, originalMb) {
    const interval = setInterval(() => {
        
        fetch(`https://all-video-downloader-hcqb.onrender.com/api/check_compression/${jobId}`)
        .then(res => res.json())
        .then(job => {
            if (job.status === 'completed') {
                clearInterval(interval); // Stop asking
                
                // 🔥 LOGIC 14 (Master Stroke): Calculate Saved MB and show Dynamic English Alert
                let finalMb = job.final_mb || 0;
                let alertMessage = "";
                
                if (originalMb > finalMb && finalMb > 0) {
                    let savedMb = (originalMb - finalMb).toFixed(1);
                    alertMessage = `Success! 10 Credits used.\n\n Original Size: ${originalMb} MB\n Compressed Size: ${finalMb} MB\n You Saved: ${savedMb} MB of internet data!\n\nYour High-Quality video is downloading straight to your Gallery/Downloads. ✅`;
                } else {
                    // Fallback message if original was smaller or unavailable
                    alertMessage = `Success! 10 Credits used.\n\nYour High-Quality video is ready! (Final Size: ${finalMb} MB).\n\nIt's downloading straight to your Gallery/Downloads. ✅`;
                }

                dataSaverBtn.innerText = "Download Complete! ✅";
                dataSaverBtn.disabled = false;
                dataSaverBtn.style.opacity = "1";
                showCustomAlert(alertMessage);
                
                // 🔥 NEW: Save real data to database!
                const videoTitleObj = document.getElementById('video-title');
                const savedTitle = videoTitleObj ? videoTitleObj.innerText : "Compressed Video";
                saveToHistory(savedTitle, "Data Saver (Compressed)");
               
                const downloadUrl = `https://all-video-downloader-hcqb.onrender.com/api/download_compressed/${job.file_path}`;
                window.location.href = downloadUrl; 

              
                setTimeout(() => {
                    dataSaverBtn.innerText = originalText;
                }, 3000);

            } else if (job.status === 'error') {
                clearInterval(interval);
                showCustomAlert("Error compressing video: " + (job.message || "Unknown error"));
                dataSaverBtn.innerText = originalText;
                dataSaverBtn.disabled = false;
            }
        })
        .catch(err => console.log("Polling wait..."));
        
    }, 3000); // Wait 3 seconds between each question
}


// ==========================================
// --- LOGIC 17: SAVE TO HISTORY DATABASE ---
// ==========================================
function saveToHistory(title, downloadType) {
    if (!db) return;
    const transaction = db.transaction(['history'], 'readwrite');
    const store = transaction.objectStore('history');
    store.add({
        title: title || "Video Download",
        type: downloadType,
        date: new Date().toLocaleString(),
        timestamp: new Date().getTime()
    });
}

// ==========================================
// --- LOGIC: EK TEER SE DO SHIKAR (Double Click Logo) ---
// ==========================================

// 1. Create the small round logo element dynamically
const appLogo = document.createElement('img');
appLogo.src = 'logo.png'; // Make sure your image is saved in the images folder with this exact name
appLogo.alt = 'Jawad Downloader Logo';

// 2. Style the logo (Small, Round, and Beautiful)
appLogo.style.cssText = `
    width: 70px; 
    height: 70px; 
    border-radius: 50%; 
    object-fit: cover; 
    cursor: pointer; 
    border: 3px solid var(--primary-color, #00f2fe); 
    box-shadow: 0 4px 15px rgba(0,242,254,0.4); 
    display: block; 
    margin: 0 auto 15px auto; 
    transition: transform 0.3s ease;
`;

// Add a cool hover effect
appLogo.onmouseover = () => appLogo.style.transform = 'scale(1.1)';
appLogo.onmouseout = () => appLogo.style.transform = 'scale(1)';

// 3. Inject the logo at the top of the main container
const mainAppContainer = document.querySelector('.container');
if (mainAppContainer) {
    mainAppContainer.insertBefore(appLogo, mainAppContainer.firstChild);
}

// 4. The Magic Double Click Event (Full Screen Pop-up)
appLogo.addEventListener('dblclick', () => {
    // Create the dark background overlay
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed; 
        top: 0; 
        left: 0; 
        width: 100%; 
        height: 100%; 
        background: rgba(0, 0, 0, 0.9); 
        display: flex; 
        justify-content: center; 
        align-items: center; 
        z-index: 9999; 
        cursor: zoom-out;
        backdrop-filter: blur(5px);
    `;

    // Create the Full HD Image
    const fullScreenImg = document.createElement('img');
    fullScreenImg.src = 'logo.png';
    fullScreenImg.style.cssText = `
        max-width: 90%; 
        max-height: 90%; 
        border-radius: 15px; 
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.8);
        transform: scale(0.8);
        transition: transform 0.3s ease;
    `;

    // Add elements to screen
    overlay.appendChild(fullScreenImg);
    document.body.appendChild(overlay);

    // Small delay to trigger the pop-up zoom animation
    setTimeout(() => {
        fullScreenImg.style.transform = 'scale(1)';
    }, 10);

    // Close the full screen when clicked anywhere
    overlay.addEventListener('click', () => {
        fullScreenImg.style.transform = 'scale(0.8)';
        setTimeout(() => {
            document.body.removeChild(overlay);
        }, 200); // Wait for zoom-out animation to finish
    });
});

// --- PWA Installation Logic (App Download System) ---

let deferredPrompt;
const installAppBtn = document.getElementById('install-app-btn');

// 1. Register the Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
                console.log('Service Worker registered successfully:', registration.scope);
            })
            .catch((error) => {
                console.log('Service Worker registration failed:', error);
            });
    });
}

// 2. Catch the install prompt and show the button
window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the default browser pop-up
    e.preventDefault();
    deferredPrompt = e;
    
    // Show our custom "Install App" button
    if (installAppBtn) {
        installAppBtn.style.display = 'inline-block';
    }
});

// 3. Handle the user clicking the "Install App" button
if (installAppBtn) {
    installAppBtn.addEventListener('click', async () => {
        if (deferredPrompt) {
            // Show the actual installation prompt to the user
            deferredPrompt.prompt();
            // Wait for the user's response (Yes or No)
            const { outcome } = await deferredPrompt.userChoice;
            console.log(`User response to the install prompt: ${outcome}`);
            
            // Clear the prompt and hide the button
            deferredPrompt = null;
            installAppBtn.style.display = 'none';
        }
    });
}

