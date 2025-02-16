#!/bin/bash

set -e # Arrête l'exécution en cas d'erreur

# Installation des paquets apt

echo "Installation des dépendances"

sudo apt udpate
sudo apt install -y postgresql libpq-dev python3-dev build-essential libpq-dev python3-pip python3-venv

echo "Dépendances installées avec succès"

################################
## Installation de PostgreSQL ##
################################

echo "Mise en place de la base de données PostgreSQL"

cd /tmp

# Créer l'utilisateur PostgreSQL avec mot de passe (non interactif)
sudo -u postgres psql <<EOF
DO \$\$ 
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_roles WHERE rolname = 'myuser'
   ) THEN
      CREATE ROLE myuser WITH LOGIN PASSWORD 'azerty';
      ALTER ROLE myuser CREATEDB;
   END IF;
END
\$\$;
EOF

# Créer la base de données
sudo -u postgres createdb domotique_test -O myuser

echo "Base de données installée avec succès"

############################
## Installation de RaspAP ##
############################

# Vérifier l'état de rfkill pour le Wi-Fi
echo "Vérification de l'état du Wi-Fi"
wifi_status=$(rfkill list wifi | grep -i "Soft blocked: yes")

if [[ -n "$wifi_status" ]]; then
    echo "Le Wi-Fi est désactivé. Réactivation en cours..."
    rfkill unblock wifi
    echo "Wi-Fi réactivé."
else
    echo "Le Wi-Fi est déjà activé."
fi

echo "Installation de RaspAP"

sudo cp /dev/null /etc/wpa_supplicant/wpa_supplicant.conf
echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1" | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf
wget -q https://git.io/voEUQ -O /tmp/raspap && bash /tmp/raspap --yes

# Ajouter le groupe 'hostapd' s'il n'existe pas déjà
echo "Création du groupe hostapd"
if getent group hostapd >/dev/null; then
    echo "Le groupe 'hostapd' existe déjà."
else
    echo "Création du groupe 'hostapd'..."
    sudo groupadd hostapd
fi

# Ajouter l'utilisateur actuel au groupe 'hostapd'
echo "Ajout de l'utilisateur $(whoami) au groupe 'hostapd'..."
sudo usermod -aG hostapd $(whoami)

# Modifier la ligne 'ctrl_interface_group=hostapd' dans /etc/hostapd/hostapd.conf
CONF_FILE="/etc/hostapd/hostapd.conf"
LINE_TO_SET="ctrl_interface_group=hostapd"

if grep -q "^ctrl_interface_group=" "$CONF_FILE"; then
    echo "Mise à jour de la ligne 'ctrl_interface_group' dans $CONF_FILE..."
    sudo sed -i "s/^ctrl_interface_group=.*/$LINE_TO_SET/" "$CONF_FILE"
else
    echo "Ajout de la ligne 'ctrl_interface_group=hostapd' dans $CONF_FILE..."
    echo "$LINE_TO_SET" | sudo tee -a "$CONF_FILE" >/dev/null
fi

############################
## Installation du projet ##
############################

echo "Initialisation du projet"

cd /home/user/home_automation_server/

# Installer les dépendances python dans le pyenv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Initialiser la base de données
python init_db.py

echo "Configuration terminée. Déconnecte-toi et reconnecte-toi pour que les changements de groupe prennent effet."
