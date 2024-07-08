
import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app import schemas 
from typing import List
from app.database import SessionLocal, engine, get_db
from uuid import UUID
from sqlalchemy.exc import NoResultFound
import requests
from app import controllers
from app.models.models import TurnoVehiculos
from app.models.models import Turno as TurnoModel
from app.models.models import Vehiculo as VehiculoModel


token_data = {
    "access_token": None,
    "expires_at": None
}


def obtener_token_self_client(client_id, client_secret):
    url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "ZohoSubscriptions.fullaccess.all"
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get('access_token')
        expires_in = token_info.get('expires_in')
        
        # Guardar el token y su tiempo de expiración
        token_data["access_token"] = access_token
        token_data["expires_at"] = time.time() + expires_in
        
        return access_token
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())


client_id = "1000.2XN8PCJIW8RDRCEN2RSNE4VEB5686F"
client_secret = "825979c68dbc646e0993d616f09c779d5f2cd0d2af"


def obtener_token_actual(client_id, client_secret):
    if token_data["access_token"] and token_data["expires_at"] > time.time():
        return token_data["access_token"]
    else:
        return obtener_token_self_client(client_id, client_secret)




def crear_cliente(cliente_data):
    access_token = obtener_token_actual(client_id, client_secret)
    zoho_books_api_url = "https://www.zohoapis.com/billing/v1/contacts?organization_id=857084194"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(zoho_books_api_url, json=cliente_data, headers=headers)
    if response.status_code == 201:
        return response.json().get("contact").get("contact_id")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())



def crear_factura(factura: schemas.Invoice):
    print("Entro a crear factura")
    access_token = obtener_token_actual(client_id, client_secret)
    zoho_books_api_url = f"https://www.zohoapis.com/billing/v1/invoices?organization_id=857084194"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "customer_id": factura.customer_id,
        "currency_id": factura.currency_id,
        "due_date": factura.due_date,
        "invoice_items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "rate": item.rate
            } for item in factura.invoice_items
        ],
        "payment_options": {
            "payment_gateways": [
                {
                    "configured": gateway.configured,
                    "additional_field1": gateway.additional_field1,
                    "gateway_name": gateway.gateway_name
                } for gateway in factura.payment_options.payment_gateways
            ]
        },
        "allow_partial_payments": factura.allow_partial_payments
    }
    response = requests.post(zoho_books_api_url, json=data, headers=headers)
    if response.status_code == 201:
        invoice_id=response.json().get("invoice").get("invoice_id")
        url_sent = f"https://billing.zoho.com/api/v3/invoices/{invoice_id}/status/sent?organization_id=857084194"
        headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
        }
        response_sent = requests.post(url_sent, headers=headers)
        
        ##set stripe
        url_put_stripe=f"https://billing.zoho.com/api/v3/invoices/{invoice_id}?organization_id=857084194"
        headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
        }
        data={"payment_options":{"payment_gateways":[{"gateway_name":"test_gateway"}]}}
        response_put = requests.put(url_put_stripe, json=data,headers=headers)


        return response.json().get("invoice")
    

    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())
   



def search_item_zoho_billing(item_name):
    print("Entro a buscar items")
    access_token = obtener_token_actual(client_id, client_secret)
    url = f"https://www.zohoapis.com/billing/v1/items?organization_id=857084194&name_contains={item_name}"
    print(access_token)
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code == 200:
        items = response.json().get("items")
        if items:
            return items[0].get("item_id")
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())


def crear_factura_from_turno(db: Session, uuidTurno: str, customer_id: str, currency_id: str, due_date: str):
    turnos = db.query(TurnoModel).filter(TurnoModel.uuidTurno == uuidTurno)\
    .join(TurnoVehiculos, TurnoVehiculos.uuidTurno == TurnoModel.uuidTurno)\
    .join(VehiculoModel, TurnoVehiculos.uuidVehiculo == VehiculoModel.uuidvehiculo).all()
    
    if not turnos:
        raise HTTPException(status_code=404, detail="Turno not found")

    turno = turnos[0] 
    detalles = turno.detalles

    invoice_items = []
    for detalle in detalles:
        item_id = search_item_zoho_billing(detalle.descripcion)  
        invoice_item = schemas.InvoiceItem(
            product_id=item_id,
            quantity=detalle.cantidad, 
            rate=detalle.costo_total / detalle.cantidad  
        )
        invoice_items.append(invoice_item)

    payment_options = schemas.PaymentOptions(
        payment_gateways=[
            schemas.PaymentGateway(
                configured=True,
                additional_field1="standard",
                gateway_name="test_gateway"
            )
        ]
    )

    factura = schemas.Invoice(
        customer_id=customer_id,
        currency_id=currency_id,
        due_date=due_date,
        invoice_items=invoice_items,
        payment_options=payment_options,
        allow_partial_payments=False
    )
    return crear_factura(factura)
