# Klaviatuuri juhtimine
Hoonete valimine

Klaviatuuri abil saad valida, millist objekti ehitada:

- H – elamuala (House / Residential)

- S – äriala (Store / Commercial)

- F – tööstusala (Factory / Industrial)

- T – raekoda (Town Hall)
(saadaval ainult siis, kui linna seisund seda lubab)

- R – tee (Road)

Tee suuna muutmine

- ↑ / ↓ (UP / DOWN) – vahetab vertikaalse ja horisontaalse tee vahel

Muu

- ESC – sulgeb mängu kohe

# Hiire juhtimine

- Vasak hiirenupp (LMB) - Ehita valitud hoone kaardile

- Parem hiirenupp (RMB) - Eemalda hoone või objekt kaardilt

Ava Settings menüü, kui klikid ⚙️ ikoonile paremas ülanurgas


# Ekraanil kuvatav info (HUD)

Mängu ekraanil kuvatakse reaalajas järgmised andmed:

- Date – mängusisene kuupäev

- Money – linna raha

- Happiness – elanike õnnetase (%)

- Population – elanike arv

- City Profit – linna kasum tunnis

- Selected – hetkel valitud hoone

- Demand – elamu-, äri- ja tööstusnõudlus

# Projekti kirjeldus

See projekt on SimCity-stiilis linnasimulaator, mis on arendatud Pythonis, kasutades Arcade teeki. Mängija ehitab linna ruudustikupõhisel kaardil, paigutades erinevaid hooneid, hallates raha, elanikkonda, õnne (happiness) ja hoolduskulusid.

# Ehitus ja kaart
Linn koosneb grid-põhisest kaardist, iga ruut võib sisaldada ühte objekti

Hooneid saab:

- ehitada

- eemaldada

Ehitamine on piiratud kaardi suurusega

# Hoonete tüübid
House (elamud)

- Lisavad elanikkonda

- Mõjutavad linna õnne

Store (poed)

- Annavad tulu

- Parandavad õnne, eriti elamute läheduses

Factory (tehased)

- Annavad rohkem raha

- Vähendavad õnne, kui asuvad elamute lähedal

Road (teed)

- Struktuuri osa (hetkel lihtsustatud loogikaga)

Town Hall

- Oluline keskhoone

- Mõjutab üldist linna õnne

# Salvestamine ja laadimine

Linnaseisundit saab salvestada ja laadida, kuid see praegu ei tööta ideaalselt.

# Tulevikuplaanid (ideed)

- Rohkem hoonete tüüpe

- Animatsioonid

- Täpsem õnne ja saaste süsteem

- Parem salvestusstruktuur

- UI statistika paneel

- Tasakaalustatud progression

- Autod ja inimesed

