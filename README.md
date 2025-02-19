# home_automation_server

## Installation

Le script d'installation est conçu pour une installation minimale de Raspberry Pi OS Lite (64 bits). Le but est d'effectuer l'installation directement après avoir flashé l'OS sur la carte SD et avoir démarré le raspberry pour la première fois.

```
sudo apt install git -y
cd ~
git clone https://github.com/cfoowl/home_automation_server.git
cd home_automation_server
./install.sh
```

### Troubleshooting

Si au démarrage du raspberry vous avez toujours un message qui dit que le wifi est bloqué par rfkill, faire :

```bash
sudo rfkill unblock wifi
```

## Utilisation du serveur

```bash
./main
```

## Remise à zéro du système

```bash
./reset.sh # Supprime la liste de baux DHCP et relance le hotspot wifi
python init_db.py # Remet à zéro la base de donnée
```

