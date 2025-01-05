## Skripte za sestavljanje in pakiranje naloga za tekmovanje Bober

**Disclaimer**: te skripte sem na hitro napisal, ko sem jih potreboval. Določene grozne stvari (npr. inline css v vsaki nalogi) tudi niso moja ideja, temveč so podedovane iz predprejšnjega tekmovalnega sistema. Znal bi narediti tudi lepše. :)

**Popravki (by Alenka)**: Skripte za ustvarjanje nalog popravljene jeseni 2024 in ustrezno popravljena navodila.

### Priprava skript in direktorijev

1. Ustvari poddirektorij, v katerem bodo naloge, na primer `solsko2022` ali `drzavno2025`. **Državno ima isto letnico kot šolsko, čeprav poteka v naslednjem koledarskem letu.**
2. V direktorij skopiraj task.css, da bodo naloge videti (približno) tako, kot bodo v sistemu.
3. Poberi vsebino tega repozitorija v direktorij, ki mora biti sosed direktorija `solsko2022`.
4. V preglednici z nalogami dodaj ID-je nalog. ID prve naloge naj ne bo 1 temveč 5, ker je to hkrati številka vrstice, sicer se boš stalno motil in prepisoval številke vrstic namesto ID-jev nalog.

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

4. Skripta je ustvarila nov poddirektorij znotraj `solsko{leto}` oz `drzavno{leto}`. V poddirektorij `resources` dodamo slike, nato pa urejamo `index.html`.

    - Slike vstavljamo z `<img src="resources/ime-slike.png">`. Navadno je dobra ideja `<img style="float: right; margin: 20px;" src="resources/ime-slike.png">`.
    - Če ima datoteka s sliko preveliko ločljivost, jo zmanjšamo, da razbremenimo sistem.
    - Vstavljamo lahko tudi SVG-je, pri čemer je seveda potrebno določiti velikost.
    - Sicer je to običajen HTML, v katerega lahko dodajamo, kar hočemo. Tudi, npr. priložnostni `<style>` za oblikovanje kakšne tabele.
    
        Edina finta: če hočeš uporabljati `{` in `}` moraš pisati `{{` in `}}`. Opravičujem se, ker sem len.


### Pakiranje nalog

0. Uredi si dostop do strežnika z nalogami. Potrebuješ ključ ssh.
1. V direktoriju z nalogami (npr. `solsko2022`, se pravi, direktoriju, katerega poddirektoriji vsebujejo posamične naloge) naredi datoteko `groups.txt` z vsebino takšne oblike:

    ```
    solsko-2018-razred_6_7  13,14,15,16,17,18,23,24,25,26,27,28,29,30,31
    solsko-2018-razred_8_9  13,14,15,23,24,25,26,27,28,29,30,32,33,34,35,36
    solsko-2018-srednja     23,24,25,26,27,32,33,34,35,36,37,38,39,40,41,42,43
    ```

    Imena tekmovanj so vedno takšne oblike. Znotraj imen ni presledkov.

2. Odpri terminal
3. `cd` v nek direktorij; za spodnji primer bo to `/Users/janez/Downloads/`.
4. Kloniraj repozitorij z nalogami.

   ```
   git clone ssh://acm-bober-2021.fri1.uni-lj.si/home/j/bober-naloge.git
   ```
5. V skripti `pakiraj.py` poišče `DEST_DIR =` in 
   - ustrezno spremeni direktorij, na primer `DEST_DIR = "/Users/janez/Downloads/bober-naloge/solsko2022"`
   - spremeni tudi direktorij dve vrstici nižje, v `chdir`.

6. `cd` nazaj v direktorij s skriptami. Tam poženi `python pakiraj.py`. Ta skopira direktorije z nalogami v repozitorij za git, poleg tega pa pripravi skripto `link_tasks`, ki bo na strežniku (ob hooku v git-u) pripravila poddirektorije za skupine in v njih simbolične povezave na naloge.

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
