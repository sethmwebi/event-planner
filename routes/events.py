from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status

from auth.authenticate import authenticate
from database.connection import Database
from models.event import Event, EventUpdate

event_database = Database(Event)

event_router = APIRouter(tags=["Events"])

events = []


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist",
        )
    return event


@event_router.post("/new")
async def create_event(
    body: Event = Body(...), user: str = Depends(authenticate)
) -> dict:
    body.creator = user
    await event_database.save(body)
    return {"message": "Event created successfully"}


@event_router.put("/{id}", response_model=Event)
async def update_event(
    id: PydanticObjectId, body: EventUpdate, user: str = Depends(authenticate)
) -> Event:
    event = await event_database.get(id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Operation not allowed"
        )
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist",
        )
    return updated_event


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    event = await event_database.get(id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return {"message": "Event deleted successfully"}


@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {"message": "Events deleted successfully"}
