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



# Aufgabenpaket 1 (Build und Ausführung)
## 1. Flask App erstellen und testen
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
- Docker Container lokal ausführen: `docker run -p 5000:5000 flask-app` (Wenn Port `5000` belegt ist, dann z.B. `5001:5000`)




### ArgoCD
-> Quellen: [ArgoCD installieren](https://argo-cd.readthedocs.io/en/stable/getting_started/), [Application YAML definieren](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/)
- Namespace für ArgoCD erstellen: `kubectl create namespace argocd`
- ArgoCD installierern: `kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`
- Zugriff auf die ArgoCD Oberfäche mit Portforwarding_ `kubectl port-forward svc/argocd-server -n argocd 8080:443`
- Passwort für die ArgoCD Oberfäche aus dem secret anzeigen (User ist `admin`): `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode && echo ""`
- ArgoCD Application in `argocd-app.yaml` definieren

### Helm Chart
-> Quellen: [Helm Chart erstellen](https://opensource.com/article/20/5/helm-charts)
- Helm installieren (MacOS): `brew install helm`
- Helm Chart Template anlegen: `helm create <name>`

