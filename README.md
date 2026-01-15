# Secure QR Code Generator (Dockerized)

A lightweight, responsive, and multilingual web interface to generate QR codes. Built with Python (Flask), this tool supports single generation, batch processing (CSV/TXT), and features a secured API for external integrations.

## 🚀 Features

- **Responsive Web UI**: Built with MVP.css for a clean look on desktop and mobile.
- **Multilingual Support**: Automatic detection (EN/FR) with a manual language switcher.
- **Batch Generation**: Upload `.txt` or `.csv` files to get a `.zip` containing multiple QR codes.
- **Secured API**: Dedicated `/api/generate` endpoint protected by a mandatory token.
- **Environment Driven**: Configuration managed via `.env` for better security.
- **Developer Tools**: Includes a bash script for automated build and redeployment.

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/avl12ng/qrgen_docker.git
cd qrgen_docker
```

### 2. Configure Environment Variables

Create a .env file in the root directory:
```env
API_TOKEN=your_very_secret_token_here
PORT=5050
```

### 3. Build and Run

Use the provided automation script:
```bash
chmod +x qrgen_docker_build.sh
./qrgen_docker_build.sh
```

🔌 API Integration

To use the generator from another website (e.g., PHP or JS) without exposing your secret token, use a backend proxy.

Endpoint: GET /api/generate?data=YOUR_TEXT&token=YOUR_TOKEN

Example with PHP
```php
<?php
$data = "https://github.com";
$token = "your_secret_token_here";
$api_url = "http://your-server-ip:5050/api/generate?data=" . urlencode($data) . "&token=" . $token;

$image = file_get_contents($api_url);
header("Content-Type: image/png");
echo $image;
?>
```

📦 Project Structure
```plaintext
.
├── app_qrgen.py             # Main Flask application
├── Dockerfile               # Container configuration
├── requirements.txt         # Python dependencies
├── qrgen_docker_build.sh    # Build & Deploy automation script
├── .env.example             # Example configuration file
├── .gitignore               # Files excluded from Git
└── README.md                # Documentation
```

🔒 Security

The .env file is ignored by Git to prevent secret leaks.

Cross-Origin Resource Sharing (CORS) is enabled for flexible integration.

In-memory processing: No images are stored on the server disk.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
