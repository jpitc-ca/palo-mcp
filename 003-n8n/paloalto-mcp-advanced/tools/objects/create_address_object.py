"""
Create Address Object Tool
"""
from panos import objects
from main import get_firewall, logger
from typing import Optional

def register(server):
    """Register the create_address_object tool with the MCP server."""
    
    @server.tool()
    async def create_address_object(
        name: str,
        ip_address: str,
        description: str = "",
        sessionId: Optional[str] = None,
        action: Optional[str] = None,
        chatInput: Optional[str] = None,
        toolCallId: Optional[str] = None
    ) -> str:
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
            logger.error(f"Failed to create address object: {str(e)}")
            return f"✗ Error: {str(e)}"
