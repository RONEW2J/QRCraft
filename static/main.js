document.getElementById('qrForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const generateBtn = document.getElementById('generateBtn');

    showLoading();
    generateBtn.disabled = true;
    generateBtn.textContent = 'Generating...';

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            showSuccess('QR code generated successfully!');
            displayQRCode(result.image, result.download_url, result.filename);
        } else {
            showError(result.error || 'Failed to generate QR code');
        }
    } catch (error) {
        showError('Network error. Please check your connection and try again.');
    } finally {
        hideLoading();
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate QR Code';
    }
});

function showLoading() {
    document.getElementById('loading').classList.add('show');
    document.getElementById('error').classList.remove('show');
    document.getElementById('success').classList.remove('show');
    document.getElementById('result').classList.remove('show');
}

function hideLoading() {
    document.getElementById('loading').classList.remove('show');
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('error').classList.add('show');
    document.getElementById('success').classList.remove('show');
}

function showSuccess(message) {
    document.getElementById('successMessage').textContent = message;
    document.getElementById('success').classList.add('show');
    document.getElementById('error').classList.remove('show');
}

function displayQRCode(imageData, downloadUrl, filename) {
    const qrPreview = document.getElementById('qrPreview');
    qrPreview.innerHTML = `<img src="${imageData}" alt="Generated QR Code">`;

    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.href = downloadUrl;
    downloadBtn.download = filename;

    document.getElementById('result').classList.add('show');

    document.getElementById('result').scrollIntoView({
        behavior: 'smooth',
        block: 'center'
    });
}

function resetForm() {
    document.getElementById('qrForm').reset();
    document.getElementById('result').classList.remove('show');
    document.getElementById('error').classList.remove('show');
    document.getElementById('success').classList.remove('show');

    // Reset color labels
    document.querySelector('#fill_color + span').textContent = 'Black';
    document.querySelector('#back_color + span').textContent = 'White';
}

// Update color labels dynamically
document.getElementById('fill_color').addEventListener('input', function() {
    this.nextElementSibling.textContent = this.value;
});

document.getElementById('back_color').addEventListener('input', function() {
    this.nextElementSibling.textContent = this.value;
});

const sampleData = [
    'https://www.google.com',
    'Hello World!',
    'Contact: +1-555-0123',
    'Email: example@email.com',
    'WiFi:T:WPA;S:MyNetwork;P:password123;;'
];

document.getElementById('data').addEventListener('focus', function() {
    if (!this.value) {
        this.placeholder = 'Try: ' + sampleData[Math.floor(Math.random() * sampleData.length)];
    }
});