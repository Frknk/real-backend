from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from src.routes.sales.models import Sale, ProductSale, SaleCreate, SaleRead, ProductSaleRead, CustomerRead
from src.routes.customers.models import Customer
from src.routes.products.models import Product
from src.database import get_session

def read_sale(sale_id: int, session: Session = Depends(get_session)):
    statement = (
        select(Sale, Product, ProductSale)
        .join(ProductSale, Sale.id == ProductSale.sale_id)
        .join(Product, ProductSale.product_id == Product.id)
        .where(Sale.id == sale_id)
    )
    
    results = session.exec(statement).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    sale = results[0][0]
    customer = session.exec(select(Customer).where(Customer.dni == sale.customer_dni)).first()  # Now using the actual sale's user_dni

    customer_read = CustomerRead(
        dni=customer.dni,
        name=customer.name,
        last_name=customer.last_name,
        email=customer.email
    )

    # Collect product details with quantities
    products_details = []
    for _, product, product_sale in results:
        product_detail = ProductSaleRead(
            name=product.name,  # Assuming you have a name field in Product
            price=product.price,  # Assuming you have a price field in Product
            brand=product.brand,
            category=product.category,  # If you have a category
            provider_id=product.provider_id,  # If applicable
            quantity=product_sale.quantity
        )
        products_details.append(product_detail)
        
    sale_read = SaleRead(
        id=sale.id,
        created_at=sale.created_at,
        total=sale.total,
        products=products_details,
        customer=customer_read
    )
    
    return sale_read

def create_sale(sale_input: SaleCreate, session: Session = Depends(get_session)):
    # Fetch products
    products = []
    total_amount = 0

    # Check if user exists
    if not session.exec(select(Customer).where(Customer.dni == sale_input.customer_dni)).first():
        raise HTTPException(status_code=404, detail="User not found")

    # Check of products is empty
    if not sale_input.products:
        raise HTTPException(status_code=400, detail="No products provided")
    
    for item in sale_input.products:
        product = session.get(Product, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        # check if enought stock
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.name}")

        # remove stock
        product.stock -= item.quantity
        
        total_amount += product.price * item.quantity
        products.append(product)

    # Create sale
    sale = Sale(customer_dni=sale_input.customer_dni, total=total_amount)
    session.add(sale)
    session.flush()  # To get sale ID

    # Create product sales
    for item in sale_input.products:
        product_sale = ProductSale(
            product_id=item.product_id,
            sale_id=sale.id,
            quantity=item.quantity
        )
        #print(product_sale)
        session.add(product_sale)

    session.commit()
    session.refresh(sale)

    return sale