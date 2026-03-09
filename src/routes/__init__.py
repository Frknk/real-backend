from fastapi import APIRouter, Depends
from src.routes.products.views import router as products_router
from src.routes.categories.views import router as categories_router
from src.routes.providers.views import router as providers_router
from src.routes.brands.views import router as brands_router
from src.routes.customers.views import router as customers_router
from src.routes.sales.views import router as sales_router
from src.routes.auth.views import router as auth_router
from src.routes.auth.operations import get_current_user

root_router = APIRouter()

crud_dependencies = [Depends(get_current_user)]

root_router.include_router(
    products_router,
    prefix="/products",
    tags=["products"],
    dependencies=crud_dependencies,
)
root_router.include_router(
    categories_router,
    prefix="/categories",
    tags=["categories"],
    dependencies=crud_dependencies,
)
root_router.include_router(
    providers_router,
    prefix="/providers",
    tags=["providers"],
    dependencies=crud_dependencies,
)
root_router.include_router(
    brands_router,
    prefix="/brands",
    tags=["brands"],
    dependencies=crud_dependencies,
)
root_router.include_router(
    customers_router,
    prefix="/customers",
    tags=["customers"],
    dependencies=crud_dependencies,
)
root_router.include_router(
    sales_router,
    prefix="/sales",
    tags=["sales"],
    dependencies=crud_dependencies,
)
root_router.include_router(auth_router, prefix="/auth", tags=["auth"])
