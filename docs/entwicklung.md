# Entwicklung

Um eine Entwicklungsumgebung aufzusetzen musst du im Prinzip nur der [Bare-Metal Installationsbeschreibung](deployment/bare-metal.md) folgen. Nutze keinen systemd Service, sondern führe das Front- und Backend direkt aus.

Zum Ausführen des Frontends nutze folgende Befehle:

```bash
cd /pfad/zum/frontend
npm run dev
```

Zum Ausführen des Backends nutze folgende Befehle:

```bash
cd /pfad/zum/backend
source .venv/bin/activate
fastapi dev app/main.py
```
