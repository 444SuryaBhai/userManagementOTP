from fastapi import Request

def get_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.client.host
    return ip

def get_mac_address(request: Request) -> str:
    # MAC address is not available via HTTP; placeholder for future device fingerprinting
    return "unknown" 