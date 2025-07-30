from lxml import etree

def validate_xml_against_xsd(xml_string: str, xsd_path: str) -> bool:
    """
    Validate XML string against the XSD file at xsd_path.
    Returns True if valid, raises ValueError otherwise.
    """
    xml_doc = etree.fromstring(xml_string.encode("utf-8"))
    with open(xsd_path, 'rb') as xsd_file:
        xsd_doc = etree.parse(xsd_file)
        xsd = etree.XMLSchema(xsd_doc)
        if not xsd.validate(xml_doc):
            errors = "\n".join([str(e) for e in xsd.error_log])
            raise ValueError(f"XML failed XSD validation:\n{errors}")
    return True
