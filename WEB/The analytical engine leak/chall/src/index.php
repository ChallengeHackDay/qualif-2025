<?php
include "db.php";

// Mécanisme anti-automatisation : blocage des User-Agent suspects
if (isset($_SERVER['HTTP_USER_AGENT'])) {
    $user_agent = strtolower($_SERVER['HTTP_USER_AGENT']);
    $blacklisted_agents = ['sqlmap', 'python', 'scanner'];

    foreach ($blacklisted_agents as $agent) {
        if (strpos($user_agent, $agent) !== false) {
            die("Automation - Forbidden Access.");
        }
    }
}

// Mécanisme anti-automatisation : ajout d'un délai aléatoire pour ralentir les tests
usleep(rand(500000, 1200000)); // Délai entre 0.5s et 1.2s

$output = ""; // Stockage des résultats ou erreurs

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    try {
        // Requête de base : Injection SQL possible ici
        $query = "SELECT id, username, password FROM blueprints WHERE username = '$username' AND password = '$password'";
        
        // Exécution de la requête
        $result = $pdo->query($query);
        $count = $result->rowCount();

        // Gestion de l'affichage des erreurs
        if ($count > 0) {
            while ($row = $result->fetch()) {
                // Vérification avant htmlspecialchars pour éviter le problème avec null
                $id = isset($row['id']) ? htmlspecialchars($row['id']) : " ";
                $username = isset($row['username']) ? htmlspecialchars($row['username']) : " ";

                $output .= "<p>$id  $username</p>";
            }
        } else {
            $output = "<p>Not found in the DB.</p>";
        }
    } catch (PDOException $e) {
        // Vérifier si une erreur a déjà été affichée
        static $errorDisplayed = false; 
        if (!$errorDisplayed) {
            $output = "<p>Erreur SQL : " . htmlspecialchars($e->getMessage()) . "</p>";
            $errorDisplayed = true; // Empêcher d'afficher plus d'une erreur
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" "href="favicon.ico">
    <title>The Analytical Engine Leak</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="container">
        <h1>🧭🔧 The Analytical Engine Leak 🔩🔐</h1>
        <p class="instructions">
            The Black Mist has infiltrated the Steam Station archives.            
            You must extract the key that will decode the stolen plans of the Analytical Machine before they disappear!  
        </p>
        
        <div class="terminal">
            <p>>> Connection to server in progress...</p>
	    <p>>> Database ready.
            <p>>> Restricted access. Authentication required.</p>
            <form method="POST">
                <label>>> Username:</label>
                <input type="text" name="username" required><br>
                <label>>> Password:</label>
                <input type="password" name="password" required><br>
                <button type="submit">Connect</button>
            </form>
        </div>

        <!-- Affichage des résultats sous le formulaire -->
        <div class="results">
            <?= $output; ?>
        </div>
    </div>

    <footer>
        <p>⚙ Hackday - Steampunk CTF ⚙</p>
    </footer>

</body>
</html>


