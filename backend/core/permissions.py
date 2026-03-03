"""
Sistema Permessi - Versione 2 Ruoli
"""

from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.models import Utente, Prenotazione, Sede
from backend.models.enums import RuoloUtente


class PermissionChecker:
    """Verifica permessi utente basati sul ruolo"""
    
    @staticmethod
    def is_coordinamento(utente: Utente) -> bool:
        """Verifica se utente è COORDINAMENTO"""
        return utente.ruolo == RuoloUtente.COORDINAMENTO
    
    @staticmethod
    def is_operativo(utente: Utente) -> bool:
        """Verifica se utente è OPERATIVO"""
        return utente.ruolo == RuoloUtente.OPERATIVO
    
    @staticmethod
    def can_view_all_locations(utente: Utente) -> bool:
        """Solo COORDINAMENTO può vedere tutte le sedi"""
        return PermissionChecker.is_coordinamento(utente)
    
    @staticmethod
    def can_view_location(utente: Utente, sede_id: int) -> bool:
        """OPERATIVO: solo propria sede, COORDINAMENTO: tutte"""
        if PermissionChecker.is_coordinamento(utente):
            return True
        return utente.sede_id == sede_id
    
    @staticmethod
    def can_manage_users(utente: Utente) -> bool:
        """Solo COORDINAMENTO può gestire utenti"""
        return PermissionChecker.is_coordinamento(utente)
    
    @staticmethod
    def can_manage_locations_rooms(utente: Utente) -> bool:
        """Solo COORDINAMENTO può gestire sedi e aule"""
        return PermissionChecker.is_coordinamento(utente)
    
    @staticmethod
    def can_create_booking(utente: Utente) -> bool:
        """Tutti possono creare prenotazioni"""
        return True
    
    @staticmethod
    def can_modify_booking(utente: Utente, prenotazione: Prenotazione) -> bool:
        """OPERATIVO: solo proprie, COORDINAMENTO: tutte"""
        if PermissionChecker.is_coordinamento(utente):
            return True
        return prenotazione.richiedente_id == utente.id
    
    @staticmethod
    def can_resolve_conflicts(utente: Utente) -> bool:
        """Solo COORDINAMENTO può risolvere conflitti"""
        return PermissionChecker.is_coordinamento(utente)
    
    @staticmethod
    def can_export_data(utente: Utente) -> bool:
        """Solo COORDINAMENTO può esportare dati"""
        return PermissionChecker.is_coordinamento(utente)


def require_coordinamento(utente: Utente):
    """Dependency: richiede ruolo COORDINAMENTO"""
    if not PermissionChecker.is_coordinamento(utente):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accesso negato: richiesto ruolo COORDINAMENTO"
        )
    return utente


def check_permission(condition: bool, error_message: str = "Accesso negato"):
    """Helper per verificare permesso"""
    if not condition:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_message
        )