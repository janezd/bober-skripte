## Skripte za sestavljanje in pakiranje naloga za tekmovanje Bober

**Disclaimer (by Janez)**: te skripte sem na hitro napisal, ko sem jih potreboval. Določene grozne stvari (npr. inline css v vsaki nalogi) tudi niso moja ideja, temveč so podedovane iz predprejšnjega tekmovalnega sistema. Znal bi narediti tudi lepše. :)

**Popravki (by Alenka)**: Skripte za ustvarjanje nalog popravljene jeseni 2024 in ustrezno popravljena navodila.
**Popravki (by Alenka)**: Oktobra 2025 dodana skripta za ustvarjanje nalog, ki podatke o nalogah prebere iz csv datoteke ter ustvari vse naloge; ustrezno popravljena tudi navodila.


### Priprava skript in direktorijev

1. Ustvari poddirektorij, v katerem bodo naloge, na primer `solsko2025` ali `drzavno2025`. **Državno ima isto letnico kot šolsko, čeprav poteka v naslednjem koledarskem letu.**
2. V direktorij skopiraj task.css, da bodo naloge videti (približno) tako, kot bodo v sistemu.
3. Poberi vsebino tega repozitorija v direktorij, ki mora biti sosed direktorija `solsko2025`.
4. V preglednici z nalogami dodaj ID-je nalog. ID-je dobijo le naloge, ki jih damo v tekmovalni sistem, to je od 6. razreda dalje. (ID prve naloge naj ne bo 1 temveč 5, ker je to hkrati številka vrstice, sicer se boš stalno motil in prepisoval številke vrstic namesto ID-jev nalog.)

### Ustvarjanje naloge

1. Odpri terminal, pojdi v direktorij s skriptami.
2. Poženi `python ustvari.py`

    ```
    Naslov naloge: Bober preskuša kilave skripte
    Id naloge: 38
    Država: si
    Smer odgovorov [v/n/2]: v
    Število odgovorov: 5
    Pravilni odgovor [a/b/c/d/...]: b
    ```

    Podatki o nalogi:

    - Naslov naloge: videli ga bodo učenci, hkrati bo to ime direktorija
    - Id: prepiši iz preglednice.
    - Država: dvočrkovna koda. Uporabi se za zastavico.
    - Smer: `v` pomeni, da bodo odgovori vodoravno, `n`, da bodo navpično, `2` pa v tabeli v dveh vrsticah. Od tega je odvisno, kakšna oblika tabele bo v HTML. To je mogoče ročno spreminjati in narediti tabelo z več vrsticami ali pa prestavljati odgovore po vrsticah.
    - Število odgovorov: koliko je podanih odgovorov. Lahko jih je poljubno, tudi več kot 10 (vendar ne pretiravaj).
    - Pravilni odgovor: črka pravilnega odgovora.
        
    Vloga id-jev: skripta pripravi podano število odgovorov (v obliki `2` jih je število/2 v prvi vrstici, ostali v drugi vratici). Vsak odgovor ima id oblike `{leto}{id-naloge}{id-odgovora}`. Leta 21 imajo odgovori pri naloge 38 id-je 21381, 23182, ..., 21389, 213810, 213811 ... Če kot pravilni odgovor označimo `b`, bo v manifest.json za to nalogo zapisano, da je pravilni odgovor 21382 (črke so po vrsti po angleški abecedi).

3. ALTERNATIVA točki 2: pripravi csv datoteko s podatki o nalogah (ID	Naslov	Drzava	Smer_odg	St_odg	Pravilni), ločeni s tab (glej primer datoteke naloge.csv; podatke lahko copy-paste iz Excela v Notepad; pazi na kodiranje utf-8 in zapis šumnikov). ID naloge, ime naloge in državo dobiš iz preglednice z nalogami, dodati moraš še smer odgovorov (v/n/2), število odgovorov (int) in označen pravilni odgovor (a/b/c ...) - te poiščeš v knjižici s prevodi.
   Poženi `python ustvari_vse.py` (pred tem v datoteki ustvari_vse.py pravilno nastavi ime datoteke s podatki o nalogah) in ustvarile se bodo vse naloge glede na podatke iz datoteke.

4. Skripta je ustvarila nov poddirektorij znotraj `solsko{leto}` oz `drzavno{leto}`. V poddirektorij `resources` dodamo slike, nato pa urejamo `index.html`.

    - Slike vstavljamo z `<img src="resources/ime-slike.png">`. Navadno je dobra ideja `<img style="float: right; margin: 20px;" src="resources/ime-slike.png">`.
    - Namesto png je bolje uporabiti svg (večina slik je pripravljena kot svg), pri tem pa moramo sliki določiti velikost. Primeri vstavljanja slike so že v ustvarjenem index.html.
    - Če ima datoteka s sliko (png) preveliko ločljivost, jo zmanjšamo, da razbremenimo sistem.
    - Sicer je to običajen HTML, v katerega lahko dodajamo, kar hočemo. Tudi, npr. priložnostni `<style>` za oblikovanje kakšne tabele.
    
        Edina finta: če hočeš uporabljati `{` in `}` moraš pisati `{{` in `}}`. Opravičujem se, ker sem len.

### Ustvarjanje nalog v prevodu

Naloge za OŠ so lahko tudi v madžarščini ali italijanščini (če šola predhodno javi, da bi želeli prevode). Navodila so za madžarščino (če bi imeli še italijanščino, bi naredili podobno). Naloge v madžarščini imajo ID-je za 100 večje (npr. če ima slo naloga ID 5, ima hu naloga ID 105). Naloge v italijanščini naj imajo ID-je za 200 večje.
1. v direktoriju `solsko{leto}` oz `drzavno{leto}` kopiraj direktorij z nalogo in imenu dodaj predpono `hu-` (npr. "Sporočilo" --> "hu-Sporočilo"). Za italijanščino bi bila predpona "it-".
2. popravi manifest:
    - zamenjaj ID (25032 -> 25132)
    - popravi title (Naslov -> Naslov/HU Naslov)
3. popravi index.html:
    - zamenjaj title (Naslov -> Naslov/HU Naslov)
    - dodaj črto (<hr>) po zaključku prvega <div> v <body> (torej pred <form>)
    - za črto skopiraj cel prvi <div> ter slovensko besedilo zamenjaj z madžarskim
    - po potrebi dopolni odgovore z madžarskim besedilom

### Pakiranje nalog

0. Uredi si dostop do strežnika z nalogami. Potrebuješ ključ ssh.
1. V direktoriju z nalogami (npr. `solsko2025`, se pravi, direktoriju, katerega poddirektoriji vsebujejo posamične naloge) naredi datoteko `groups.txt` z vsebino takšne oblike:

    ```
    solsko-2025-razred_6_7  1,2,3,4,5,6,7,8,9,11,13,14,15,16,17
    solsko-2025-razred_8_9  3,10,11,12,13,14,15,17,18,19,20,21,22,23,24,26
    solsko-2025-srednja     10,13,18,19,20,21,22,23,25,26,27,28,29,30,31,32,33
    solsko-2025-razred_6_7-hu  101,102,103,104,105,106,107,108,109,111,113,114,115,116,117
    solsko-2025-razred_8_9-hu  103,110,111,112,113,114,115,117,118,119,120,121,122,123,124,126
    ```

    Imena tekmovanj so vedno takšne oblike. Znotraj imen ni presledkov. Naloge v madžarščini (oz. italijanščini) so kot ločeni tekmovalni razredi.
    **Pazi na pravilno poimenovanje skupin, prava letnica!**

2. Odpri terminal
3. `cd` v nek direktorij; za spodnji primer bo to `/Users/janez/Downloads/`.
4. Kloniraj repozitorij z nalogami.

   ```
   git clone ssh://acm-bober-2021.fri1.uni-lj.si/home/j/bober-naloge.git
   ```
5. V skripti `pakiraj.py` poišče `DEST_DIR =` in 
   - ustrezno spremeni direktorij, na primer `DEST_DIR = "/Users/janez/Downloads/bober-naloge/solsko2025"`
   - spremeni tudi direktorij dve vrstici nižje, v `chdir`.

6. `cd` nazaj v direktorij s skriptami. Tam poženi `python pakiraj.py`. Ta skopira direktorije z nalogami v repozitorij za git, poleg tega pa pripravi skripto `link_tasks`, ki bo na strežniku (ob hooku v git-u) pripravila poddirektorije za skupine in v njih simbolične povezave na naloge.

**PAZI:** skripta za pakiranje deluje na sistemu Linux, na Windows pa je problem s kodiranjem cp1252 in tudi s potmi do datotek, zato poskrbi, da jo poženeš v pravem okolju -- po potrebi kopiraj skripte in direktorij z nalogami (solsko2025 oz. drzavno2025) na sistem Linux, zapakiraj naloge ter prenesi zapakirane naloge nazaj na Windows.

7. Potisni naloge na strežnik. `cd` v direktorij `/Users/janez/Downloads/bober-naloge/` in tam:

   ```
   git add -A solsko2022/*  
   git commit -m "Solsko 2022: Naloge"
   git push
   ```

   (Disclaimer: avtor teh navodil v splošnem ne podpira in ne uporablja `add -A`. Ampak tole je poseben primer.)

   Če se ob tem uvažanju nalog po skupinah izpisuje napaka `Resource matching query does not exist.`, je vse OK.

8. Ker gornji korak, izgleda, ne naredi, kar bi moral, je potrebno (prvič?) ročno pognati nekaj stvari na strežniku. Pojdi torej na strežnik

   ```
   ssh j@acm-bober-2021.fri1.uni-lj.si
   ```

   potem pa:

   ```
   cd bober-naloge
   git pull
   cd solsko2022
   . link_tasks
   /home/bober/bober/django/bober/import_tasks_venv.sh
   ```

   Tisti `link_tasks` naredi poddirektorij `skupine` s poddirektoriji za tekmovanja, ki potem vsebujejo simbolične linke na naloge.

   Zadnja vrstica uvozi naloge v tekmovanje.

   **Če se kasneje izkaže, da v kakšnem tekmovanju manjka kakšna naloga, ali pa je kakšna napačna ali odveč,** je najbrž potrebno ponovno ročno zagnati `link_tasks`.

9. Ker tudi gornji korak, kot kaže, ne uvozi nalog, pišeš Polžu. :)
