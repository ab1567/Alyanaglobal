# ens/xml/builder.py

from ens.models.ics2_ie315 import ICS2IE315
import xml.etree.ElementTree as ET

ICS2_NS = "http://ics2.europa.eu/xsd/ics2-entry-summary-declaration"

def build_ics2_ie315_xml(data: ICS2IE315) -> str:
    """
    Convert an ICS2IE315 object to a standards-compliant ICS2 XML string.
    """
    # Register default namespace
    ET.register_namespace('', ICS2_NS)
    root = ET.Element(f"{{{ICS2_NS}}}EntrySummaryDeclaration")

    # Add fields one by one:
    ET.SubElement(root, "DeclarationReferenceNumber").text = data.declaration_reference_number
    ET.SubElement(root, "DeclarationType").text = data.declaration_type
    ET.SubElement(root, "DeclarationCreationDate").text = data.declaration_creation_date
    ET.SubElement(root, "ConsignmentReferenceNumber").text = data.consignment_reference_number

    if data.master_reference_number:
        ET.SubElement(root, "MasterReferenceNumber").text = data.master_reference_number

    ET.SubElement(root, "CarrierEORI").text = data.carrier_eori
    ET.SubElement(root, "OfficeOfFirstEntry").text = data.office_of_first_entry
    ET.SubElement(root, "ExpectedArrivalDateAndTime").text = data.expected_arrival_date_and_time

    # Parties section (call helper function)
    parties_el = ET.SubElement(root, "Parties")
    _party_to_xml(data.consignor, "Consignor", parties_el)
    _party_to_xml(data.consignee, "Consignee", parties_el)
    if data.notify_party:
        _party_to_xml(data.notify_party, "NotifyParty", parties_el)
    if data.representative:
        _party_to_xml(data.representative, "Representative", parties_el)

    # Arrival transport means
    atm = data.arrival_transport_means
    atm_el = ET.SubElement(root, "ArrivalTransportMeans")
    ET.SubElement(atm_el, "TransportModeCode").text = atm.transport_mode_code
    ET.SubElement(atm_el, "TransportMeansIdentificationTypeCode").text = atm.transport_means_id_type
    ET.SubElement(atm_el, "IdentificationNumber").text = atm.identification_number
    ET.SubElement(atm_el, "NationalityCode").text = atm.nationality_code

    # Inland/Departure transport means
    if data.inland_transport_means:
        itm = data.inland_transport_means
        itm_el = ET.SubElement(root, "InlandTransportMeans")
        if itm.transport_mode_code:
            ET.SubElement(itm_el, "TransportModeCode").text = itm.transport_mode_code
        if itm.identification_number:
            ET.SubElement(itm_el, "IdentificationNumber").text = itm.identification_number
    if hasattr(data, "departure_transport_means") and data.departure_transport_means:
        dtm = data.departure_transport_means
        dtm_el = ET.SubElement(root, "DepartureTransportMeans")
        if dtm.transport_mode_code:
            ET.SubElement(dtm_el, "TransportModeCode").text = dtm.transport_mode_code
        if dtm.identification_number:
            ET.SubElement(dtm_el, "IdentificationNumber").text = dtm.identification_number
        if dtm.nationality_code:
            ET.SubElement(dtm_el, "NationalityCode").text = dtm.nationality_code

    # Goods Items
    goods_items_el = ET.SubElement(root, "GoodsItems")
    for item in data.goods_items:
        _goods_item_to_xml(item, goods_items_el)

    # Optional: Routing, Place of Unloading, Seals, Info
    if data.routing_countries:
        for country in data.routing_countries:
            ET.SubElement(root, "RoutingCountry").text = country
    if data.place_of_unloading:
        ET.SubElement(root, "PlaceOfUnloading").text = data.place_of_unloading
    if data.seals:
        seals_el = ET.SubElement(root, "Seals")
        for seal in data.seals:
            ET.SubElement(seals_el, "SealNumber").text = seal.seal_number
    if data.additional_information:
        ET.SubElement(root, "AdditionalInformation").text = data.additional_information
    if data.circumstances_indicator:
        ET.SubElement(root, "CircumstancesIndicator").text = data.circumstances_indicator
    if data.transport_charges:
        ET.SubElement(root, "TransportCharges").text = str(data.transport_charges)

    # Serialize
    from xml.dom.minidom import parseString
    xml_str = ET.tostring(root, encoding='utf-8')
    return parseString(xml_str).toprettyxml(indent="  ")

# --- Helper functions for submodels ---

def _party_to_xml(party, tag, parent):
    p_el = ET.SubElement(parent, tag)
    ET.SubElement(p_el, "Name").text = party.name
    if party.eori:
        ET.SubElement(p_el, "EORI").text = party.eori
    addr = party.address
    addr_el = ET.SubElement(p_el, "Address")
    ET.SubElement(addr_el, "Street").text = addr.street
    ET.SubElement(addr_el, "City").text = addr.city
    ET.SubElement(addr_el, "PostalCode").text = addr.postal_code
    ET.SubElement(addr_el, "CountryCode").text = addr.country_code
    if getattr(party, "contact_name", None):
        ET.SubElement(p_el, "ContactName").text = party.contact_name
    if getattr(party, "contact_phone", None):
        ET.SubElement(p_el, "ContactPhone").text = party.contact_phone
    if getattr(party, "contact_email", None):
        ET.SubElement(p_el, "ContactEmail").text = party.contact_email

def _goods_item_to_xml(item, parent):
    item_el = ET.SubElement(parent, "GoodsItem")
    ET.SubElement(item_el, "ItemNumber").text = str(item.item_number)
    ET.SubElement(item_el, "Description").text = item.description
    ET.SubElement(item_el, "Quantity").text = str(item.quantity)
    ET.SubElement(item_el, "ValueAmount").text = str(item.value_amount)
    ET.SubElement(item_el, "CurrencyCode").text = item.currency_code
    ET.SubElement(item_el, "CommodityCode").text = item.commodity_code
    ET.SubElement(item_el, "OriginCountry").text = item.origin_country
    ET.SubElement(item_el, "GrossMass").text = str(item.gross_mass)
    if item.documents:
        docs_el = ET.SubElement(item_el, "Documents")
        for doc in item.documents:
            doc_el = ET.SubElement(docs_el, "Document")
            ET.SubElement(doc_el, "DocumentType").text = doc.document_type
            ET.SubElement(doc_el, "DocumentReference").text = doc.document_reference
    if item.additional_information:
        add_info_el = ET.SubElement(item_el, "AdditionalInformation")
        for info in item.additional_information:
            ET.SubElement(add_info_el, "Info").text = info
