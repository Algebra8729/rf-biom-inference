#include "esp_wifi.h"
#include "esp_wifi_types.h"
#include "esp_system.h"
#include "Arduino.h"

void csi_cb(void *ctx, wifi_csi_info_t *data) {
    wifi_csi_info_t *csi_info = data;
    int8_t *csi_data = (int8_t *)csi_info->buf;

    Serial.print("CSI_DATA");
    for (int i = 0; i < csi_info->len; i++) {
        Serial.print(",");
        Serial.print(csi_data[i]);
    }
    Serial.println();
}

void setup() {
    Serial.begin(115200);
    
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);
    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_start();

    wifi_csi_config_t csi_config = {
        .filter_mask = WIFI_CSI_FILTER_MASK_ALL, // On écoute tout
    };
    esp_wifi_set_csi_config(&csi_config);
    esp_wifi_set_csi_rx_cb(csi_cb, NULL);
    esp_wifi_set_csi(true);
    
    Serial.println("[*] ESP32 Radar Initialisé. Envoi des trames CSI...");
}

void loop() {
    delay(10);
}