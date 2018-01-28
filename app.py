from typing import Tuple, Optional
from datetime import datetime
from apistar import Include, Route
from apistar.handlers import docs_urls, serve_static
from pydantic import BaseModel
from apistar_pydantic import WSGIApp as App, BodyData


class Location(BaseModel):
    lat: int
    lng: int


class Ticket(BaseModel):
    ticket_id: int
    citizen: str = None
    citizen_location: Location = None

    text: str
    location: Location
    happened_at: datetime

    created_at: datetime


class Notification(BaseModel):
    text: str
    ticket_id: int


TICKETS = [
    #
    #     user_loc=(-12.24715, -38.9493582),
    #     loc=(-12.24715, -38.9493582)
    # ),
    # Ticket(
    #     citzen="Beltrano",
    #     description="Algo também aconteceu!!!!!",
    #     user_loc=(-12.25715, -38.9503582),
    #     loc=(-12.25715, -38.9503582)
    # ),
]


def list_tickets():
    return TICKETS


def add_ticket(ticket: BodyData[Ticket]):
    TICKETS.append(ticket)


routes = [
    Route('/tickets', 'GET', list_tickets),
    Route('/tickets', 'POST', add_ticket),
    Include('/docs', docs_urls),
    Route('/{path}', 'GET', serve_static)
]

settings = {
    'STATICS': {
        'ROOT_DIR': 'statics',  # Include the 'statics/' directory.
        'PACKAGE_DIRS': ['apistar']  # Include the built-in apistar static files.
    }
}

app = App(
    settings=settings,
    routes=routes
)


if __name__ == '__main__':
    app.main()
