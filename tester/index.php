<?php
/**
 * QR API Tester - PHP Proxy Simulation
 * Features: Multi-language support (FR/EN), Responsive Design, Secure API calling
 */

// 1. Configuration from Docker Environment Variables
$api_url = getenv('QR_API_URL');
$api_token = getenv('QR_API_TOKEN');

// 2. Language Management Logic
$i18n = [
    'fr' => [
        'title' => "Testeur de Microservice",
        'subtitle' => "Test de connexion vers l'hôte : <code>qrgen</code>",
        'form_title' => "Générer un QR via l'API",
        'label' => "Contenu à encoder :",
        'placeholder' => "Tapez un texte ou une URL...",
        'submit' => "Envoyer la requête",
        'success' => "Succès !",
        'msg' => "Image reçue via le proxy sécurisé :",
        'error_conn' => "La connexion a échoué. Vérifiez que les conteneurs sont sur le même réseau.",
        'switch' => "English"
    ],
    'en' => [
        'title' => "Microservice Tester",
        'subtitle' => "Testing connection to internal host: <code>qrgen</code>",
        'form_title' => "Generate QR via API",
        'label' => "Content to encode:",
        'placeholder' => "Type text or URL...",
        'submit' => "Submit Request",
        'success' => "Success!",
        'msg' => "Image received via secure proxy:",
        'error_conn' => "API connection failed. Ensure both containers are on the same Docker network.",
        'switch' => "Français"
    ]
];

// Determine language: URL parameter first, then Browser header, default to 'en'
$lang = $_GET['lang'] ?? (strpos($_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? '', 'fr') !== false ? 'fr' : 'en');
if (!array_key_exists($lang, $i18n)) { $lang = 'en'; }
$t = $i18n[$lang];

// 3. API Request Handling
$qr_base64 = null;
$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($_POST['data'])) {
    $text = $_POST['data'];
    
    // Construct the private API call (Internal Docker Network)
    $target = $api_url . "?token=" . $api_token . "&data=" . urlencode($text);
    
    // Server-to-server request
    $image_data = @file_get_contents($target);
    
    if ($image_data) {
        $qr_base64 = base64_encode($image_data);
    } else {
        $error = $t['error_conn'];
    }
}
?>
<!DOCTYPE html>
<html lang="<?php echo $lang; ?>">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $t['title']; ?></title>
    <link rel="stylesheet" href="https://unpkg.com/mvp.css">
    <style>
        :root { --accent: #118bee; }
        body { max-width: 800px; margin: 0 auto; padding: 20px; }
        .lang-switch { text-align: right; margin-bottom: 10px; }
        .result-box { text-align: center; margin-top: 20px; padding: 20px; border: 1px solid #eee; border-radius: 8px; }
        .error { color: #d00; background: #fff5f5; padding: 10px; border-radius: 4px; border: 1px solid #d00; }
        img { margin-top: 15px; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <div class="lang-switch">
        <a href="?lang=<?php echo $lang === 'fr' ? 'en' : 'fr'; ?>">
            <?php echo $t['switch']; ?>
        </a>
    </div>

    <header>
        <h1><?php echo $t['title']; ?></h1>
        <p><?php echo $t['subtitle']; ?></p>
    </header>

    <main>
        <section>
            <form method="POST" action="?lang=<?php echo $lang; ?>">
                <h2><?php echo $t['form_title']; ?></h2>
                <label><?php echo $t['label']; ?></label>
                <input type="text" name="data" placeholder="<?php echo $t['placeholder']; ?>" required>
                <button type="submit"><?php echo $t['submit']; ?></button>
            </form>
        </section>

        <?php if ($qr_base64): ?>
            <div class="result-box">
                <h3><?php echo $t['success']; ?></h3>
                <p><?php echo $t['msg']; ?></p>
                <img src="data:image/png;base64,<?php echo $qr_base64; ?>" alt="QR Code">
            </div>
        <?php endif; ?>

        <?php if ($error): ?>
            <div class="error">
                <strong>Error:</strong> <?php echo $error; ?>
            </div>
        <?php endif; ?>
    </main>
</body>
</html>
