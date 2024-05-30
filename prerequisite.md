### Docker
Follow the instructions in this [link](https://docs.docker.com/engine/install/). Alternatively, for ubuntu systems you can run the following commands

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
```bash
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world
```
```bash
# Post installation steps
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

### Docker compose
Follow the instructions in this [link](https://docs.docker.com/compose/install/), or run the following commands
```bash
wget https://github.com/docker/compose/releases/download/v2.24.3/docker-compose-linux-x86_64 -O /usr/bin/docker-compose
chmod +x /usr/bin/docker-compose 
which docker-compose 
```

## Install postgres
Follow the instructions in this [link](https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql-linux/), or run the following commands
```bash
sudo apt update
sudo apt install gnupg2 wget
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
sudo apt update
sudo apt install postgresql-16 postgresql-contrib-16
```
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```
```bash
sudo sed -i "s/^# listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/16/main/postgresql.conf
sudo sed -i '/^host/s/ident/md5/' /etc/postgresql/16/main/pg_hba.conf
sudo sed -i '/^local/s/peer/trust/' /etc/postgresql/16/main/pg_hba.conf
echo "host all all 0.0.0.0/0 md5" | sudo tee -a /etc/postgresql/16/main/pg_hba.conf
```
```bash
sudo systemctl restart postgresql
sudo ufw allow 5432/tcp
sudo -u postgres psql
```
```sql
ALTER USER postgres PASSWORD 'mypassword';
\q
```

### Python venv
For ubuntu run this command if the environment doesn't have venv
```bash
sudo apt install python3.10-venv
```
