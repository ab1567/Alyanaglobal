from typing import List, Optional
from pydantic import BaseModel, Field

class Address(BaseModel):
    """Address used by any Party in the ENS/ICS2 context."""
    street: str = Field(..., example="1234 Main Street")
    city: str = Field(..., example="Stockholm")
    postal_code: str = Field(..., example="11120")
    country_code: str = Field(..., min_length=2, max_length=2, example="SE", description="ISO 3166-1 alpha-2")

class Party(BaseModel):
    """A party (consignor, consignee, etc.) in the ICS2 ENS."""
    name: str = Field(..., example="Acme AB")
    eori: Optional[str] = Field(None, example="SE123456789012")
    address: Address
    contact_name: Optional[str] = Field(None, example="John Doe")
    contact_phone: Optional[str] = Field(None, example="+46701234567")
    contact_email: Optional[str] = Field(None, example="info@acme.se")
    # role: Optional[str] = Field(None, description="e.g., 'notify_party', 'representative' if required by future schemas")

class ArrivalTransportMeans(BaseModel):
    """Arrival transport means as per ICS2 (air/sea/road/rail)."""
    transport_mode_code: str = Field(..., example="4")  # "4"=Air, "1"=Sea, etc.
    transport_means_id_type: str = Field(..., example="10")  # "10"=Flight number, "11"=IMO, etc.
    identification_number: str = Field(..., example="LH123")
    nationality_code: str = Field(..., example="DE")

class InlandTransportMeans(BaseModel):
    transport_mode_code: Optional[str] = Field(None)
    identification_number: Optional[str] = Field(None)

class DepartureTransportMeans(BaseModel):
    """Optional. Used for multimodal or transshipments if required."""
    transport_mode_code: Optional[str] = Field(None)
    identification_number: Optional[str] = Field(None)
    nationality_code: Optional[str] = Field(None)

class Document(BaseModel):
    """Supporting document, e.g., waybill, invoice."""
    document_type: str = Field(..., example="AWB")
    document_reference: str = Field(..., example="123-45678901")

class Seal(BaseModel):
    seal_number: str = Field(..., example="SEAL12345")

class GoodsItem(BaseModel):
    item_number: int = Field(..., example=1)
    description: str = Field(..., example="Mobile Phones")
    quantity: float = Field(..., example=10)
    value_amount: float = Field(..., example=1500.00)
    currency_code: str = Field(..., example="EUR")
    commodity_code: str = Field(..., example="8517120000")
    origin_country: str = Field(..., example="CN")
    gross_mass: float = Field(..., example=12.3)
    documents: Optional[List[Document]] = Field(None)
    additional_information: Optional[List[str]] = Field(None, example=["Fragile", "Lithium batteries"])

class ICS2IE315(BaseModel):
    """
    ICS2 ENS IE315 data model.
    This model covers all common and extended fields for ENS filings.
    """
    declaration_reference_number: str = Field(..., example="1001")
    declaration_type: str = Field("IE315", example="IE315")
    declaration_creation_date: str = Field(..., example="2025-07-09T09:07:34")
    consignment_reference_number: str = Field(..., example="DUMMY-CONSIGNMENT-ID")
    master_reference_number: Optional[str] = Field(None, example="MRN1234567890")
    carrier_eori: str = Field(..., example="SE987654321000")
    office_of_first_entry: str = Field(..., example="SE003099")
    expected_arrival_date_and_time: str = Field(..., example="2025-07-10T11:00:00")
    version: Optional[str] = Field(None, example="1.0")

    consignor: Party
    consignee: Party
    notify_party: Optional[Party] = None
    representative: Optional[Party] = None

    arrival_transport_means: ArrivalTransportMeans
    inland_transport_means: Optional[InlandTransportMeans] = None
    departure_transport_means: Optional[DepartureTransportMeans] = None

    goods_items: List[GoodsItem]

    routing_countries: Optional[List[str]] = Field(None, example=["DE", "DK"])
    place_of_unloading: Optional[str] = Field(None, example="SESTO")
    seals: Optional[List[Seal]] = None
    additional_information: Optional[str] = None
    circumstances_indicator: Optional[str] = None
    transport_charges: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "declaration_reference_number": "1001",
                "declaration_creation_date": "2025-07-09T09:07:34",
                "consignment_reference_number": "DUMMY-CONSIGNMENT-ID",
                "carrier_eori": "SE987654321000",
                "office_of_first_entry": "SE003099",
                "expected_arrival_date_and_time": "2025-07-10T11:00:00",
                "consignor": {
                    "name": "Acme AB",
                    "eori": "SE123456789012",
                    "address": {
                        "street": "1234 Main Street",
                        "city": "Stockholm",
                        "postal_code": "11120",
                        "country_code": "SE"
                    }
                },
                "consignee": {
                    "name": "Receiver AB",
                    "eori": "SE987654321098",
                    "address": {
                        "street": "5678 Elm Street",
                        "city": "Gothenburg",
                        "postal_code": "41120",
                        "country_code": "SE"
                    }
                },
                "arrival_transport_means": {
                    "transport_mode_code": "4",
                    "transport_means_id_type": "10",
                    "identification_number": "LH123",
                    "nationality_code": "DE"
                },
                "goods_items": [
                    {
                        "item_number": 1,
                        "description": "Mobile Phones",
                        "quantity": 10,
                        "value_amount": 1500.0,
                        "currency_code": "EUR",
                        "commodity_code": "8517120000",
                        "origin_country": "CN",
                        "gross_mass": 12.3
                    }
                ]
            }
        }
