# Week 36 OCI Cloud Security Lab

## Del 1-2

## Del 3 – Logga in med SSH

- Whoami visar vem som användaren är loggad in i och i det här fallet "ubuntu".
- Hostname visar eller sätter systemets host name. i det här fallet "instance-20260903-0851"
- pwd visar i vilken katalog användaren befinner sig i.
- uname med option -a skriver ut all system information som kernel name, os version osv. "Linux instance-20260903-0851 7.0.0-1009-oracle #9-Ubuntu SMP PREEMPT Thu Jul 23 02:43:14 UTC 2026 x86_64 GNU/Linux"
- uptime skriver ut hur länge servern/sytemet varit igång. i mitt fall 09h:54m:32s

## Del 4 – Utforska Linux (Gäller alla!)
- ls -la :
Skriver ut en lista av alla filer incl osynsliga filer till terminalen.
Hotaktör kan en snabb få överblick för vad dem kan göra på systemet
ls -la ger en aktör överblick på rättigheter och ser hemliga filer, koppling till Konfidentialitet  
- whoami :
skriver ut användarnamner på användaren som är inloggad.
snabb blick på vad kontot kan ha för behörigheter.
Hotaktören får snabb koll på vilket konto dem har loggat in med och vad dem kan ha för behörgheter påverkar konfidentialitet
- date   : visar eller sätter systemets datum och tid. 
- id     : 
visar användare och grupp information för varje specifierad användare eller nuvarande användare.
Kan ge en hotaktör information om vilka användare som finns och vilka grupper dem tillhör för att veta vilka konton dem kan sikta på, konfidentialiteten utsätts för aktören får tillgång till lista av användera och deras gruppmedlemskap.
- groups :
skriver ut grupp medlemskap för varje användaren




## 1. Min OCI-miljö/Min lokala Linux-miljö/Min lokala WSL-miljö
- Tenancy (N/A):
- Compartment (Endast OCI): larshammarlund (root)
- Region (Endast OCI): eu-stockholm-1
- Availability Domain (Endast OCI): AD-1
- VM-namn/hostnamn/WSL-maskinnamn: instance-20260902-1210
- Operativsystem: Canonical Ubuntu 26.04
- Shape (Hårdvara, gäller alla): VM.Standard.E2.1.Micro | OCPU count 1 | Network bandwidth 0.48 | Memory 1GB | 50GB Storage
- Inloggningsmetod: SSH med key pair.
---
## 2. Linux-kommandon
| Kommando | Vad visar det? | CIA-koppling |
|-----------|-----------|-----------|
| whoami | visar användaren som är inloggad:"Ubunu" | medel koppling till C |
| hostname | visar eller skriver systemets host namn |  |
| pwd | skriver ut katalogen användaren befinner sig i | |
| uname -a | skriver ut all system information |  |
| uptime | beskriver hur länge systemet har körts  | |
---
## 3. Hardening
| Kontroll | Risk | Vad gjorde jag? | Hur verifierade jag? | CIA |
|-----------|-----------|-----------|-----------|-----------|
| Filrättigheter  |   | | | |
| Systemupdateringar  | | | | |
| ssh | | | | |
| Identitet och behörigheter  | | | | |

---
## 4. Recovery-plan
### Vad kan gå fel?
Kan inte komma åt server med ssh
### Hur upptäcker jag problemet?
Försöker logga in med ssh och ssh.key pair
### Vad kontrollerar jag först?
Att servern är uppe antingen genom att pinga eller kontrollera att instansen rapporterar "Running"
### Hur återställer jag åtkomst?
Kontrollera ssh porten och generera ett nytt ssh nyckelpar. 
### När behöver jag hjälp?
Om jag inte har behörigheter att interagera med servern fysiskt eller den virtuella Cloud panelen.

---
## 5. Backup
### Vad har jag sparat?
klon av instansen för rollback
### Vad finns i GitHub?
Documentering över server konfiguration, samt övriga markdownfiler
### Vad kan återskapas?
vid rollback som återgått till gammal konfiguration kan man konsultera konfiguration ducumenten som finns på GitHub och arbete kan upptas igen.
### Vad går inte att återskapa?
Odocumenterade konfigurationer och arbete som inte sparat och pushat till GitHub.

---
## 6. Cleanup
### VM-instans
Stoppad och terminerad
### Diskar

### Backuper
### Publika IP-adresser
### GitHub-evidens
---
## 7. CIA-reflektion
### Konfidentialitet
Rätt person har åtkomst till maskinen
### Integritet
Informationen finns när det behövs och att skulle något hända eller förstöras så finns en backup att falla tillbaka på
### Tillgänglighet
Servern eller maskinen är tillgängling när du behöver den, brandvägg rätt konfigurerad och du når med ssh.

---
## 8. Reflektion
### Vad fungerade bra?
Skapandet av Oracle instansen och uppkopplingen till maskinen med ssh
### Vad var svårt?
Stötte inte på några svårigheter under hela processen
### Vad lärde jag mig?
lärde mig skapa virtualla maskinen i molnet.

