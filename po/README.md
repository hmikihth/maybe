In the folllowing examples I will use the hu_HU.UTF-8 language code. You
have to change it to your own language code.

----------
If you want to generate a totally new pot file use the following command:

```
xgettext maybe/*.py -o po/maybe.pot
```


----------
To generate a new po file for a new language:

```
msginit --locale=hu_HU.UTF-8 --input=maybe.pot
```

It generated the hu.po file.


----------
To update your po file you have to use the msgmerge:

```
msgmerge -N hu.po maybe.pot >new.po
mv new.po hu.po
```


----------
To create a new mo file:

```
msgfmt po/hu.po -o usr/share/locale/hu_HU/LC_MESSAGES/maybe.mo 
```
  
   or use the poedit

```
poedit hu.po
```
