import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.repositories import company_discovery_repository as discovery_runs
from app.repositories import company_repository
from app.schemas.company import CompanyDiscoveryRequest, CompanyDiscoveryResponse, CompanyDiscoveryRunResponse, CompanyLocationResponse, CompanyLocationWrite, CompanyResponse, CompanyWrite
from app.services import company_discovery_service as service
from app.services.current_candidate_service import get_current_candidate

router = APIRouter(prefix="/companies", tags=["Companies"])


def candidate(user: dict, db: Session):
    return get_current_candidate(db, user["uid"])


@router.post("/discover", response_model=CompanyDiscoveryResponse)
def discover(request: CompanyDiscoveryRequest, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    run, result_companies = service.discover(db, candidate(user, db), request)
    return {"run": run, "companies": result_companies}


@router.get("/discovery-runs", response_model=list[CompanyDiscoveryRunResponse])
def list_discovery_runs(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return discovery_runs.list_for_candidate(db, candidate(user, db).id)


@router.get("/discovery-runs/{run_id}", response_model=CompanyDiscoveryRunResponse)
def get_discovery_run(run_id: uuid.UUID, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    run = discovery_runs.owned_run(db, run_id, candidate(user, db).id)
    if not run:
        from fastapi import HTTPException
        raise HTTPException(404, "Discovery run not found")
    return run


@router.get("", response_model=list[CompanyResponse])
def list_companies(search: str | None = None, city: str | None = None, area: str | None = None, status: str | None = Query(None, pattern="^(active|inactive|unknown)$"), limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return company_repository.search(db, query=search, city=city, area=area, status=status, limit=limit, offset=offset)


@router.post("", response_model=CompanyResponse)
def create_company(item: CompanyWrite, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.create_manual_company(db, item)


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: uuid.UUID, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    from fastapi import HTTPException
    company = company_repository.by_id(db, company_id)
    if not company:
        raise HTTPException(404, "Company not found")
    return company


@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: uuid.UUID, item: CompanyWrite, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.update_manual_company(db, company_id, item)


@router.get("/{company_id}/locations", response_model=list[CompanyLocationResponse])
def list_locations(company_id: uuid.UUID, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    from fastapi import HTTPException
    company = company_repository.by_id(db, company_id)
    if not company:
        raise HTTPException(404, "Company not found")
    return company.locations


@router.post("/{company_id}/locations", response_model=CompanyLocationResponse)
def create_location(company_id: uuid.UUID, location: CompanyLocationWrite, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.add_location(db, company_id, location)
