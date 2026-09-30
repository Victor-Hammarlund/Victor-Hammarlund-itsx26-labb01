a) Fakta och antaganden

Fakta

Ett välskrivet mejl har skickats till skoladministrationen.
Mejlet verkar komma från en betrodd intern avsändare.
Mejlet uppmanar mottagaren att klicka på en länk för att uppdatera ett konto.
Det är okänt om mejlet är legitimt eller phishing.
Det är inte fastställt om AI har använts för att skapa mejlet.

Antaganden

- Avsändaren är verkligen en intern medarbetare.
- Kontot behöver uppdateras.
- Länken leder till en legitim inloggningssida.
- Mejlet är ett phishingförsök.
- AI har använts för att göra phishingförsöket mer      trovärdigt.

b) Tillgångar och CIA-dimensioner
Tillgångar
Skolans identitets- och kontohanteringssystem
Elevregister
Personuppgifter om elever och vårdnadshavare
Personalregister
E-postsystem
Dokument- och lärplattformar
Administrativa system för betyg, frånvaro och schema
CIA
Dimension	Möjlig påverkanKonfidentialitet	Angriparen kan få tillgång till elev- och personaluppgifter.
Riktighet (Integrity)	Betyg, kontaktuppgifter eller administrativa uppgifter kan ändras.
Tillgänglighet	System eller konton kan låsas eller användas för ransomware-angrepp.

I detta scenario är konfidentialitet ofta den mest kritiska dimensionen eftersom skoladministrationen behandlar personuppgifter, men även riktighet är viktig då felaktiga elevuppgifter eller betyg kan få stora konsekvenser.

c) Relevanta CIS Controls

CIS Control 5 – Account Management

Skydd av användarkonton.
Rutiner för hantering av komprometterade konton.

CIS Control 6 – Access Control Management

MFA.
Principen om minsta privilegium.

CIS Control 9 – Email and Web Browser Protections

Skydd mot phishing.
Filtrering av länkar och bilagor.

CIS Control 14 – Security Awareness and Skills Training

Utbildning av skoladministratörer om phishing och social engineering.

CIS Control 8 – Audit Log Management

Loggning av inloggningar och kontoändringar.

CIS Control 13 – Network Monitoring and Defense

Upptäckt av kommunikation med skadliga webbplatser.
d) Förebyggande och upptäckande åtgärd
Förebyggande åtgärd

Införa MFA och utbilda personal att verifiera kontoändringsbegäranden via en separat kanal.

Exempel:

Om ett mejl begär kontoåtgärder ska användaren kontakta IT-avdelningen eller avsändaren via telefon eller intern chatt innan länken används.
Upptäckande åtgärd

Övervakning av inloggnings- och kontologgar med larm vid avvikande aktiviteter.

Exempel:

Inloggning från okänd plats.
Inloggning på ovanlig tid.
Flera misslyckade inloggningsförsök.
Kontoändringar direkt efter klick på en länk i e-post.