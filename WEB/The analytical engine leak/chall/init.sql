-- Se connecter en root pour s'assurer que nous avons les permissions nécessaires
USE mysql;

-- Assurer que root a tous les privilèges
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'rootpass' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS ctf;
USE ctf;

-- Création de la table et insertion de données
CREATE TABLE blueprints (
    id INT AUTO_INCREMENT PRIMARY KEY,   
    username VARCHAR(255) NOT NULL,  
    password VARCHAR(255) NOT NULL,  
    is_encrypted VARCHAR(255) DEFAULT 'Encrypted file: ACCESS_DENIED',
    file_name VARCHAR(255) NOT NULL,    
    description TEXT DEFAULT NULL
);

INSERT INTO blueprints (username, password, is_encrypted, file_name, description) VALUES 
('admin', 'admin123', 'Encrypted file: ACCESS_DENIED', 'steam_decoder_plan.txt', 'Critical file for the Analytical Machine project'),
('engineer', 'eng1pass', 'Encrypted file: ACCESS_DENIED', 'defense_layout.pdf', 'Plans for the defense system, requiring elevated privileges'),
('researcher', 'researcher42', 'Encrypted file: ACCESS_DENIED', 'steam_chimney_optimization.docx', 'Designs to optimize the steam chimneys'),
('cipher', 'rootpass', 'Encrypted file: ACCESS_DENIED', 'secret_key.txt', 'W5HWRxWbZM7AUhxgfRwZg58ANQFKgMwutG'),
('guest', 'guestpass', 'Encrypted file: ACCESS_DENIED', 'old_blueprint_archive.bin', 'Historical data with no critical value'),
('engineer2', 'eng2secure', 'Encrypted file: ACCESS_DENIED', 'obsolete_schematics.pdf', 'Outdated designs for machine components'),
('archivist', 'archivist77', 'Encrypted file: ACCESS_DENIED', 'miscellaneous_archives.txt', 'Assorted data files dating back to the 1940s');

-- Création de l'utilisateur en lecture seule
CREATE USER IF NOT EXISTS 'readonly'@'%' IDENTIFIED BY 'readonlypass';
GRANT SELECT ON ctf.* TO 'readonly'@'%';
FLUSH PRIVILEGES;

