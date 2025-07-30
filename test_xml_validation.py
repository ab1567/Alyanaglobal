from ens.models.ics2_ie315 import ICS2IE315, Address, Party, ArrivalTransportMeans, GoodsItem
from ens.xml.builder import build_ics2_ie315_xml
from ens.validators.xsd_validator import validate_xml_against_xsd

data = ICS2IE315(
    declaration_reference_number="1001",
    declaration_creation_date="2025-07-09T09:07:34",
    consignment_reference_number="DUMMY-CONSIGNMENT-ID",
    carrier_eori="SE987654321000",
    office_of_first_entry="SE003099",
    expected_arrival_date_and_time="2025-07-10T11:00:00",
    consignor=Party(
        name="Acme AB",
        address=Address(street="1234 Main St", city="Stockholm", postal_code="11120", country_code="SE")
    ),
    consignee=Party(
        name="Receiver AB",
        address=Address(street="5678 Elm St", city="Gothenburg", postal_code="41120", country_code="SE")
    ),
    arrival_transport_means=ArrivalTransportMeans(
        transport_mode_code="4",
        transport_means_id_type="10",
        identification_number="LH123",
        nationality_code="DE"
    ),
    goods_items=[
        GoodsItem(
            item_number=1,
            description="Mobile Phones",
            quantity=10,
            value_amount=1500.0,
            currency_code="EUR",
            commodity_code="8517120000",
            origin_country="CN",
            gross_mass=12.3
        )
    ]
)

xml_string = build_ics2_ie315_xml(data)
print(xml_string)

xsd_path = "ens/resources/ics2-entry-summary-declaration.xsd"
try:
    validate_xml_against_xsd(xml_string, xsd_path)
    print("XML is valid against ICS2 XSD!")
except ValueError as e:
    print("Validation error:", e)
