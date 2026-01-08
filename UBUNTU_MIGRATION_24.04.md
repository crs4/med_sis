# Guida alla Migrazione a Ubuntu 24.04

Questo documento descrive i passaggi necessari per migrare il sistema da Ubuntu 22.04 a Ubuntu 24.04 utilizzando il nuovo Dockerfile basato su `geonode/geonode-base:latest-ubuntu-24.04`.

## ⚠️ IMPORTANTE: Differenze tra il Dockerfile nuovo e quello attuale

Il Dockerfile fornito dal repository GeoNode ha alcune differenze rispetto alla configurazione attuale:

1. **Path del progetto**: Il nuovo Dockerfile usa `/usr/src/geonode` ma il tuo progetto si chiama `s4m_catalogue`, quindi **devi mantenere il path `/usr/src/s4m_catalogue`**
2. **Porta**: Il nuovo Dockerfile espone la porta `8000` invece di `8088`
3. **Pacchetti apt**: Il nuovo Dockerfile non installa pacchetti aggiuntivi (saga, cron, spatialite, ecc.) che potrebbero essere necessari
4. **Configurazione locale**: Il nuovo Dockerfile non configura le locale
5. **Cron job**: Il nuovo Dockerfile non configura il cron job per backoffice

## 📋 Piano di Migrazione

### Opzione 1: Mantenere la porta 8088 (CONSIGLIATO)

Se vuoi mantenere la porta 8088 (per evitare modifiche estese), usa il file `Dockerfile.new` che ho creato, che:
- Usa Ubuntu 24.04
- Mantiene il path `/usr/src/s4m_catalogue`
- Mantiene tutti i pacchetti necessari
- Mantiene la porta 8088
- Mantiene il cron job

**Passaggi:**
1. Sostituisci il Dockerfile attuale con `Dockerfile.new`
2. **Nessuna altra modifica necessaria** - tutto continuerà a funzionare

### Opzione 2: Cambiare la porta a 8000

Se vuoi allinearti completamente al nuovo Dockerfile e cambiare la porta a 8000, devi modificare:

#### 1. File da modificare per la porta 8000:

**docker-compose.yml** (linee 29, 38):
```yaml
# Cambia da:
test: "curl -m 10 --fail --silent --write-out 'HTTP CODE : %{http_code}\n' --output /dev/null http://django:8088/"
command: "python manage.py runserver 0.0.0.0:8088"

# A:
test: "curl -m 10 --fail --silent --write-out 'HTTP CODE : %{http_code}\n' --output /dev/null http://django:8000/"
command: "python manage.py runserver 0.0.0.0:8000"
```

**docker-compose_dev.yml** (linee 29, 38):
```yaml
# Stesse modifiche di docker-compose.yml
```

**src/uwsgi.ini** (linea 3):
```ini
# Cambia da:
http-socket = 0.0.0.0:8088

# A:
http-socket = 0.0.0.0:8000
```

**src/uwsgi.ini.prod** (se presente, stessa modifica)

**src/s4m_catalogue/settings.py** (linea 201):
```python
# Cambia da:
API_BASE_URL = "http://django:8088"

# A:
API_BASE_URL = "http://django:8000"
```

**env.txt** (linea 73):
```bash
# Cambia da:
GEONODE_LB_PORT=8088

# A:
GEONODE_LB_PORT=8000
```

#### 2. Usa il Dockerfile.new modificato

Nel file `Dockerfile.new`, cambia:
```dockerfile
EXPOSE 8088
```
in:
```dockerfile
EXPOSE 8000
```

## 🔧 Passaggi Operativi

### 1. Backup del sistema attuale

```bash
# Ferma i container
docker-compose down

# Backup del database (se necessario)
docker-compose exec db pg_dumpall -U postgres > backup_pre_migrazione.sql

# Backup dei volumi (opzionale ma consigliato)
docker volume ls | grep s4m_catalogue
# Esporta i volumi importanti se necessario
```

### 2. Sostituzione del Dockerfile

```bash
# Se scegli Opzione 1 (mantieni 8088):
mv Dockerfile Dockerfile.backup
mv Dockerfile.new Dockerfile

# Se scegli Opzione 2 (cambia a 8000):
# Prima modifica tutti i file sopra elencati, poi:
mv Dockerfile Dockerfile.backup
mv Dockerfile.new Dockerfile
# E modifica EXPOSE 8088 → EXPOSE 8000 nel Dockerfile
```

### 3. Rebuild delle immagini

**IMPORTANTE**: Sia `django` che `celery` usano la **stessa immagine** (`${COMPOSE_PROJECT_NAME}/geonode:${GEONODE_BASE_IMAGE_VERSION}`). 
Il servizio `django` ha la sezione `build`, mentre `celery` eredita solo l'immagine dal template comune.

**Opzioni per il rebuild:**

```bash
# Opzione 1: Build solo django (consigliato - crea l'immagine usata da entrambi)
docker-compose build --no-cache django

# Opzione 2: Build tutti i servizi che hanno build (django, nginx, geoserver, ecc.)
docker-compose build --no-cache

# Opzione 3: Rimuovi prima le immagini vecchie per forzare il rebuild completo
docker images | grep s4m_catalogue
docker rmi <image_ids>
docker-compose build --no-cache
```

**Nota**: Non serve fare `docker-compose build celery` perché `celery` non ha una sezione `build` - usa l'immagine creata da `django`.

### 4. Verifica delle dipendenze

Verifica che tutti i pacchetti necessari siano ancora disponibili in Ubuntu 24.04:
- `saga` (SAGA GIS)
- `libsqlite3-mod-spatialite` (Spatialite)
- `cron` (per i cron job)
- `curl`, `wget`, `unzip`, `gnupg2` (utilità)

### 5. Test del sistema

```bash
# Avvia i container
docker-compose up -d

# Verifica i log
docker-compose logs -f django

# Verifica che il container sia healthy
docker-compose ps

# Testa l'endpoint
curl http://localhost:8088/  # o 8000 se hai cambiato porta
```

### 6. Verifica funzionalità specifiche

- [ ] Django risponde correttamente
- [ ] Celery worker funziona
- [ ] Cron job per backoffice funziona (verifica `/var/log/backoffice-updatelayers.log`)
- [ ] GeoServer comunica con Django
- [ ] Database connection funziona
- [ ] Static files vengono serviti correttamente

## 🐛 Risoluzione Problemi

### Problema: Container non si avvia
- Verifica i log: `docker-compose logs django`
- Controlla che tutti i path siano corretti (`/usr/src/s4m_catalogue`)
- Verifica che i permessi degli script siano corretti

### Problema: Pacchetti mancanti
- Se mancano pacchetti, aggiungili nel Dockerfile nella sezione `apt-get install`

### Problema: Locale non configurata
- Il Dockerfile.new include già la configurazione delle locale, ma se hai problemi:
```dockerfile
RUN sed -i -e 's/# C.UTF-8 UTF-8/C.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
```

### Problema: Cron non funziona
- Verifica che il servizio cron sia avviato nell'entrypoint.sh (già presente: `service cron restart`)
- Verifica i permessi del file cron: `chmod 0644 /etc/cron.d/backoffice-updatelayers-cron`

## 📝 Note Finali

- Il file `Dockerfile.new` che ho creato è un adattamento che combina Ubuntu 24.04 con tutte le personalizzazioni del tuo progetto
- **Raccomando l'Opzione 1** (mantenere porta 8088) per minimizzare i cambiamenti
- Se in futuro vuoi allinearti completamente al template GeoNode, potrai farlo gradualmente
- Ricorda di aggiornare anche `Dockerfile.prod` se lo usi in produzione

## ✅ Checklist Pre-Migrazione

- [ ] Backup del database
- [ ] Backup dei volumi importanti
- [ ] Verifica che tutti i servizi siano documentati
- [ ] Notifica al team (se applicabile)
- [ ] Pianifica una finestra di manutenzione

## ✅ Checklist Post-Migrazione

- [ ] Container Django funziona
- [ ] Container Celery funziona
- [ ] GeoServer comunica con Django
- [ ] Database connection OK
- [ ] Static files serviti correttamente
- [ ] Cron job funziona
- [ ] API rispondono correttamente
- [ ] Frontend si connette al backend

