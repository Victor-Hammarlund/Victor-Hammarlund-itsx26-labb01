# 01 Riskbedömning

## Instruktion

Välj minst tre observationer från labben. Beskriv varje observation, koppla den till CIA-triaden och föreslå en rimlig åtgärd.

| Observation | Påverkan på CIA | Riskbeskrivning | Föreslagen åtgärd | Prioritet |
|---|---|---|---|---|
| Exempel: debug-läge aktiverat | Konfidentialitet, riktighet | Debug kan exponera teknisk information | Säkerställ att debug är false i labbkonfig | Medel |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

## Reflektion

Beskriv kort hur du prioriterade riskerna.

### main.py 
- - - - - - - 
#### Observationer:
1. Dubug mode exponerar systemets användarnamn och paths:
   
    Att användarnamnet och paths exponeras i debugmode gör inte programet sårbart, eftersom det körs lokalt. låg till ingen CIA påverkan.

    Åtgärd: Stäng av debug-mode.

   ##### Prioritet : LÅG-MEDEL

1. programmet tar ingen input från användaren:
  
    Den tar ingen input av personen som kör programmet,
    låg till ingen CIA påverkan 

    Åtgärd: Ingen åtgärd nödvändig.

    ##### Prioritet : LÅG

2. ingen information exoneras när koden körs vanligt:
  
    Vid program körning produceras ingen information till terminalen som skulle göra systemet eller användaren sårbar för något hot. Låg till ingen CIA påverkan

    Åtgärd: Ingen åtgärd nödvändig.

    ##### Prioritet : LÅG

3. Programmet ändrar inte på några filer:
   
    Programet utsätter inte någon påverkam gällande integritet, systemetets riktighet är oberörd.

    Åtgärd: Ingen åtgärd nödvändig.

    ##### Prioritet : LÅG

