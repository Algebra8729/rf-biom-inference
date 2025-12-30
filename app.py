import numpy as np
import scipy.signal as signal
from datetime import datetime
import time
import sys
import serial
import serial.tools.list_ports

class BiometricRFEngine:
    """
    Moteur d'inférence biométrique exploitant le CSI (Channel State Information).
    Analyse les micro-perturbations RF pour détecter présence et respiration.
    """
    def __init__(self, carriers=64, use_real_hw=False):
        self.carriers = carriers
        self.sampling_rate = 30  # Fréquence cible en Hz
        self.signal_buffer = []
        self.use_real_hw = use_real_hw
        self.ser = None
        
        # Configuration du filtre Butterworth : Bande passante [0.15Hz - 0.5Hz]
        # Correspond aux fréquences physiologiques de la respiration humaine.
        self.b, self.a = signal.butter(4, [0.15, 0.5], btype='bandpass', fs=self.sampling_rate)

        if self.use_real_hw:
            self._init_serial()

    def _init_serial(self):
        """Détection et ouverture automatique du port série."""
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            # Recherche des drivers USB-Série communs (CP210x, CH340, FTDI)
            if any(x in p.description for x in ["UART", "CP210", "CH340", "USB"]):
                try:
                    self.ser = serial.Serial(p.device, 115200, timeout=0.1)
                    print(f"[*] Hardware connecté sur {p.device}")
                    return
                except Exception as e:
                    print(f"[!] Erreur port {p.device}: {e}")
        print("[!] Aucun matériel détecté. Rebasculement en simulation.")
        self.use_real_hw = False

    def _get_frame(self):
        """Récupère une trame CSI réelle ou génère une simulation."""
        if self.use_real_hw and self.ser:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if "CSI_DATA" in line:
                    # Format attendu : "CSI_DATA,val1,val2,..."
                    vals = line.split(',')[1:]
                    return np.array([float(v) for v in vals[:self.carriers]])
            except:
                pass
        
        # Simulation (Bruit thermique + signature respiratoire cyclique)
        frame = np.random.normal(15, 0.1, self.carriers)
        t = time.time()
        if 10 < (t % 20) < 18:  # Simulation d'une présence toutes les 20s
            frame += np.sin(2 * np.pi * 0.3 * t) * 0.65
        return frame

    def extract_vitals(self):
        """Calcule la variance (mouvement) et l'énergie filtrée (biométrie)."""
        if len(self.signal_buffer) < 300:
            return 0, 0
        
        # 1. Analyse de la variance instantanée sur la dernière trame
        variance = np.var(self.signal_buffer[-1])
        
        # 2. Analyse temporelle sur le buffer (Fenêtre glissante)
        # Moyenne spatiale des porteuses pour isoler la composante temporelle
        temporal_signal = np.mean(self.signal_buffer, axis=1)
        
        # Application du filtre pour isoler la fréquence respiratoire
        filtered = signal.filtfilt(self.b, self.a, temporal_signal)
        
        # Énergie efficace (RMS) sur la fin du signal filtré
        energy = np.sum(filtered[-self.sampling_rate:]**2)
        
        return variance, energy

    def run_inference(self):
        print("--- RF-BIOM-INFERENCE ENGINE v2.0 ---")
        print(f"[{datetime.now()}] Initialisation...")
        print(f"[*] Mode : {'HARDWARE' if self.use_real_hw else 'SIMULATION'}")
        
        try:
            while True:
                start_time = time.time()
                
                raw_frame = self._get_frame()
                self.signal_buffer.append(raw_frame)
                
                # Maintien d'un buffer de 10 secondes (300 échantillons)
                if len(self.signal_buffer) > 300:
                    self.signal_buffer.pop(0)

                var, bio_energy = self.extract_vitals()

                # Logique de classification
                if var > 0.18:
                    state = "🚶 MOUVEMENT DÉTECTÉ              "
                    if bio_energy > 0.05: 
                        state = "🫁 BIOMÉTRIE ACTIVE (Sujet Statique)"
                else:
                    state = "⚪ ZONE VACANTE                   "

                # Interface Terminal
                sys.stdout.write(f"\r[RF-ID] Variance: {var:.4f} | Bio-Energy: {bio_energy:.6f} | {state}")
                sys.stdout.flush()
                
                # Régulation de la boucle
                elapsed = time.time() - start_time
                time.sleep(max(0, (1/self.sampling_rate) - elapsed))

        except KeyboardInterrupt:
            print("\n\n[!] Arrêt système.")
            if self.ser: self.ser.close()

if __name__ == "__main__":
    # Passer use_real_hw=True pour utiliser un ESP32/Intel 5300 flashé
    engine = BiometricRFEngine(use_real_hw=True)
    engine.run_inference()