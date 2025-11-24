from panos import objects
from main import get_firewall, logger

def register(server):

    @server.tool()
    async def create_address_object(name: str, ip_address: str, description: str = "") -> str:
        """
        Create an address object on the Palo Alto firewall.
    
        Args:
            name: Name of the address object (e.g., "Server1")
            ip_address: IP address or CIDR (e.g., "192.168.1.10" or "192.168.1.0/24")
            description: Optional description for the address object
    
        Returns:
            str: Success or error message
        """
        try:
            if not name or not ip_address:
                return "✗ Error: name and ip_address are required"

            fw = get_firewall()

            addr = objects.AddressObject(
                name=name,
                value=ip_address,
                description=description
            )

            fw.add(addr)
            addr.create()

            logger.info(f"Created address object: {name} -> {ip_address}")
            return f"✓ Successfully created address object '{name}' with IP {ip_address}"

        except Exception as e:
            logger.error(f"Failed: {str(e)}")
            return f"✗ Error: {str(e)}"
