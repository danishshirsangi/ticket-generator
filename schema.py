from pydantic import BaseModel

class TicketRequest(BaseModel):
    ticketnumber: str
    ticketamount: float
    ticketstatus: bool

class UpdateRequest(BaseModel):
    returnedAmount: float
    amountCleared: bool