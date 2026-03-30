#!/bin/bash
# ICE Planning Aule - Docker Management Script
# Usage: ./deploy.sh [command]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_ok() { echo -e "${GREEN}✓ $1${NC}"; }
print_err() { echo -e "${RED}✗ $1${NC}"; }
print_warn() { echo -e "${YELLOW}⚠ $1${NC}"; }

check_env() {
    if [ ! -f .env ]; then
        print_err "File .env non trovato!"
        echo "Esegui: cp .env.example .env"
        exit 1
    fi
}

case "$1" in
    start|up)
        check_env
        print_ok "Avvio stack..."
        docker-compose up -d
        echo ""
        print_ok "Stack avviato!"
        echo "  Frontend: http://localhost"
        echo "  Backend:  http://localhost:8000"
        echo "  API docs: http://localhost:8000/docs"
        ;;
    stop|down)
        print_warn "Arresto stack..."
        docker-compose down
        print_ok "Stack fermato"
        ;;
    restart)
        docker-compose restart
        print_ok "Stack riavviato"
        ;;
    logs)
        docker-compose logs -f ${2:-}
        ;;
    build)
        check_env
        print_ok "Rebuild immagini..."
        docker-compose build --no-cache
        print_ok "Build completato"
        ;;
    status)
        docker-compose ps
        ;;
    backup)
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        print_ok "Backup database -> $BACKUP_FILE"
        docker-compose exec -T db mysqldump -u root -p"$DB_ROOT_PASSWORD" planning_aule > "$BACKUP_FILE"
        print_ok "Backup completato: $BACKUP_FILE"
        ;;
    shell-db)
        docker-compose exec db mysql -u planning_user -p planning_aule
        ;;
    shell-backend)
        docker-compose exec backend /bin/bash
        ;;
    clean)
        print_warn "Pulizia completa (ATTENZIONE: elimina volumi!)"
        read -p "Sicuro? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down -v --rmi local
            print_ok "Pulizia completata"
        fi
        ;;
    *)
        echo "ICE Planning Aule - Docker Management"
        echo ""
        echo "Comandi:"
        echo "  start     Avvia tutti i servizi"
        echo "  stop      Ferma tutti i servizi"
        echo "  restart   Riavvia servizi"
        echo "  logs      Mostra logs (opz: logs backend)"
        echo "  build     Rebuild immagini Docker"
        echo "  status    Stato containers"
        echo "  backup    Backup database MySQL"
        echo "  shell-db  Shell MySQL"
        echo "  shell-backend  Shell backend"
        echo "  clean     Rimuove tutto (containers, volumi, immagini)"
        ;;
esac
