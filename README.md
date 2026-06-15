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
In diesem Abschnitt werden wird die Lösung zu den Aufgabenpaketen angeben, im Abschnitt [Einzelne Einrichtungs- und Installationsschritte](#Einzelne-Einrichtungs--undInstallationsschritte) sind die genauen teschnischen Schritte und Befehle aufgeführt

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
TODO


### Deployment-Prozess
1. Code wird in GitHub gepusht
2. GitHub Actions baut ein Docker Image und pusht es in die Registry (GHCR)
3. Die Pipeline aktualisiert den Image Tag im Helm Chart
4. Die Änderung wird ins Repository committed
5. ArgoCD erkennt die Änderung und deployed automatisch das neue Image ins Kubernetes Cluster

### Überprüfung des Deployments (TODO)
- kubectl get pods → Status der Pods prüfen
- kubectl logs <pod> → Logs analysieren
- Zugriff auf den Health-Endpoint (/healthz)
- ArgoCD UI: Status "Synced" und "Healthy"



## Aufgabenpaket 3 (Fehleranalyse und Betriebsfaehigkeit)

TODO

## Aufgabenpaket 4 (Mini CI/CD-Teil)

### Helm Chart

### CI Teil (TODO)
- Der CI Teil wird über eine GitHub Actions mit folgenden Pipelineschritten ausgeführt
    - Checkout: 
    - Set up Docker Buildx:
    - Set up QEMU:
    - Login to GitHub Container Registry:
    - Build and push:
    - Update image tag in values.yaml:

### CD Teil
TODO

### Versionierung
TODO

### Umgang mit Secrets
TODO

## Aufgabenpaket 5 (Rollback und Supply Chain)

### Rollback
- Ein Rollback kann über ArgoCD durchgeführt werden, indem eine frühere Revision ausgewählt und erneut deployed wird

### Supply Chain
TODO


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
- Für Kubernetes wird Docker Desktop Kubernetes verwendet, dabei wird durch Docker Desktop, welches ich ohnehin bereits nutze, ein lokales Kubernetes Cluster auf dem Rechner mit einem Note auf gesetzt


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


TODO
kubectl port-forward svc/flask-app 5000:5000 -n flask-app


# Problem: Image Tag bei der Pipeline
- Ich hatte zunächst den Tag latest in die Helm Values geschrieben und dann das Problem, dass ArgoCD keinen neuen Pod deployed hat, wenn ich etwas in der Flask Anwendung angepasst hatte
- Dies lag daran, dass ArgoCD scheinbar nur auf geänderte Helm Values reagiert und dementsprechden der Tag angepasst werden muss
- Den Tag aktuallisiere ich jetzt immer im letzten Pipeline Schritt mit dem eindeutigen Commit SHA (Simple Hashing Algorithm), damit ArgoCD bei jedem Commit einen neune Pod baut
- Es gäbe das Tool ArgoCD Image Updater, ich habe mich aber erstmal für die einfacherer Variante entschieden und Update das Image Tag in der Pipeline


# Fazit
- Einige der hier behandelten Themen und Technologien habe ich bereits vorher gekannt und verwendet
- Folgende Tools habe ich bereits vor der Challenge verwendet: Flask, Docker, Kubernetes, Helm, ArgoCD
- Helm hatte ich bereits verwendet, jedoch habe ich vorher noch kein eigenes Helm Chart gebaut
- Auch GitHub Actions war neu für mich, ich habe vorher einmal mit GitLab CI ein Pipeline gebaut, jedoch im Kontext eines Terraform States
- Dementsprechend konnte ich meine Kenntinsse in den Technologien die ich bereits kannte vertiefen und auch neue Themen kennenleren