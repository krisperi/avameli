SUPPORTED_VENDORS = ["palo_alto", "fortigate"]


def is_supported_vendor(vendor):
    return vendor in SUPPORTED_VENDORS


def get_supported_vendors_message():
    return ", ".join(SUPPORTED_VENDORS)