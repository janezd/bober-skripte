## Skripte za sestavljanje in pakiranje naloga za tekmovanje Bober

**Disclaimer**: te skripte sem na hitro napisal, ko sem jih potreboval. Določene grozne stvari (npr. inline css v vsaki nalogi) tudi niso moja ideja, temveč so podedovane iz predprejšnjega tekmovalnega sistema. Znal bi narediti tudi lepše. :)

### Priprava skript in direktorijev

1. Ustvari poddirektorij, v katerem bodo naloge, na primer `solsko2022` ali `drzavno2025`. **Državno ima isto letnico kot šolsko, čeprav poteka v naslednjem koledarskem letu.**
2. Poberi vsebino tega repozitorija v direktorij, ki mora biti sosed direktorija `solsko2022`.
3. V `ustvari.py` poišči vrstico, ki se začne z `outdir = os.path.join("` in zamenjaj ime direktorija, npr `../solsko2022` z aktualnim.
4. V preglednici z nalogami dodaj ID-je nalog. ID prve naloge naj ne bo 1 temveč 5, ker je to hkrati številka vrstice, sicer se boš stalno motil in prepisoval številke vrstic namesto ID-jev nalog.

### Ustvarjanje naloge

1. Odpri terminal, pojdi v direktorij s skriptami.
2. Poženi `python ustvari.py`

    ```
    Naslov naloge: Bober preskuša kilave skripte
    Id naloge: 38
    Država: si
    Smer odgovorov [v/n/2]: v
    Pravilni odgovor [a/b/c/d/...]: b
    ```

    Podatki o nalogi:

    - Naslov naloge: videli ga bodo učenci, hkrati bo to ime direktorija
    - Id: prepiši iz preglednice.
    - Država: dvočrkovna koda. Uporabi se za zastavico.
    - Smer: `v` pomeni, da bodo odgovori vodoravno, `n`, da bodo navpično, `d` pa v tabeli 2x2. Od tega je odvisno, kakšna oblika tabele bo v HTML. To je mogoče ročno spreminjati.
    - Pravilni odgovor: črka pravilnega odgovora.
        
    Vloga id-jev: skripta pripravi 9 odgovorov (razen v obliki `2`). Vsak odgovor ima petmestni id oblike `{leto}{id-naloge}{id-odgovora}`. Leta 21 imajo odgovori pri naloge 38 id-je 21381, 23182, ..., 21389. Če kot pravilni odgovor označimo `b`, bo v manifest.json za to nalogo zapisano, da je pravilni odgovor 21382.

    Če ima naloga manj kot devet odgovorov, odvečne pobrišemo. Če jim ima več kot 9, dodamo nove odgovore in jim dodelimo poljubne idje, ki pa **morajo imeti pravilno letnico in id naloge. Če bi pri gornji nalogi dodali pet napačnih odgovorov, imajo lahko vsi id 21389, ali poljuben ID 2138X, razen 21382. Drugih števk ne smemo spreminjati; če bi šli naprej v 21390, 21391 ... bi bil 21391 lahko označen kot pravilni odgovor, če je `a` slučajno pravilni odgovor za nalogo 39.

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

6. Poženi `python pakiraj.py`. Ta skopira direktorije z nalogami v repozitorij za git, poleg tega pa pripravi skripto `link_tasks`, ki bo na strežniku (ob hooku v git-u) pripravila poddirektorije za skupine in v njih simbolične povezave na naloge.

7. Potisni naloge na strežnik.

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
   . solsko2022/link_tasks
   /home/bober/bober/django/bober/import_tasks_venv.sh
   ```

   Tisti `link_tasks` naredi poddirektorij `skupine` s poddirektoriji za tekmovanja, ki potem vsebujejo simbolične linke na naloge.

   Zadnja vrstica uvozi naloge v tekmovanje.

   **Če se kasneje izkaže, da v kakšnem tekmovanju manjka kakšna naloga, ali pa je kakšna napačna ali odveč,** je najbrž potrebno ponovno ročno zagnati `link_tasks`.

9. Ker tudi gornji korak, kot kaže, ne uvozi nalog, je morda potrebno napisati še 

    ```
    /usr/bin/docker exec -it production_web_1 /home/bober/bober/import_tasks.sh
    ```

    Vendar to nima nobenega pozitivnega učinka, ker `/usr/bin/docker: No such file or directory`.
