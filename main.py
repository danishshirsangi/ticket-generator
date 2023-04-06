from fastapi import FastAPI, status, HTTPException
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schema import TicketRequest, UpdateRequest
from models import TicketInformation
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

app = FastAPI()


@app.get('/')
def homepage():
    return {'message':'Hello World!'}


@app.get('/api/v1/readtickets/')
def read_tickets():
    session = Session(bind=engine, expire_on_commit=False)
    tickets = session.query(TicketInformation).all()
    return tickets

@app.get('/api/v1/readticket/{ticket_id}/')
def read_ticket(ticket_id: str):
    session = Session(bind=engine, expire_on_commit=False)
    ticket_id = ticket_id.lower()
    ticket = session.query(TicketInformation).get(ticket_id)
    if ticket:
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail='Cannot Find Given Ticket')
    return ticket

@app.post('/api/v1/updateticket/{ticket_id}')
def update_ticket(ticket_id: str, req_body: UpdateRequest):
    session = Session(bind=engine, expire_on_commit=False)

    ticket = session.query(TicketInformation).filter(TicketInformation.ticketnumber==ticket_id).first()
    if ticket:
        if req_body.amountCleared:
            session.query(TicketInformation).filter(TicketInformation.ticketnumber == ticket_id).update(
                {
                "ticketnumber": ticket_id,
                "ticketamount": 0,
                "ticketstatus": False
                }
            )
            session.commit()
            session.close()
            return {"Amount Returned & Ticket Closed"}
        else:
            session.query(TicketInformation).filter(TicketInformation.ticketnumber == ticket_id).update({
                "ticketnumber": ticket_id,
                "ticketamount": abs(ticket.ticketamount - req_body.returnedAmount),
                "ticketstatus": True
                })
            session.commit()
            session.close()
            return {"Remaining Amount Will Be Closed Soon"}
    else:
        raise HTTPException(status_code=404, detail={"error":"Cannot Find Ticket"})

@app.post('/api/v1/createticket/')
def create_ticket(ticket: TicketRequest):
    session = Session(bind=engine, expire_on_commit=False)
    ticket.ticketnumber = ticket.ticketnumber.lower()
    try:
        ticketObj = TicketInformation(ticketnumber=ticket.ticketnumber, ticketamount=ticket.ticketamount,   ticketstatus = ticket.ticketstatus)
        session.add(ticketObj)
        session.commit()
        session.close()
    except:
        raise HTTPException(status_code=404,detail={"error":"Cannot Create Ticket"})
    return ticketObj

@app.get('/api/v1/ticketdelete/{ticket_id}/')
def delete_ticket(ticket_id: str):
    session = Session(bind=engine, expire_on_commit=False)
    ticket_id = ticket_id.lower()
    ticket = session.query(TicketInformation).get(ticket_id)

    if ticket:
        session.delete(ticket)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"No Ticket With Given Id")
    return f"Deleted Ticket with ID {ticket_id}"