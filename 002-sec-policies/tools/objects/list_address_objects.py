from panos import objects
from main import get_firewall, logger

def register(server):

    @server.tool()
    async def list_address_objects() -> str:
        """
        List all address objects on the Palo Alto firewall.
    
        Returns:
            str: List of address objects or error message
        """
        try:
            fw = get_firewall()
            addresses = objects.AddressObject.refreshall(fw)

            if not addresses:
                return "No address objects found."

            lines = [f"Found {len(addresses)} object(s):\n"]
            logger.info(f"Found {len(addresses)} object(s)")
            
            for addr in addresses:
                lines.append(f"Name: {addr.name}")
                lines.append(f"  Value: {addr.value}")
                if addr.description:
                    lines.append(f"  Description: {addr.description}")
                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            logger.error(f"Failed: {str(e)}")
            return f"✗ Error: {str(e)}"
