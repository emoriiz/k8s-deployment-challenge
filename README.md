# k8s-deployment-challenge
Im Rahmen eines Bewerbungsprozesses auf eine Stelle als `CloudOps Engineer / Consultant` habe ich die folgende Aufgabenstellung bekommen und in diesem Repository dokumentiert gelöst.

# Aufgabenstellung
### Ziel

Sie sollen eine beliebige Beispielanwendung deployen. Danach erweitern Sie die Auslieferung um einen kleinen, reproduzierbaren CI/CD-Ansatz.Ob Sie eine existierende Anwendung (z.b. von dockerhub) verwenden oder eine selber erstellen bleibt Ihnen überlassen.

### Rahmenbedingungen

- Die Wahl der Technologien ist frei (z. B. Container-Runtime, Orchestrierung, Deployment-Mechanismus, CI/CD-Tool).
- Die Lösung muss lokal oder in einer von Ihnen gewaehlten Umgebung nachvollziehbar demonstrierbar sein.
- Die Anwendung muss einen Health-Endpoint z.B. `GET /healthz` bereitstellen.

### Aufgabenpakete

1. **Build und Ausführung**
    - Anwendung builden (als Container).
    - Anwendung starten.
    - Nachweis, dass App und Health-Endpoint funktionieren.
2. **Deployment-Umsetzung**
    - Deployment mit einem von Ihnen gewaehlten Ansatz umsetzen. (z.B. Pipelines, GitHub Actions, ArgoCD, ...)
    - Konfiguration nachvollziehbar und reproduzierbar setzen.
    - Deployment-Zustand prüfen (z. B. Logs, Health-Checks, Status, Fehlerfälle).
3. **Fehleranalyse und Betriebsfaehigkeit**
    - Simulieren Sie einen realistischen Fehlerfall (z. B. falscher Image-Tag oder fehlerhafte Env-Konfiguration).
    - Beschreiben Sie kurz die Diagnose-Schritte und die Behebung.
4. **Bonus (optional) Mini CI/CD-Teil**
    - Verwenden von Helm Charts
    - Erstellen Sie eine einfache Pipeline (z. B. GitHub Actions oder Azure DevOps YAML), die mindestens:
        - den Build ausfuehrt,
        - Artefakte/versionierte Ergebnisse sinnvoll kennzeichnet,
        - und einen Deployment-Schritt ausfuehrt.
    - Secrets müssen sauber behandelt werden (keine Klartext-Credentials in Dateien oder Screenshots).
5. **Bonus (optional)**
    - Rollback- oder Recovery-Demonstration.
    - Kurzer Vorschlag zur Absicherung der Supply Chain (z. B. Image-Scan, Signierung, SBOM).

### Präsentation im 2. Termin

Im **2. Termin** präsentieren Sie Ihr Ergebnis in ca. **15-20 Minuten**:

1. Kurzer Architektur- und Vorgehens-Überblick.
2. Live- Walkthrough der wichtigsten Ergebnisse.
3. Begründung zentraler Entscheidungen (z. B. Tooling, Versionierung, Troubleshooting).

### Bewertungskriterien

Bewertet wird:

- **Technische Korrektheit**: Funktioniert die Lösung reproduzierbar?
- **DevOps-Verständnis**: Sinnvolle Entscheidungen bei Build, Tagging, Deployment und Betrieb.
- **Plattform-/Deployment-Kompetenz**: Solider Umgang mit dem gewählten Deployment-Ansatz und Debugging.
- **Sicherheitsbewusstsein**: Keine Secrets im Klartext, vernünftiger Umgang mit Credentials.
- **Kommunikation**: Verständliche Erklärung, saubere Argumentation, Rückfragen fachlich fundiert beantworten.

### Hinweise

- Sie dürfen KI-Tools verwenden, wenn Sie dies kurz kenntlich machen.
- Es geht nicht um "perfekt", sondern um sauberes, pragmatisches Engineering.
- Falls Sie nicht alle Punkte schaffen, priorisieren Sie Kernfunktionalität und dokumentieren offen, was noch fehlt.


# Übersicht Aufgabenlösungen
In diesem Abschnitt werden die Lösungen zu den Aufgabenpaketen angeben, im Abschnitt [Einzelne Einrichtungs- und Installationsschritte](#Einzelne-Einrichtungs-undInstallationsschritte) sind die genauen teschnischen Schritte und Befehle aufgeführt.

## Aufgabenpaket 1 (Build und Ausführung)

### Anwendung
- Die Beispielanwendung ist eine minimalistische Flask-App mit zwei Endpunkten:
    - `/` -> Gibt einfachen Text als HTML Paragraph zurück
    - `/healthz` -> gibt ein JSON {"status": "healthy"} und den Statuscode 200 zurück
    - Beispiel: curl http://localhost:5000/healthz -> {"status": "healthy"}

### Containerisierung
- Die Anwendung wurde in ein Docker Image verpackt und lokal geteste, siehe [Flask App erstellen und testen](#Flask-App-erstellen-und-testen)


## Aufgabenpaket 2 (Deployment-Umsetzung)

### Architektur
- Lokales Single Node Kubernetes Cluster über Docker Desktop
- Flask App als Docker Container
- Images werden in der GHCR (GitHub Container Registry) gespeichert
- Helm Chart im Ordner `deployment/` definiert alle Kubernetes Ressourcen
- ArgoCD läuft im Cluster im Namespace `argocd` und überwacht das GitHub Repository auf Änderungen im `deployment/` Ordner
- GitHub Actions Pipeline übernimmt den CI-Part: Image bauen, in GHCR pushen, Image Tag in `values.yaml` aktualisieren

### Deployment-Prozess
1. Code wird in GitHub gepusht
2. GitHub Actions baut ein Docker Image und pusht es in die Registry (GHCR)
3. Die Pipeline aktualisiert den Image Tag im Helm Chart
4. Die Änderung wird ins Repository committed
5. ArgoCD erkennt die Änderung und deployed automatisch das neue Image in den Namespace `flask-app` im Kubernetes Cluster

### Überprüfung des Deployments
- `kubectl get pods -n flask-app` -> Status der Pods prüfen
- `kubectl logs <pod> -n flask-app` -> Logs analysieren
- `kubectl describe deployment flask-app -n flask-app` -> Analyse des Deployments
- `kubectl port-forward svc/flask-app 5000:5000 -n flask-app` → Zugriff auf den Health-Endpoint unter `http://127.0.0.1:5000/healthz`
- ArgoCD UI: Status "Synced" und "Healthy"


## Aufgabenpaket 3 (Fehleranalyse und Betriebsfaehigkeit)

### Fehlerfall: Falsch konfigurierte Liveness Probe
**Szenario:** Der Pfad der Liveness Probe in `deployment/values.yaml` zeigt auf einen nicht existierenden Endpunkt -> Kubernetes markiert den Pod wiederholt als unhealthy und startet ihn neu

**Simulation:**
- `livenessProbe.httpGet.path` in `deployment/values.yaml` auf `/wrong` setzen und committen
- Pipeline läuft durch, ArgoCD synct die Änderung ins Cluster
- Kubernetes ruft periodisch `/wrong` auf -> 404 -> Pod wird als unhealthy eingestuft und neugestartet

**Diagnose:**
- `kubectl get pods -n flask-app` -> Zunächst läuft der Pod, aber er startet immer wieder neu (siehe **Verhalten des Pods im Namespace `flask-app`**)
- Nach 5 Neustarts wechselt der Status zu `CrashLoopBackOff`
- Wechselt zwischenzeitlich immer wieder in den Zustand `Running`, währenddessen ist die Flask Anwendung auch erreichbar
- Mit `kubectl logs <pod> -n flask-app` sieht man, dass beim `livenessProbe` Endpoint der Fehler `404` zurückkommt, da `/wrong` nicht als Endpoint in der Flask App existiert (siehe **Pod Logs**)
- In der ArgoCD UI kommt ebenfalls eine Fehlermeldung:
    ```
    Container is waiting because of CrashLoopBackOff. It is not started and not ready.
    The container last terminated 4 minutes ago with exit code 137 because of Error.
    ```

**Verhalten des Pods im Namespace `flask-app`:**
```
nico@macbook-pro-14 ~ % kubectl get pods -n flask-app                      
NAME                         READY   STATUS        RESTARTS      AGE
flask-app-644c77968b-8n77x   1/1     Running       0             20s
flask-app-8975ddb87-ts4st    1/1     Terminating   1 (98m ago)   2d1h
nico@macbook-pro-14 ~ % kubectl get pods -n flask-app
NAME                         READY   STATUS    RESTARTS   AGE
flask-app-644c77968b-8n77x   1/1     Running   0          46s
nico@macbook-pro-14 ~ % kubectl get pods -n flask-app
NAME                         READY   STATUS    RESTARTS      AGE
flask-app-644c77968b-8n77x   1/1     Running   1 (55s ago)   115s
nico@macbook-pro-14 ~ % kubectl get pods -n flask-app
NAME                         READY   STATUS    RESTARTS      AGE
flask-app-644c77968b-8n77x   1/1     Running   2 (37s ago)   2m37s
nico@macbook-pro-14 ~ % kubectl get pods -n flask-app
NAME                         READY   STATUS    RESTARTS      AGE
flask-app-644c77968b-8n77x   1/1     Running   3 (33s ago)   3m33s
nico@macbook-pro-14 ~ % kubectl get pods -n flask-app
NAME                         READY   STATUS             RESTARTS     AGE
flask-app-644c77968b-8n77x   0/1     CrashLoopBackOff   5 (5s ago)   6m5s
nico@macbook-pro-14 ~ % kubectl get pods -n flask-app
NAME                         READY   STATUS    RESTARTS      AGE
flask-app-644c77968b-8n77x   1/1     Running   6 (89s ago)   7m29s
nico@macbook-pro-14 ~ % kubectl get pods -n flask-app
NAME                         READY   STATUS    RESTARTS        AGE
flask-app-644c77968b-8n77x   1/1     Running   6 (2m15s ago)   8m15s
nico@macbook-pro-14 ~ % kubectl get pods -n flask-app
NAME                         READY   STATUS             RESTARTS      AGE
flask-app-644c77968b-8n77x   0/1     CrashLoopBackOff   6 (10s ago)   8m30s
nico@macbook-pro-14 ~ % kubectl get pods -n flask-app
NAME                         READY   STATUS             RESTARTS        AGE
flask-app-644c77968b-8n77x   0/1     CrashLoopBackOff   7 (4m49s ago)   16m
nico@macbook-pro-14 ~ % kubectl get pods -n flask-app
NAME                         READY   STATUS    RESTARTS       AGE
flask-app-644c77968b-8n77x   1/1     Running   8 (6m8s ago)   18m
nico@macbook-pro-14 ~ % kubectl get pods -n flask-app
NAME                         READY   STATUS             RESTARTS      AGE
flask-app-644c77968b-8n77x   0/1     CrashLoopBackOff   9 (21s ago)   19m
```

**Pod Logs:**
```
nico@macbook-pro-14 ~ % kubectl logs flask-app-644c77968b-8n77x -n flask-app
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://10.244.0.13:5000
Press CTRL+C to quit
10.244.0.1 - - [17/Jun/2026 18:39:51] "GET /healthz HTTP/1.1" 200 -
10.244.0.1 - - [17/Jun/2026 18:39:53] "GET /wrong HTTP/1.1" 404 -
10.244.0.1 - - [17/Jun/2026 18:40:01] "GET /healthz HTTP/1.1" 200 -
10.244.0.1 - - [17/Jun/2026 18:40:03] "GET /wrong HTTP/1.1" 404 -
10.244.0.1 - - [17/Jun/2026 18:40:11] "GET /healthz HTTP/1.1" 200 -
10.244.0.1 - - [17/Jun/2026 18:40:13] "GET /wrong HTTP/1.1" 404 -
10.244.0.1 - - [17/Jun/2026 18:40:21] "GET /healthz HTTP/1.1" 200 -
127.0.0.1 - - [17/Jun/2026 18:40:30] "GET /healthz HTTP/1.1" 200 -
10.244.0.1 - - [17/Jun/2026 18:40:31] "GET /healthz HTTP/1.1" 200 -
127.0.0.1 - - [17/Jun/2026 18:40:31] "GET /healthz HTTP/1.1" 200 -
127.0.0.1 - - [17/Jun/2026 18:40:34] "GET / HTTP/1.1" 200 -
10.244.0.1 - - [17/Jun/2026 18:40:41] "GET /healthz HTTP/1.1" 200 -
```

**Behebung:**
- `livenessProbe.httpGet.path` in `deployment/values.yaml` auf `/healthz` zurücksetzen und committen
- ArgoCD erkennt die Änderung automatisch und synced den korrekten Zustand zurück


## Aufgabenpaket 4 (Mini CI/CD-Teil)

### Helm Chart
- Helm Chart Template mit `helm create deployment` erstellt
- Template als Ausgangspunkt genommen und auf die Flask App angepasst:
    - `image.repository` auf `ghcr.io/emoriiz/k8s-deployment-challenge` gesetzt
    - `service.port` auf `5000` (Flask Standard) gesetzt
    - `livenessProbe` und `readinessProbe` auf den `/healthz` Endpunkt konfiguriert

### CI Teil
- Der CI Teil wird über eine GitHub Actions Pipeline mit folgenden Schritten ausgeführt:
    - **Checkout:** Repository Code auschecken
    - **Set up Docker Buildx:** Multi Arch Builds (amd64 + arm64) ermöglichen
    - **Set up QEMU:** ARM-Emulation für Cross Platform Builds
    - **Login to GitHub Container Registry:** Authentifizierung an GHCR über automatisches `GITHUB_TOKEN`
    - **Build and push:** Docker Image bauen und in GHCR pushen (für `linux/amd64` und `linux/arm64`)
    - **Update image tag in values.yaml:** Commit SHA als neuen Image Tag in `deployment/values.yaml` schreiben und ins Repository pushen

### CD Teil
- ArgoCD per Helm im Cluster im Namespace `argocd` deployed
- ArgoCD Application in `argocd-app.yaml` definiert und im Cluster angewendet
- ArgoCD überwacht Branch `main` des GitHub Repositories und erkennt Änderungen im `deployment/` Ordner
- Bei einer Änderung (z.B. neuer Image Tag in `values.yaml`) synced ArgoCD automatisch den neuen Zustand ins Cluster

### Versionierung
- Images werden mit dem vollständigen Git Commit SHA getaggt
- Der SHA wird am Ende der Pipeline automatisch in `deployment/values.yaml` eingetragen und committed
- Dadurch ist jedes laufende Image eindeutig einem Commit zuzuordnen und ArgoCD erkennt jede Änderung zuverlässig
- Zusätzlich wird das Tag `latest` für den jeweils neuesten Stand gepflegt

### Umgang mit Secrets
- Keine Credentials sind im Repository gespeichert
- Das `GITHUB_TOKEN` wird von GitHub Actions automatisch bereitgestellt und ist nur während der Pipeline Laufzeit verfügbar -> kein manuelles Secret nötig
- Die GHCR Registry ist für öffentliche Images konfiguriert, daher ist kein `imagePullSecret` im Kubernetes Cluster notwendig
- Das initiale ArgoCD Admin Passwort liegt als Kubernetes Secret (`argocd-initial-admin-secret`) im Cluster, ist aber nicht im Repository vorhanden, das Auslesen setzt Cluster Zugriff voraus

## Aufgabenpaket 5 (Rollback und Supply Chain)

### Rollback
- Ein Rollback kann über ArgoCD durchgeführt werden, indem eine frühere Version ausgewählt und erneut deployed wird

### Vorschlag zur Absicherung der Supply Chain
- Nicht implementiert
- Automatisches Image-Scanning (z. B. mit Trivy)
    - Das fertige Docker Image wird direkt in der GitHub Action vor dem Push auf bekannte Sicherheitslücken und Viren untersucht
    - Verhindert, dass unsichere Bibliotheken in den Cluster deployed werden
- Erstellung einer Software Stückliste (SBOM)
    - Automatische Generierung einer Liste aller in der Flask-App installierten Pakete
    - Volle Transparenz darüber, was sich im Container befindet
- Digitale Image-Signierung (z. B. mit Cosign)
    - Die Pipeline versieht das überprüfte Image mit einem digitalen, kryptografischen Siegel
    - Das Kubernetes Cluster startet die App nur, wenn das Siegel echt ist -> Schutz vor manipulierten Images
- Orientierung an Standards
    - [Offizielle Best Practices der CNCF (Cloud Native Computing Foundation)](https://tag-security.cncf.io/community/resources/security-whitepaper/v1/secure-software-factory/)
    - [Richtlinie TR-03183 des BSI](https://www.bsi.bund.de/DE/Service-Navi/Presse/Alle-Meldungen-News/Meldungen/TR-03183-2-SBOM-Anforderungen.html)


# Einzelne Einrichtungs- und Installationsschritte

## Flask App erstellen und testen

### Lokal
-> Quellen: [Installation virtuelle Umgebung und Flask](https://flask.palletsprojects.com/en/stable/installation/), [Grundgerüst Flaskanwendung und Ausführung](https://flask.palletsprojects.com/en/stable/quickstart/)
- Flask Application `app.py` und `requirements.txt` Dateien erstellen
- Virtuelle Python Umgebung erstellen um Versionsabhänigkeiten bei verschiedenen Projekten zu vermeiden: `python3 -m venv .venv`
- Virtuelle Umgebung aktivieren: `. .venv/bin/activate` oder `source .venv/bin/activate`
- In den `app` Ordner wechseln: `cd app`
- Erforderliche Pakete installieren (aktuell nur Flask): `pip install -r requirements.txt`
- Flask Anwendung starten: `flask --app app run`
- Die Anwendungs ist im Browser unter `http://127.0.0.1:5000`erreichbar
- Bei `http://127.0.0.1:5000/healthz` erscheint der healthz Endpoint

### Docker
-> Quellen: [Python Anwendung containerisieren](https://docs.docker.com/guides/python/containerize/), [Minimal Docker Container Python](https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3)
- Dockerfile erstellen
- Docker Image bauen: `docker build -t flask-app .`
- Docker Container lokal ausführen (Docker Desktop): `docker run -p 5000:5000 flask-app` (Wenn Port `5000` belegt ist, dann z.B. `5001:5000`)


## Kubernetes
- Für Kubernetes wird Docker Desktop Kubernetes verwendet, dabei wird durch Docker Desktop, welches ich ohnehin bereits nutze, ein lokales Kubernetes Cluster auf dem Rechner mit einem Node auf gesetzt


## ArgoCD
-> Quellen: [ArgoCD installieren](https://argo-cd.readthedocs.io/en/stable/getting_started/), [Application YAML definieren](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/)
- Namespace für ArgoCD erstellen: `kubectl create namespace argocd`
- ArgoCD installierern: `kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`
- Zugriff auf die ArgoCD Oberfäche mit Portforwarding_ `kubectl port-forward svc/argocd-server -n argocd 8080:443`
- Passwort für die ArgoCD Oberfäche aus dem secret anzeigen (User ist `admin`): `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode && echo ""`
- ArgoCD Application in `argocd-app.yaml` definieren
- Datei im Cluster anwenden: `kubectl apply -f argocd-app.yaml`


## Helm Chart
-> Quellen: [Helm Chart erstellen](https://opensource.com/article/20/5/helm-charts)
- Helm installieren (MacOS): `brew install helm`
- Helm Chart Template anlegen: `helm create <name>`
- Helm Values anpassen: image, service, livenessProbe, readinessProbe


## GitHub Actions
-> Quellen: [GitHub Actions Build and Push Docker Images Anleitung GitHub](https://docs.github.com/de/actions/tutorials/publish-packages/publish-docker-images), [GitHub Actions Build and Push Docker Images Anleitung Docker](https://docs.docker.com/guides/python/configure-github-actions/)
- `yml` Datei für den Workflow in `.github/workflows` anlegen


# Problem: Image Tag bei der Pipeline
- Zunächst hatte ich `latest` als Image Tag in den Helm Values gesetzt, ArgoCD hat daraufhin keine neuen Pods ausgerollt, obwohl sich die Flask Anwendung geändert hatte
- Der Grund: ArgoCD erkennt nur Änderungen in den Helm Values und reagiert nicht auf ein neu gepushtes Image unter demselben Tag
- Die Lösung war, den Tag im letzten Pipeline Schritt immer auf den aktuellen Commit SHA zu setzen, so sieht ArgoCD bei jedem Commit eine Änderung und deployed automatisch
- Alternativ gäbe es den ArgoCD Image Updater, ich habe mich aber bewusst für die einfachere Pipeline Variante entschieden


# Fazit
- Einige der hier behandelten Themen und Technologien habe ich bereits vorher gekannt und verwendet
- Folgende Tools habe ich bereits vor der Challenge verwendet: Flask, Docker, Kubernetes, Helm, ArgoCD
- Helm hatte ich bereits verwendet, jedoch habe ich vorher noch kein eigenes Helm Chart gebaut
- Auch GitHub Actions war neu für mich, ich habe vorher einmal mit GitLab CI ein Pipeline gebaut, jedoch im Kontext eines Terraform States
- Dementsprechend konnte ich meine Kenntinsse in den Technologien die ich bereits kannte vertiefen und auch neue Themen kennenleren
- KI Tools (Claude) habe ich punktuell zur Validierung von Ideen, zur Unterstützung bei der Fehleranalyse sowie beim Verfeinern der Dokumentation eingesetzt, die technische Umsetzung basiert auf eigenem Wissen und eigener Recherche