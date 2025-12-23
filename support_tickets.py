# support_tickets.py - GESTIÓN DE INCIDENCIAS
from datetime import datetime

class TicketSystem:
    def __init__(self, db):
        self.db = db.tickets # Conexión a la colección de tickets

    def open_ticket(self, user_id, issue):
        ticket_data = {
            "user_id": user_id,
            "issue": issue,
            "status": "OPEN",
            "date": datetime.now()
        }
        return self.db.insert_one(ticket_data).inserted_id

    def close_ticket(self, ticket_id):
        self.db.update_one({"_id": ticket_id}, {"$set": {"status": "CLOSED"}})
