# Label maker - tvorba cenovek

> Tento projek je součástí navazujícího kurzu [pyladies Plzeň](https://pyladies.cz/plzen/).
> Možnosti vstupu, výstupu a chování aplikace je popsáno v [zadání](task.md).

## Popis projektu

Program, který usnadňuje práci při tvorbě štítků pro označení vzorků v laboratorí.

Uživatel zadá potřebné hodnoty, výsupem je pak tisknutelný soubor připravený k roztřížení/nalepení.

![ilustracni_foto_cedulky](_)

---

## Instalace

Momentálně je aplikace ve formě spustitelného python scriptu. Je tak potřeba mýt nainstalovaný python ve verzi 3.6 a
větší.
Pro instalaci je také doporučeno použít virtuální prostředí, například vestavěné `venv`.

Instalaci pythonu ověříte v příkazové řádce pomocí příkzu: `where.exe python`.

Poté v příkazové řádce instalujte pomocí následujících příkazů:

```commandline
git clone https://github.com/pyladies-pilsen/label-maker
cd label-maker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Spuštění

> Poznámka: Momentálně aplikace neumožňuje zadat cestu k csv souboru pomocí argumentu v příkazové řádce.