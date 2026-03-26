# Avvio Applicativo in locale

### Database

Start Apache
Start MySQL
(http://localhost/phpmyadmin/)

### Ambiente Virtuale

.\ice_venv\Scripts\activate

### Backend - Terminale 1

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload --log-config backend/utils/logging_config.json
(http://localhost:8000/api/docs)

### Frontend - Terminale 2

cd frontend
npm run dev
(http://localhost:5173)




**Altra modifica sul filtro in base all'utente:**

**Vorrei aggiungerlo anche nella pagina Nuova Prenotazione**
