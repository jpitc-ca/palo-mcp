from panos import objects
from main import get_firewall, logger
from typing import Optional

def register(server):
    @server.tool()
    async def delete_address_object(
        name: str,
        sessionId: Optional[str] = None,
        action: Optional[str] = None,
        chatInput: Optional[str] = None,
        toolCallId: Optional[str] = None
    ) -> str:
        """
        Delete an address object from the Palo Alto firewall.
    
        Args:
            name: Name of the address object to delete
    
        Returns:
            str: Success or error message
        """
        
        try:
            if not name:
                return "✗ Error: name is required"
            fw = get_firewall()
            objects.AddressObject.refreshall(fw)
            addr = fw.find(name, objects.AddressObject)
            if addr is None:
                return f"✗ Address object '{name}' not found"
            addr.delete()
            logger.info(f"Deleted address object: {name}")
            return f"✓ Successfully deleted address object '{name}'"
        except Exception as e:
            logger.error(f"Failed: {str(e)}")
            return f"✗ Error: {str(e)}"
