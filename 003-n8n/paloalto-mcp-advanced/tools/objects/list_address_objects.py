from panos import objects
from main import get_firewall, logger
from typing import Optional

def register(server):
    @server.tool()
    async def list_address_objects(
        sessionId: Optional[str] = None,
        action: Optional[str] = None,
        chatInput: Optional[str] = None,
        toolCallId: Optional[str] = None
    ) -> str:
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
