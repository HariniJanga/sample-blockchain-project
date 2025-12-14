from flask import Flask, request, jsonify, session, redirect, url_for
import hashlib
import json
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Simple user storage
users = {
    'admin': {
        'username': 'admin',
        'password': 'admin123',
        'email': 'admin@example.com',
        'company_name': 'Demo Company',
        'role': 'manufacturer'
    }
}

# Simple blockchain storage
blockchain_data = {
    'transactions': {},
    'current_block': 12345,
    'connected': True
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Login required'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            session['user'] = users[username]
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials'
            return f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Login - Product Authentication</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }}
                    .login-box {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }}
                    h1 {{ text-align: center; color: #333; margin-bottom: 30px; }}
                    .form-group {{ margin-bottom: 20px; }}
                    label {{ display: block; margin-bottom: 5px; color: #555; font-weight: bold; }}
                    input {{ width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }}
                    input:focus {{ outline: none; border-color: #667eea; }}
                    button {{ width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }}
                    button:hover {{ transform: translateY(-2px); }}
                    .error {{ color: red; text-align: center; margin-bottom: 20px; }}
                    .demo {{ text-align: center; margin-top: 20px; font-size: 14px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="login-box">
                    <h1>🔐 Login</h1>
                    <div class="error">{error}</div>
                    <form method="POST">
                        <div class="form-group">
                            <label>Username:</label>
                            <input type="text" name="username" required>
                        </div>
                        <div class="form-group">
                            <label>Password:</label>
                            <input type="password" name="password" required>
                        </div>
                        <button type="submit">Login</button>
                    </form>
                    <div class="demo">
                        <strong>Demo:</strong> admin / admin123
                    </div>
                </div>
            </body>
            </html>
            '''
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - Product Authentication</title>
        <style>
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
            .login-box { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }
            h1 { text-align: center; color: #333; margin-bottom: 30px; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; color: #555; font-weight: bold; }
            input { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }
            input:focus { outline: none; border-color: #667eea; }
            button { width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
            button:hover { transform: translateY(-2px); }
            .demo { text-align: center; margin-top: 20px; font-size: 14px; color: #666; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h1>🔐 Login</h1>
            <form method="POST">
                <div class="form-group">
                    <label>Username:</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit">Login</button>
            </form>
            <div class="demo">
                <strong>Demo:</strong> admin / admin123
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = session['user']
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - Product Authentication</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }}
            .header {{ background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: white; padding: 20px; }}
            .container {{ max-width: 1000px; margin: 0 auto; padding: 20px; }}
            .card {{ background: white; padding: 30px; margin: 20px 0; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
            .form-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .form-group {{ margin-bottom: 20px; }}
            label {{ display: block; margin-bottom: 5px; font-weight: bold; color: #333; }}
            input, textarea {{ width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; }}
            input:focus, textarea:focus {{ border-color: #e74c3c; outline: none; }}
            button {{ background: #e74c3c; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
            button:hover {{ background: #c0392b; }}
            .status {{ padding: 15px; margin: 15px 0; border-radius: 5px; }}
            .success {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
            .error {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
            .nav {{ text-align: right; }}
            .nav a {{ color: white; text-decoration: none; margin-left: 20px; }}
            .tx-hash {{ font-family: monospace; background: #f8f9fa; padding: 10px; border-radius: 5px; word-break: break-all; }}
            .qr-section {{ text-align: center; margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 10px; }}
            @media (max-width: 768px) {{ .form-grid {{ grid-template-columns: 1fr; }} }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="container">
                <h1>🔗 Product Authentication Dashboard</h1>
                <div class="nav">
                    Welcome, {user['username']} | 
                    <a href="/consumer">🔍 Consumer Portal</a> | 
                    <a href="/logout">Logout</a>
                </div>
            </div>
        </div>
        
        <div class="container">
            <div class="card">
                <h2>⛓️ Blockchain Status</h2>
                <div id="blockchainStatus">
                    <div class="status success">
                        <strong>✅ Connected</strong><br>
                        Block: {blockchain_data['current_block']} | Balance: 10.0 ETH
                    </div>
                </div>
                <button onclick="refreshStatus()">🔄 Refresh</button>
            </div>
            
            <div class="card">
                <h2>📝 Register Product</h2>
                <form id="productForm">
                    <div class="form-grid">
                        <div class="form-group">
                            <label>Product Name *</label>
                            <input type="text" id="productName" required>
                        </div>
                        <div class="form-group">
                            <label>Manufacturer *</label>
                            <input type="text" id="manufacturer" value="{user['company_name']}" required>
                        </div>
                        <div class="form-group">
                            <label>Batch Number *</label>
                            <input type="text" id="batchNumber" required>
                        </div>
                        <div class="form-group">
                            <label>Serial Number</label>
                            <input type="text" id="serialNumber">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Description</label>
                        <textarea id="description" rows="3"></textarea>
                    </div>
                    <button type="submit">⛓️ Register on Blockchain</button>
                </form>
                <div id="result"></div>
            </div>
        </div>
        
        <script>
            async function refreshStatus() {{
                try {{
                    const response = await fetch('/api/blockchain/status');
                    const data = await response.json();
                    document.getElementById('blockchainStatus').innerHTML = 
                        '<div class="status success"><strong>✅ Connected</strong><br>Block: ' + data.current_block + ' | Balance: 10.0 ETH</div>';
                }} catch (error) {{
                    document.getElementById('blockchainStatus').innerHTML = 
                        '<div class="status error"><strong>❌ Error</strong><br>' + error.message + '</div>';
                }}
            }}
            
            document.getElementById('productForm').addEventListener('submit', async function(e) {{
                e.preventDefault();
                
                const productData = {{
                    name: document.getElementById('productName').value,
                    manufacturer: document.getElementById('manufacturer').value,
                    batchNumber: document.getElementById('batchNumber').value,
                    serialNumber: document.getElementById('serialNumber').value,
                    description: document.getElementById('description').value
                }};
                
                if (!productData.name || !productData.manufacturer || !productData.batchNumber) {{
                    document.getElementById('result').innerHTML = 
                        '<div class="status error">Please fill in all required fields</div>';
                    return;
                }}
                
                try {{
                    const response = await fetch('/api/products', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(productData)
                    }});
                    
                    const result = await response.json();
                    
                    if (result.success) {{
                        document.getElementById('result').innerHTML = `
                            <div class="status success">
                                <h3>✅ Product Registered!</h3>
                                <p><strong>Transaction Hash:</strong></p>
                                <div class="tx-hash">${{result.transaction_hash}}</div>
                                <p><strong>Block:</strong> ${{result.block_number}} | <strong>Gas:</strong> ${{result.gas_used}}</p>
                                <div class="qr-section">
                                    <button onclick="generateQR('${{result.transaction_hash}}')">🎯 Generate QR Code</button>
                                    <button onclick="copyHash('${{result.transaction_hash}}')">📋 Copy Hash</button>
                                    <button onclick="testVerify('${{result.transaction_hash}}')">🔍 Test Verify</button>
                                </div>
                                <div id="qrCode"></div>
                            </div>
                        `;
                        this.reset();
                        document.getElementById('manufacturer').value = '{user['company_name']}';
                    }} else {{
                        document.getElementById('result').innerHTML = 
                            '<div class="status error">❌ Error: ' + result.error + '</div>';
                    }}
                }} catch (error) {{
                    document.getElementById('result').innerHTML = 
                        '<div class="status error">❌ Error: ' + error.message + '</div>';
                }}
            }});
            
            function generateQR(txHash) {{
                const verifyUrl = window.location.origin + '/consumer?tx=' + txHash;
                const qrUrl = 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=' + encodeURIComponent(verifyUrl);
                document.getElementById('qrCode').innerHTML = `
                    <h4>📱 QR Code for Verification</h4>
                    <img src="${{qrUrl}}" alt="QR Code" style="border: 2px solid #27ae60; border-radius: 10px;">
                    <p>Scan to verify product authenticity</p>
                    <button onclick="downloadQR('${{qrUrl}}', '${{txHash}}')">💾 Download</button>
                `;
            }}
            
            function downloadQR(qrUrl, txHash) {{
                const link = document.createElement('a');
                link.href = qrUrl;
                link.download = 'product-qr-' + txHash.substring(0, 10) + '.png';
                link.click();
            }}
            
            function copyHash(txHash) {{
                navigator.clipboard.writeText(txHash).then(() => {{
                    alert('✅ Transaction hash copied!');
                }}).catch(() => {{
                    prompt('Copy this hash:', txHash);
                }});    
            }}
            
            function testVerify(txHash) {{
                window.open('/consumer?tx=' + txHash, '_blank');
            }}
        </script>
    </body>
    </html>
    '''

@app.route('/consumer')
def consumer():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Product Verification</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); min-height: 100vh; }
            .header { background: rgba(0,0,0,0.1); color: white; padding: 20px; text-align: center; }
            .container { max-width: 800px; margin: 0 auto; padding: 20px; }
            .card { background: white; padding: 30px; margin: 20px 0; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }
            input:focus { border-color: #27ae60; outline: none; }
            button { width: 100%; padding: 12px; background: #27ae60; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; margin: 5px 0; }
            button:hover { background: #219a52; }
            button:disabled { opacity: 0.6; cursor: not-allowed; }
            .result { margin-top: 20px; padding: 20px; border-radius: 5px; }
            .success { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }
            .product-info { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .nav-link { color: white; text-decoration: none; margin: 0 10px; }
            .scan-section { text-align: center; margin: 20px 0; }
            #qr-video { width: 100%; max-width: 400px; height: 300px; border: 2px solid #27ae60; border-radius: 10px; background: #000; }
            .scan-controls { margin: 15px 0; }
            .scan-controls button { width: auto; padding: 10px 20px; margin: 5px; }
            .camera-select { width: 100%; padding: 10px; margin: 10px 0; border: 2px solid #ddd; border-radius: 5px; }
            .scan-result { background: #e8f5e8; padding: 15px; margin: 15px 0; border-radius: 5px; border: 2px solid #27ae60; }
            .tabs { display: flex; background: #f8f9fa; border-radius: 10px; overflow: hidden; margin-bottom: 20px; }
            .tab { flex: 1; padding: 15px; text-align: center; cursor: pointer; background: #e9ecef; border: none; }
            .tab.active { background: #27ae60; color: white; }
            .tab-content { display: none; }
            .tab-content.active { display: block; }
            @media (max-width: 768px) { .container { padding: 10px; } .card { padding: 20px; margin: 10px 0; } }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔍 Product Verification</h1>
            <p>Verify product authenticity using blockchain</p>
            <a href="/" class="nav-link">🏠 Home</a> | <a href="/login" class="nav-link">🔐 Login</a>
        </div>
        
        <div class="container">
            <div class="card">
                <div class="tabs">
                    <button class="tab active" onclick="switchTab('scan')">📱 Scan QR Code</button>
                    <button class="tab" onclick="switchTab('manual')">⌨️ Enter Manually</button>
                </div>
                
                <!-- QR Scanner Tab -->
                <div id="scan-tab" class="tab-content active">
                    <h2>📱 Scan QR Code</h2>
                    <div class="scan-section">
                        <video id="qr-video" autoplay muted playsinline></video>
                        <canvas id="qr-canvas" style="display: none;"></canvas>
                        
                        <div class="scan-controls">
                            <button id="start-scan" onclick="startScanning()">📷 Start Camera</button>
                            <button id="stop-scan" onclick="stopScanning()" disabled>⏹️ Stop Camera</button>
                        </div>
                        
                        <select id="camera-select" class="camera-select" onchange="switchCamera()">
                            <option value="">Select Camera...</option>
                        </select>
                        
                        <div id="scan-status"></div>
                    </div>
                </div>
                
                <!-- Manual Entry Tab -->
                <div id="manual-tab" class="tab-content">
                    <h2>⌨️ Enter Transaction Hash</h2>
                    <form id="verifyForm">
                        <div class="form-group">
                            <label>Transaction Hash:</label>
                            <input type="text" id="txHash" placeholder="Enter transaction hash..." required>
                        </div>
                        <button type="submit">🔍 Verify Product</button>
                    </form>
                </div>
                
                <div id="verifyResult"></div>
            </div>
            
            <div class="card">
                <h3>📋 How to Verify:</h3>
                <div class="tabs">
                    <button class="tab active" onclick="switchHelpTab('qr')">QR Code Method</button>
                    <button class="tab" onclick="switchHelpTab('manual')">Manual Method</button>
                </div>
                
                <div id="qr-help" class="tab-content active">
                    <ol>
                        <li>Click "Start Camera" to activate your device camera</li>
                        <li>Point your camera at the QR code on the product</li>
                        <li>Wait for automatic detection and verification</li>
                        <li>View the blockchain-verified product details</li>
                    </ol>
                </div>
                
                <div id="manual-help" class="tab-content">
                    <ol>
                        <li>Get the transaction hash from the manufacturer</li>
                        <li>Enter it in the "Enter Manually" tab</li>
                        <li>Click "Verify Product"</li>
                        <li>View the blockchain-verified details</li>
                    </ol>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js"></script>
        <script>
            let stream = null;
            let scanning = false;
            let canvas, context, video;
            
            // Initialize elements
            window.addEventListener('load', function() {
                canvas = document.getElementById('qr-canvas');
                context = canvas.getContext('2d');
                video = document.getElementById('qr-video');
                
                // Auto-fill from URL parameter
                const urlParams = new URLSearchParams(window.location.search);
                const txParam = urlParams.get('tx');
                if (txParam) {
                    document.getElementById('txHash').value = txParam;
                    switchTab('manual');
                    setTimeout(() => {
                        document.getElementById('verifyForm').dispatchEvent(new Event('submit'));
                    }, 500);
                }
                
                // Get available cameras
                getCameras();
            });
            
            async function getCameras() {
                try {
                    const devices = await navigator.mediaDevices.enumerateDevices();
                    const videoDevices = devices.filter(device => device.kind === 'videoinput');
                    const select = document.getElementById('camera-select');
                    
                    select.innerHTML = '<option value="">Select Camera...</option>';
                    videoDevices.forEach((device, index) => {
                        const option = document.createElement('option');
                        option.value = device.deviceId;
                        option.text = device.label || `Camera ${index + 1}`;
                        select.appendChild(option);
                    });
                    
                    // Auto-select back camera on mobile
                    const backCamera = videoDevices.find(device => 
                        device.label.toLowerCase().includes('back') || 
                        device.label.toLowerCase().includes('rear')
                    );
                    if (backCamera) {
                        select.value = backCamera.deviceId;
                    }
                } catch (error) {
                    console.log('Error getting cameras:', error);
                }
            }
            
            async function startScanning() {
                try {
                    const selectedCamera = document.getElementById('camera-select').value;
                    const constraints = {
                        video: {
                            facingMode: selectedCamera ? undefined : { ideal: 'environment' },
                            deviceId: selectedCamera ? { exact: selectedCamera } : undefined,
                            width: { ideal: 1280 },
                            height: { ideal: 720 }
                        }
                    };
                    
                    stream = await navigator.mediaDevices.getUserMedia(constraints);
                    video.srcObject = stream;
                    
                    video.onloadedmetadata = () => {
                        canvas.width = video.videoWidth;
                        canvas.height = video.videoHeight;
                        scanning = true;
                        scanFrame();
                        
                        document.getElementById('start-scan').disabled = true;
                        document.getElementById('stop-scan').disabled = false;
                        document.getElementById('scan-status').innerHTML = 
                            '<div style="color: #27ae60;">📷 Camera active - Point at QR code</div>';
                    };
                } catch (error) {
                    console.error('Error starting camera:', error);
                    document.getElementById('scan-status').innerHTML = 
                        '<div style="color: #e74c3c;">❌ Camera access denied or not available</div>';
                }
            }
            
            function stopScanning() {
                scanning = false;
                if (stream) {
                    stream.getTracks().forEach(track => track.stop());
                    stream = null;
                }
                video.srcObject = null;
                
                document.getElementById('start-scan').disabled = false;
                document.getElementById('stop-scan').disabled = true;
                document.getElementById('scan-status').innerHTML = 
                    '<div style="color: #666;">📷 Camera stopped</div>';
            }
            
            function scanFrame() {
                if (!scanning) return;
                
                if (video.readyState === video.HAVE_ENOUGH_DATA) {
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
                    const code = jsQR(imageData.data, imageData.width, imageData.height);
                    
                    if (code) {
                        handleQRDetection(code.data);
                        return;
                    }
                }
                
                requestAnimationFrame(scanFrame);
            }
            
            function handleQRDetection(data) {
                document.getElementById('scan-status').innerHTML = 
                    '<div class="scan-result">🎯 QR Code detected! Processing...</div>';
                
                // Extract transaction hash from URL or use data directly
                let txHash = data;
                if (data.includes('/consumer?tx=')) {
                    const urlParams = new URLSearchParams(data.split('?')[1]);
                    txHash = urlParams.get('tx');
                } else if (data.startsWith('http')) {
                    // If it's a URL, try to extract tx parameter
                    try {
                        const url = new URL(data);
                        const params = new URLSearchParams(url.search);
                        txHash = params.get('tx') || data;
                    } catch (e) {
                        txHash = data;
                    }
                }
                
                // Verify the product
                verifyProduct(txHash);
                stopScanning();
            }
            
            function switchCamera() {
                if (scanning) {
                    stopScanning();
                    setTimeout(startScanning, 500);
                }
            }
            
            function switchTab(tab) {
                // Update tab buttons
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelector(`button[onclick="switchTab('${tab}')"]`).classList.add('active');
                
                // Update tab content
                document.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.remove('active');
                });
                document.getElementById(tab + '-tab').classList.add('active');
                
                // Stop scanning if switching away from scan tab
                if (tab !== 'scan' && scanning) {
                    stopScanning();
                }
            }
            
            function switchHelpTab(tab) {
                // Update help tab buttons
                const helpTabs = document.querySelectorAll('.card:last-child .tab');
                helpTabs.forEach(t => t.classList.remove('active'));
                document.querySelector(`button[onclick="switchHelpTab('${tab}')"]`).classList.add('active');
                
                // Update help content
                document.getElementById('qr-help').classList.remove('active');
                document.getElementById('manual-help').classList.remove('active');
                document.getElementById(tab + '-help').classList.add('active');
            }
            
            async function verifyProduct(txHash) {
                if (!txHash) {
                    document.getElementById('verifyResult').innerHTML = 
                        '<div class="result error">Please provide a transaction hash</div>';
                    return;
                }
                
                document.getElementById('verifyResult').innerHTML = 
                    '<div class="result" style="background: #e3f2fd; color: #1565c0;">🔍 Verifying product...</div>';
                
                try {
                    const response = await fetch('/api/verify/' + txHash);
                    const data = await response.json();
                    
                    if (data.verified) {
                        document.getElementById('verifyResult').innerHTML = `
                            <div class="result success">
                                <h3>✅ Product Verified!</h3>
                                <div class="product-info">
                                    <h4>Product Information:</h4>
                                    <p><strong>Name:</strong> ${data.product.name}</p>
                                    <p><strong>Manufacturer:</strong> ${data.manufacturer}</p>
                                    <p><strong>Batch:</strong> ${data.product.batchNumber}</p>
                                    <p><strong>Serial:</strong> ${data.product.serialNumber || 'N/A'}</p>
                                    <p><strong>Description:</strong> ${data.product.description || 'N/A'}</p>
                                </div>
                                <div class="product-info">
                                    <h4>Blockchain Proof:</h4>
                                    <p><strong>Transaction:</strong> ${data.blockchain_proof.transaction_hash}</p>
                                    <p><strong>Block:</strong> ${data.block_number}</p>
                                    <p><strong>Network:</strong> ${data.blockchain_proof.network}</p>
                                    <p><strong>Status:</strong> ${data.blockchain_proof.confirmations}</p>
                                </div>
                            </div>
                        `;
                    } else {
                        document.getElementById('verifyResult').innerHTML = `
                            <div class="result error">
                                <h3>❌ Product Not Verified</h3>
                                <p>Error: ${data.error}</p>
                                <p>Transaction Hash: ${txHash}</p>
                            </div>
                        `;
                    }
                } catch (error) {
                    document.getElementById('verifyResult').innerHTML = 
                        '<div class="result error">❌ Error: ' + error.message + '</div>';
                }
            }
            
            // Manual form submission
            document.getElementById('verifyForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const txHash = document.getElementById('txHash').value.trim();
                verifyProduct(txHash);
            });
            
            // Cleanup on page unload
            window.addEventListener('beforeunload', function() {
                if (scanning) {
                    stopScanning();
                }
            });
        </script>
    </body>
    </html>
    '''

# API Routes
@app.route('/api/blockchain/status')
@login_required
def api_blockchain_status():
    return jsonify({
        'connected': blockchain_data['connected'],
        'current_block': blockchain_data['current_block'],
        'account': '0x1234567890abcdef',
        'balance': 10.0,
        'network': 'Simulated Blockchain'
    })

@app.route('/api/products', methods=['POST'])
@login_required
def api_register_product():
    try:
        product_data = request.get_json()
        
        if not product_data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Generate transaction hash
        tx_hash = '0x' + hashlib.sha256(
            (json.dumps(product_data, sort_keys=True) + str(datetime.now())).encode()
        ).hexdigest()
        
        # Store in blockchain
        blockchain_data['transactions'][tx_hash] = {
            'product_data': product_data,
            'timestamp': datetime.now().isoformat(),
            'block_number': blockchain_data['current_block'] + 1,
            'gas_used': 21000,
            'manufacturer': session['user']['company_name']
        }
        
        blockchain_data['current_block'] += 1
        
        return jsonify({
            'success': True,
            'transaction_hash': tx_hash,
            'block_number': blockchain_data['current_block'],
            'product_hash': tx_hash,
            'gas_used': 21000
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/verify/<transaction_hash>')
def api_verify_product(transaction_hash):
    try:
        if not transaction_hash.startswith('0x'):
            transaction_hash = '0x' + transaction_hash
            
        if transaction_hash in blockchain_data['transactions']:
            tx_data = blockchain_data['transactions'][transaction_hash]
            
            return jsonify({
                'verified': True,
                'product': tx_data['product_data'],
                'block_number': tx_data['block_number'],
                'timestamp': tx_data['timestamp'],
                'gas_used': tx_data['gas_used'],
                'manufacturer': tx_data['manufacturer'],
                'blockchain_proof': {
                    'transaction_hash': transaction_hash,
                    'network': 'Simulated Blockchain',
                    'confirmations': 'Confirmed'
                }
            })
        else:
            return jsonify({
                'verified': False,
                'error': 'Transaction not found',
                'transaction_hash': transaction_hash
            }), 404
            
    except Exception as e:
        return jsonify({'verified': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Fresh Product Authentication System")
    print("🔐 Login: admin / admin123")
    print("🌐 http://localhost:5000")
    print("✅ Clean code, no errors!")
    
    app.run(debug=True, port=5000, host='0.0.0.0')