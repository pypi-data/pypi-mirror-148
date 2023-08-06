import datetime
import sqlalchemy
import uvicorn

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from pydantic import BaseModel, Field
from typing import List, Optional
from jaeger_client import Config
from opentracing.scope_managers.asyncio import AsyncioScopeManager
from fastapi_contrib.conf import settings

app = FastAPI(title='Job Offer Service API')
db = create_engine('postgresql://postgres:postgres@job_offer_service_db:5432/postgres')  


# should be env variable

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def setup_opentracing(app):
    config = Config(
        config={
            "local_agent": {
                "reporting_host": settings.jaeger_host,
                "reporting_port": settings.jaeger_port
            },
            "sampler": {
                "type": settings.jaeger_sampler_type,
                "param": settings.jaeger_sampler_rate,
            },
            "trace_id_header": settings.trace_id_header
        },
        service_name="job_offer_service",
        validate=True,
        scope_manager=AsyncioScopeManager()
    )

    app.state.tracer = config.initialize_tracer()
    app.tracer = app.state.tracer


@app.on_event('startup')
async def startup():
    setup_opentracing(app)
    with app.tracer.start_span('first-span') as span:
        span.set_tag('first-tag', '100')

JOB_OFFERS_URL = '/api/job_offers'

class JobOffer(BaseModel):
    id: Optional[int] = Field(description='Job Offer ID')
    date: Optional[datetime.datetime] = Field(description='Job Offer Date')
    position: str = Field(description='Job Offer Position')
    requirements: str = Field(description='Job Offer Requirements')
    description: str = Field(description='Job Offer Description')
    agent_application_link: str = Field(description='Job Offer Agent Application Link')


class NavigationLinks(BaseModel):
    base: str = Field('http://localhost:8000/api', description='API base URL')
    prev: Optional[str] = Field(None, description='Link to the previous results page')
    next: Optional[str] = Field(None, description='Link to the next results page')


class Response(BaseModel):
    results: List[JobOffer]
    links: NavigationLinks
    offset: int
    limit: int
    size: int


#should job offer have user_id and user_full_name?


def search_query(search: str):
    return f"position like '%{search}%' or requirements like '%{search}%' or description like '%{search}%'"


@app.post(JOB_OFFERS_URL)
def create_job_offer(job_offer: JobOffer):
    with db.connect() as connection:
        connection.execute(sqlalchemy.text(f"""
            insert into job_offers (date, position, requirements, description, agent_application_link) values
            (current_timestamp, '{job_offer.position}', '{job_offer.requirements}', '{job_offer.description}', '{job_offer.agent_application_link}')
        """))
        # fix sql injection here


@app.get(JOB_OFFERS_URL)
def read_job_offers(search: str = Query(''), offset: int = Query(0), limit: int = Query(7)):
    with db.connect() as connection:
        # before it was .scalar() instead of len()
        total_job_offers = len(connection.execute(sqlalchemy.text(f"select count(*) from job_offers where {search_query(search)}")))
    prev_link = f"/job_offers?search={search}&offset={offset - limit}&limit={limit}" if offset - limit >= 0 else None
    next_link = f"/job_offers?search={search}&offset={offset + limit}&limit={limit}" if offset + limit < total_job_offers else None
    links = NavigationLinks(prev=prev_link, next=next_link)

    with db.connect() as connection:
        job_offers = connection.execute(sqlalchemy.text(f"select * from job_offers where {search_query(search)} order by date desc offset {offset} limit {limit}"))
        results = [JobOffer.parse_obj(dict(job_offer)) for job_offer in job_offers]
    return Response(results=results, links=links, offset=offset, limit=limit, size=len(results))


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8002)
