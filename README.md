# home_automation_server

## Installation
Prérequis
```bash
apt install libpq-dev
```
Mise en place de l'environnement
```bash
git clone git@github.com:cfoowl/home_automation_server.git
cd home_automation_server
python -m venv .venv
source /.venv/bin/activate
pip install -r requirement.txt
python init_db.py
```
## Lancement
```bash
./main
```
## Remise à zéro du système
```bash
./reset.sh # Supprime la liste de baux DHCP et relance le hotspot wifi
python init_db.py # Remet à zéro la base de donnée
```