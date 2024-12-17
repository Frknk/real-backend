from src.routes.providers.models import Provider, ProviderCreate, ProviderUpdate
from src.database import get_session
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

def create_provider(provider: ProviderCreate, session: Session = Depends(get_session)):
    _provider = Provider.model_validate(provider)
    session.add(_provider)
    session.commit()
    session.refresh(_provider)
    return _provider
    
def get_providers(session: Session = Depends(get_session)):
    providers = session.exec(select(Provider)).all()
    return providers

def get_provider(provider_id: int, session: Session = Depends(get_session)):
    provider = session.exec(select(Provider).where(Provider.id == provider_id)).first()
    if provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    return provider

def get_provider_by_name(provider_name: str, session: Session = Depends(get_session)):
    provider = session.exec(select(Provider).where(Provider.name == provider_name)).first()
    if provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    return provider

def update_provider(provider_id: int, provider: ProviderUpdate, session: Session = Depends(get_session)):
    _provider = session.exec(select(Provider).where(Provider.id == provider_id)).first()
    if _provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    _provider.name = provider.name
    _provider.description = provider.description
    _provider.email = provider.email
    _provider.phone = provider.phone
    _provider.address = provider.address
    session.add(_provider)
    session.commit()
    session.refresh(_provider)
    return _provider

def update_provider_by_name(provider_name: str, provider: ProviderUpdate, session: Session = Depends(get_session)):
    _provider = session.exec(select(Provider).where(Provider.name == provider_name)).first()
    if _provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    _provider.name = provider.name
    _provider.description = provider.description
    _provider.email = provider.email
    _provider.phone = provider.phone
    _provider.address = provider.address
    session.add(_provider)
    session.commit()
    session.refresh(_provider)
    return _provider

def delete_provider(provider_id: int, session: Session = Depends(get_session)):
    provider = session.get(Provider, provider_id)
    session.delete(provider)
    session.commit()
    
def delete_provider_by_name(provider_name: str, session: Session = Depends(get_session)):
    provider = session.exec(select(Provider).where(Provider.name == provider_name)).first()
    if provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    session.delete(provider)
    session.commit()
    return provider