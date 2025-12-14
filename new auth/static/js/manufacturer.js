// Manufacturer portal functionality
class ManufacturerApp {
    constructor() {
        this.config = {};
        this.init();
    }

    async init() {
        await this.loadConfig();
        this.setupEventListeners();
        this.loadProducts();
    }

    async loadConfig() {
        try {
            const response = await fetch('/api/config');
            this.config = await response.json();
            
            // Apply company branding
            this.applyBranding();
        } catch (error) {
            console.error('Failed to load config:', error);
        }
    }

    applyBranding() {
        const root = document.documentElement;
        root.style.setProperty('--company-primary', this.config.branding.primary_color);
        root.style.setProperty('--company-secondary', this.config.branding.secondary_color);
        root.style.setProperty('--company-accent', this.config.branding.accent_color);
    }

    setupEventListeners() {
        document.getElementById('productForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.registerProduct();
        });
    }

    async registerProduct() {
        const formData = new FormData(document.getElementById('productForm'));
        const productData = {};
        
        for (let [key, value] of formData.entries()) {
            productData[key] = value;
        }

        // Add compliance fields
        this.config.compliance.required_fields.forEach(field => {
            const element = document.getElementById(field);
            if (element) {
                productData[field] = element.value;
            }
        });

        try {
            const response = await fetch('/api/products', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData)
            });

            const result = await response.json();

            if (result.success) {
                this.showRegistrationSuccess(result);
                this.loadProducts();
                document.getElementById('productForm').reset();
            } else {
                this.showError('Registration failed');
            }
        } catch (error) {
            this.showError('Registration error: ' + error.message);
        }
    }

    showRegistrationSuccess(result) {
        const resultDiv = document.getElementById('registrationResult');
        resultDiv.innerHTML = `
            <div class="success-message">
                ✅ Product registered successfully!<br>
                Product ID: ${result.product_id}
            </div>
        `;

        // Show QR code
        this.displayQRCode(result.qr_code, result.product_id);
    }

    displayQRCode(qrData, productId) {
        const qrSection = document.getElementById('qrSection');
        const qrDisplay = document.getElementById('qrDisplay');
        
        qrDisplay.innerHTML = `
            <div class="qr-container">
                <h3>Product ID: ${productId}</h3>
                <img src="${qrData}" alt="QR Code" class="qr-image">
                <div class="qr-actions">
                    <button onclick="downloadQR('${qrData}', ${productId})">💾 Download</button>
                    <button onclick="printQR()">🖨️ Print</button>
                </div>
            </div>
        `;
        
        qrSection.style.display = 'block';
    }

    async loadProducts() {
        try {
            const response = await fetch('/api/products');
            const products = await response.json();
            
            this.displayProducts(products);
        } catch (error) {
            console.error('Failed to load products:', error);
        }
    }

    displayProducts(products) {
        const productsList = document.getElementById('productsList');
        
        if (products.length === 0) {
            productsList.innerHTML = '<p>No products registered yet.</p>';
            return;
        }

        const productsHTML = products.map(product => `
            <div class="product-item">
                <h4>${product.productName || product.name} (ID: ${product.id})</h4>
                <p><strong>Batch:</strong> ${product.batchNumber}</p>
                <p><strong>Serial:</strong> ${product.serialNumber || 'N/A'}</p>
                <p><strong>Registered:</strong> ${new Date(product.registration_time).toLocaleString()}</p>
                <button onclick="regenerateQR(${product.id})">🎯 Regenerate QR</button>
            </div>
        `).join('');

        productsList.innerHTML = `<div class="products-grid">${productsHTML}</div>`;
    }

    showError(message) {
        const resultDiv = document.getElementById('registrationResult');
        resultDiv.innerHTML = `<div class="error-message">❌ ${message}</div>`;
    }
}

// Global functions
function downloadQR(qrData, productId) {
    const link = document.createElement('a');
    link.download = `product-${productId}-qr.png`;
    link.href = qrData;
    link.click();
}

function printQR() {
    window.print();
}

function regenerateQR(productId) {
    // Implementation for QR regeneration
    console.log('Regenerating QR for product:', productId);
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ManufacturerApp();
});