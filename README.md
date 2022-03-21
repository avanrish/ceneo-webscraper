# Aplikacja do pobierania opinii z serwisu Ceneo.pl

## Instalacja

Przed przystąpieniem do pracy nad projektem należy wykonać kilka kroków:

```
git clone https://github.com/avanrish/ceneo-webscraper.git my-project
cd my-project
rm -r .git
pip install -r requirements.txt
mkdir output
mkdir products

# Bash
export FLASK_ENV=development
```

Jak już wszystko jest zainstalowane to trzeba w terminalu napisać `flask run`.