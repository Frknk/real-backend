from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.database import get_session
from src.routes.providers.models import (
    ProviderRead,
    ProviderCreate,
    ProviderUpdate,
    Provider,
)
from src.routes.providers.operations import (
    create_provider,
    get_providers,
    get_provider,
    update_provider,
    delete_provider,
)

router = APIRouter()


@router.post("", response_model=Provider)
def create_provider_view(
    provider: ProviderCreate, session: Session = Depends(get_session)
):
    return create_provider(provider, session)


@router.get("", response_model=list[ProviderRead])
def get_providers_view(session: Session = Depends(get_session)):
    return get_providers(session)


@router.get("/{provider_id}", response_model=ProviderRead)
def get_provider_view(provider_id: int, session: Session = Depends(get_session)):
    return get_provider(provider_id, session)


@router.patch("/{provider_id}", response_model=ProviderUpdate)
def update_provider_view(
    provider_id: int, provider: ProviderUpdate, session: Session = Depends(get_session)
):
    return update_provider(provider_id, provider, session)


@router.delete("/{provider_id}")
def delete_provider_view(provider_id: int, session: Session = Depends(get_session)):
    return delete_provider(provider_id, session)
