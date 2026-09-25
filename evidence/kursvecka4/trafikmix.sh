#!/usr/bin/env bash
# Trafikmix: skapar lite blandad nätverkstrafik (ICMP, DNS, HTTP, HTTPS)
# Syfte: ge något meningsfullt att analysera i Wireshark
# Körs på labbdatorn SAMTIDIGT som tcpdump spelar in
# Exempel: ./trafikmix.sh 3 # kör 3 varv
# "Säker" bash: avbryt vid fel, fel på odefinierad variabel, fel i piped kommandon
set -euo pipefail
##### 1) MÅL / INSTÄLLNINGAR #####
# Dessa kan eleven ändra fritt för att se skillnad i Wireshark
PING_HOST="8.8.8.8" # Google DNS (svarar på ping)
DNS_NAME="google.com" # Vanligt domännamn att slå upp
HTTP_URL="http://google.com" # Okrypterad HTTP (synlig i klartext)
HTTPS_URL="https://google.com" # Krypterad HTTPS (inte läsbar payload)
##### 2) HJÄLPFUNKTIONER #####
# Enkel loggfunktion som skriver tid + meddelande
log(){ printf "[%s] %s\n" "$(date +%H:%M:%S)" "$*"; }
# Kontrollera att ett kommando finns, annars tipsa om installation
need() {
if ! command -v "$1" >/dev/null 2>&1; then
echo "Saknar '$1' – installera det först. Exempel (Rocky): sudo dnf install -y $2"
exit 1
fi
}
##### 3) FÖRKONTROLLER #####
# Verifiera att de verktyg vi använder finns
need ping "iputils"
# DNS: vi accepterar antingen 'dig' (bind-utils) eller 'nslookup'
if ! command -v dig >/dev/null 2>&1 && ! command -v nslookup >/dev/null 2>&1; then
echo "Saknar 'dig' eller 'nslookup' – installera bind-utils: sudo dnf install -y bind-utils"
exit 1
fi
need curl "curl"
sudo resolvectl flush-caches
##### 4) ANTAL VARV #####
# Eleven kan ange hur många "varv" av trafik som ska skapas
# Ex: ./trafikmix.sh 5 -> kör 5 varv
rounds="${1:-1}" # default 1 varv om inget argument anges

##### 5) HUVUDLOOP – SKAPA TRAFIK #####
for i in $(seq 1 "$rounds"); do
log "Varv $i: ICMP (ping) → $PING_HOST"

# -c 4 = skicka 4 ping. Vi slänger outputen (>/dev/null) för att inte skräpa i terminalen.
# '|| true' gör att skriptet inte avbryts om ping råkar misslyckas
ping -c 4 "$PING_HOST" >/dev/null || true
log "Varv $i: DNS (fråga) → $DNS_NAME"

# Kör 'dig' om det finns, annars 'nslookup'. Timeout kort för att inte fastna.
if command -v dig >/dev/null; then
dig +time=2 +tries=1 "$DNS_NAME" >/dev/null || true
else
nslookup "$DNS_NAME" >/dev/null || true
fi
log "Varv $i: HTTP (okrypterad) → $HTTP_URL"

# -m 5 = timeout 5 sek, -sS = tyst men visa fel, -o /dev/null = kasta innehållet
curl -m 5 -sS -o /dev/null "$HTTP_URL" || true
log "Varv $i: HTTPS (krypterad) → $HTTPS_URL"
curl -m 5 -sS -o /dev/null "$HTTPS_URL" || true
# Kort paus bara för att separera varv i tidslinjen
sleep 1
done
log "Färdig trafikmix."
