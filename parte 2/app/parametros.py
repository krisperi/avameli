PARAMETER_MAP = {
    "palo_alto": {
        "encryption": {
            "des": "des",
            "3des": "3des",
            "aes128": "aes-128-cbc",
            "aes256": "aes-256-cbc"
        },
        "integrity": {
            "sha1": "sha1",
            "sha256": "sha256"
        },
        "dh_group": {
            "group14": "group14"
        },
        "pfs_group": {
            "group14": "group14"
        },
        "ike_version": {
            "ikev2": "ikev2"
        }
    },

    "fortigate": {
        "encryption": {
            "des": "des",
            "3des": "3des",
            "aes128": "aes128",
            "aes256": "aes256"
        },
        "integrity": {
            "sha1": "sha1",
            "sha256": "sha256"
        },
        "dh_group": {
            "group14": "14"
        },
        "pfs_group": {
            "group14": "14"
        },
        "ike_version": {
            "ikev2": "2"
        }
    }
}


def map_parameters(vendor, phase1, phase2):
    vendor_map = PARAMETER_MAP[vendor]

    return {
        "phase1": {
            "ike_version": vendor_map["ike_version"][phase1["ike_version"]],
            "authentication": phase1["authentication"],
            "encryption": vendor_map["encryption"][phase1["encryption"]],
            "integrity": vendor_map["integrity"][phase1["integrity"]],
            "dh_group": vendor_map["dh_group"][phase1["dh_group"]],
            "lifetime": phase1["lifetime"]
        },
        "phase2": {
            "encryption": vendor_map["encryption"][phase2["encryption"]],
            "integrity": vendor_map["integrity"][phase2["integrity"]],
            "pfs": phase2["pfs"],
            "pfs_group": vendor_map["pfs_group"][phase2["pfs_group"]],
            "lifetime": phase2["lifetime"]
        }
    }