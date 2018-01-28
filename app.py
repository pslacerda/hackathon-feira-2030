from typing import List
from datetime import datetime
from apistar import Include, Route
from apistar.handlers import docs_urls, serve_static
from pydantic import BaseModel
from apistar_pydantic import WSGIApp as App, BodyData, JSONRenderer


class Location(BaseModel):
    lat: float
    lng: float

    def __init__(self, lat: float, lng: float):
        super().__init__(lat=lat, lng=lng)


class TicketCatgory(BaseModel):
    category_id: int
    name: str
    agency: str
    allow_anonymous: bool


class Ticket(BaseModel):
    ticket_id: int
    citizen: str = None
    citizen_location: Location = None

    text: str
    location: Location
    happened_at: datetime = None

    created_at: datetime
    category_id: int

    def __init__(self, **data):
        super().__init__(created_at=datetime.now(), **data)
        category = CATEGORIES[self.category_id]
        if not category.allow_anonymous and self.citizen is None:
            raise Exception("Anonymous not allowed")


class Notification(BaseModel):
    text: str
    ticket_id: int


CATEGORIES = [
    TicketCatgory(
        category_id=1,
        name="Queixa",
        agency="Delegacia",
        allow_anonymous=True
    ),
    TicketCatgory(
        category_id=2,
        name="Soliciar Ambulância",
        agency="Hospital",
        allow_anonymous=False
    )
]

TICKETS = [
    Ticket(
        ticket_id=1,
        citizen="Fulano",
        citizen_location=Location(-12.24715, -38.9493582),
        text="Algo aconteceu",
        location=Location(-12.24715, -38.9493582),
        hapenned_at=datetime.now(),
        category_id=1
    )
]


def list_tickets() -> List[Ticket]:
    return TICKETS


def add_ticket(ticket: BodyData[Ticket]) -> int:
    TICKETS.append(ticket)
    return TICKETS.index(ticket)


def list_categories() -> List[TicketCatgory]:
    return CATEGORIES


routes = [
    Route('/tickets', 'GET', list_tickets),
    Route('/tickets', 'POST', add_ticket),
    Include('/docs', docs_urls),
    Route('/static/{path}', 'GET', serve_static)
]

settings = {
    'STATICS': {
        'ROOT_DIR': 'statics',  # Include the 'statics/' directory.
        'PACKAGE_DIRS': ['apistar']  # Include the built-in apistar static files.
    },
    'RENDERERS': [JSONRenderer()]
}

app = App(
    settings=settings,
    routes=routes
)


if __name__ == '__main__':
    app.main()
