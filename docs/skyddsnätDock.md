# Skyddsnätet

## Vad har jag på systemet

- document
- konfigurationsfiler
-konfigurationsdokument.
- script

## Hur säkerställer jag att jag kan göra en återställning

- document, script och annan ej känsligt/hemligt  arbete laddas upp till GitHub
- Snapshot görs av systemet och sparar ev konfigurationer

## Verify
- manual inspektion av systemkonfig och dokument
- journalctl visar rätt loggar


## cleanup

- cloud miljön termineras och ev storage block raderas samt ip regler


## Summery

allt arbete som inte är hemligt laddas upp till GitHub plus system konfigurationsdokument
om 100% återställning av systemet önskas. samt recovery snapshot görs genom Oracle cloud

