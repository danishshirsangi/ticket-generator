from sqlalchemy import Column, String, Integer, Float, Boolean
from database import Base

class TicketInformation(Base):
    __tablename__ = 'tickets'
    ticketnumber =  Column(String(100), primary_key=True)
    ticketamount = Column(Float)
    ticketstatus = Column(Boolean)