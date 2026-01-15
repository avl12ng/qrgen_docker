# Secure QR Code Generator (Dockerized)

A lightweight, responsive, and multilingual web interface to generate QR codes. Built with Python (Flask), this tool supports single generation, batch processing (CSV/TXT), and features a secured API for external integrations.

## 🚀 Features

- **Batch Generation**: Upload `.txt` or `.csv` files to get a `.zip` containing multiple QR codes.
- **One-Click Deployment**: Automated bash script to handle network creation, builds, and container management.
- **Secured API**: Dedicated `/api/generate` endpoint protected by a mandatory token.
- **Microservice Architecture**: Fully isolated environments using a dedicated Docker bridge network.
- **Environment Driven**: Configuration managed via `.env` for better security.
- **Responsive Web UI**: Built with MVP.css for a clean look on desktop and mobile.
- **Multilingual Support**: Automatic detection (EN/FR) with a manual language switcher.

📦 Project Structure
```plaintext
.
├── app_qrgen.py           # Core Python/Flask Generator
├── Dockerfile             # Generator container configuration
├── requirements.txt       # Python dependencies
├── qrgen_docker_build.sh  # Automated deployment script
├── .env.example           # Template for environment variables
├── .gitignore             # Git exclusion rules
├── LICENSE                # MIT License
└── tester/                # API Testing Microservice
    ├── index.php          # Bilingual PHP Test Interface
    └── Dockerfile         # Tester container configuration
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/avl12ng/qrgen_docker.git
cd qrgen_docker
```

### 2. Configure Environment Variables

Create your environment file based on the template:
```bash
cp .env.example .env
```

Edit .env and set your API_TOKEN and preferred ports
```plaintext
API_TOKEN=your_very_secret_token_here
PORT_GEN=5050
PORT_TESTER=8081
```

### 3. Deployment

Run the master build script. It will automatically create the qrgen-network and start qrgen and qrgen-tester services.
Use the provided automation script:
```bash
chmod +x qrgen_docker_build.sh
./qrgen_docker_build.sh
```

🔌 API Integration

To use the generator from another website (e.g., PHP or JS) without exposing your secret token, use a backend proxy.
The generator provides a secure endpoint at GET /api/generate.

Endpoint: GET /api/generate?data=YOUR_TEXT&token=YOUR_TOKEN

Required Parameters:

- data: The text or URL to encode.
- token: Must match the API_TOKEN defined in your .env.

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

Backend Proxy Example (PHP): The included tester demonstrates how to call the API from your server-side code to hide the secret token from the end-user's browser.

🔒 Security

- The .env file is ignored by Git to prevent secret leaks.
- Internal communication between containers happens over a private Docker network.
- Cross-Origin Resource Sharing (CORS) is enabled for flexible integration.
- In-memory processing: No images are stored on the server disk.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
