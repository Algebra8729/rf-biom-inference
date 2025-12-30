# RF-Biom-Inference : Système d'Imagerie Passive par Perturbation RF 🛰️

### 🔬 Présentation du Projet
Ce projet est une preuve de concept (PoC) explorant les capacités des infrastructures WLAN existantes (IEEE 802.11n/ac) à agir comme des systèmes de radar passif.

En exploitant les données CSI (Channel State Information) extraites de la couche physique (PHY) du Wi-Fi, cet outil est capable de détecter la présence humaine et d'isoler des signatures biométriques (respiration) à travers des parois, sans contact visuel et sans caméras.

### 🛠️ Architecture du Système
Le projet repose sur une chaîne de traitement complète :

Hardware (Sensor) : Un microcontrôleur ESP32 configuré en mode sniffer pour l'extraction brute des trames CSI.

Firmware (Data Bridge) : Code C++ optimisé pour le streaming des sous-porteuses Wi-Fi vers l'interface série.

Software (Inference Engine) : Moteur de traitement de signal en Python utilisant des filtres de Butterworth et l'analyse spectrale (FFT).

### 🚀 Fonctionnalités
Analyse Multidimensionnelle : Monitoring simultané de 64 sous-porteuses Wi-Fi.

Détection de Présence : Analyse de la variance inter-porteuse pour identifier les mouvements.

Extraction Biométrique : Isolation des fréquences de micro-oscillations (0.15Hz - 0.5Hz) correspondant à la cage thoracique humaine.

Mode Hybride : Basculement automatique entre le streaming hardware réel et la simulation de laboratoire.

### 📋 Installation & Déploiement
Prérequis
Python 3.8+

Un ESP32 (S3 ou classique)

Bibliothèques : pip install numpy scipy pyserial

Utilisation
Flasher l'ESP32 avec le code situé dans /firmware/esp32_csi_sniffer.ino.

Brancher l'ESP32 en USB sur votre station de travail.

Lancer le moteur d'inférence :

Bash

python rf_biom_engine.py


### ⚠️ Implications
Cette recherche met en lumière deux vecteurs critiques :

Confidentialité : La possibilité de monitorer l'activité physique à l'intérieur de zones privées via l'infrastructure Wi-Fi In-Wall standard.

Sécurité : Une alternative non-intrusive aux caméras pour la surveillance de santé (détection de chute/malaise).
