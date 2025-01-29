<?php
$host = 'db';
$dbname = 'ctf';
$username = 'readonly'; // Utilisateur en lecture seule
$password = 'readonlypass';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Connexion échouée : " . htmlspecialchars($e->getMessage()));
}
?>

