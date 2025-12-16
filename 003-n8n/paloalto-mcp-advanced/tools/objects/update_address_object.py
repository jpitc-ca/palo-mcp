from panos import objects
from main import get_firewall, logger
from typing import Optional

def register(server):
    @server.tool()
    async def update_address_object(
        name: str,
        new_ip: Optional[str] = None,
        new_description: Optional[str] = None,
        sessionId: Optional[str] = None,
        action: Optional[str] = None,
        chatInput: Optional[str] = None,
        toolCallId: Optional[str] = None
    ) -> str:
        """
        Update an existing address object on the Palo Alto firewall.
    
        Args:
            name: Name of the address object to update
            new_ip: New IP address or CIDR (optional)
            new_description: New description (optional)
    
        Returns:
            str: Success or error message
        """
        
        try:
            if not name:
                return "✗ Error: name is required"
            if new_ip is None and new_description is None:
                return "✗ Error: provide new_ip or new_description"
            fw = get_firewall()
            objects.AddressObject.refreshall(fw)
            addr = fw.find(name, objects.AddressObject)
            if addr is None:
                return f"✗ Address object '{name}' not found"
            if new_ip:
                addr.value = new_ip
            if new_description is not None:
                addr.description = new_description
            addr.apply()
            
            logger.info(f"Updated address object: {name}")
            return f"✓ Successfully updated address object '{name}'"
        except Exception as e:
            logger.error(f"Failed: {str(e)}")
            return f"✗ Error: {str(e)}"
