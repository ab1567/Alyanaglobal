from pathlib import Path
from lxml import etree
from signxml import XMLSigner, methods

SIGN_METHOD = methods.enveloped
DIGEST_ALG = "sha256"

def sign_xml(
    xml_string: str,
    cert_path: str | Path = "/etc/ssl/autoens/signing_cert.pem",
    key_path: str | Path = "/etc/ssl/autoens/autoens_tls.key",
    key_passphrase: str | None = None,
) -> str:
    """
    Returns an XML string with an embedded <Signature> element.
    """
    # load doc
    doc = etree.fromstring(xml_string.encode("utf-8"))

    # read key / cert
    key_bytes = Path(key_path).read_bytes()
    cert_bytes = Path(cert_path).read_bytes()

    # build signer
    signer = XMLSigner(
        method=SIGN_METHOD,
        signature_algorithm="rsa-sha256",
        digest_algorithm=DIGEST_ALG,
        c14n_algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"
    )

    # sign (signxml 2.x: no signature_id param)
    signed_root = signer.sign(
        doc,
        key=key_bytes,
        cert=cert_bytes,
        passphrase=key_passphrase,
        reference_uri=None
    )

    return etree.tostring(
        signed_root,
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8"
    ).decode("utf-8")
