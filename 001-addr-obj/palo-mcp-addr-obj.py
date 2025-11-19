from mcp.server.fastmcp import FastMCP
from panos import firewall, objects
import urllib3
from typing import Optional
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable SSL warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

server = FastMCP("Palo Alto Firewall Manager")

# Configuration - load from environment variables
FIREWALL_IP = os.getenv("FIREWALL_IP", "1.2.3.4")
API_KEY = os.getenv("FIREWALL_API_KEY", "api-key")

if not API_KEY:
    raise ValueError("FIREWALL_API_KEY environment variable is required")

# Global state - connection persists across tool calls within same server session
_firewall_instance: Optional[firewall.Firewall] = None

def get_firewall() -> firewall.Firewall:
    """
    Get or create a firewall instance.
    The MCP server maintains this connection for the lifetime of the Claude Desktop session,
    so subsequent calls reuse the same connection.
    """
    global _firewall_instance
    
    if _firewall_instance is None:
        try:
            _firewall_instance = firewall.Firewall(
                FIREWALL_IP,
                api_key=API_KEY
            )
            logger.info("Connected to firewall")
        except Exception as e:
            logger.error(f"Failed to connect to firewall: {str(e)}")
            raise Exception(f"Failed to connect to firewall: {str(e)}")
    
    return _firewall_instance

@server.tool()
async def create_address_object(
    name: str, 
    ip_address: str, 
    description: str = ""
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

@server.tool()
async def list_address_objects() -> str:
    """
    List all address objects on the Palo Alto firewall.
    
    Returns:
        str: List of address objects or error message
    """
    try:
        fw = get_firewall()
        
        # Fresh query each time - data may have changed outside Claude
        addresses = objects.AddressObject.refreshall(fw)
        
        if not addresses:
            return "No address objects found on the firewall."
        
        lines = [f"Found {len(addresses)} address object(s):\n"]
        for addr in addresses:
            lines.append(f"Name: {addr.name}")
            lines.append(f"  Value: {addr.value}")
            if addr.description:
                lines.append(f"  Description: {addr.description}")
            lines.append("")
        
        return "\n".join(lines)
    
    except Exception as e:
        logger.error(f"Failed to list address objects: {str(e)}")
        return f"✗ Error: {str(e)}"

@server.tool()
async def delete_address_object(name: str) -> str:
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
        
        # Refresh to get current state
        objects.AddressObject.refreshall(fw)
        addr = fw.find(name, objects.AddressObject)
        
        if addr is None:
            return f"✗ Address object '{name}' not found"
        
        addr.delete()
        
        logger.info(f"Deleted address object: {name}")
        return f"✓ Successfully deleted address object '{name}'"
    
    except Exception as e:
        logger.error(f"Failed to delete address object: {str(e)}")
        return f"✗ Error: {str(e)}"

@server.tool()
async def update_address_object(
    name: str, 
    new_ip: Optional[str] = None, 
    new_description: Optional[str] = None
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
            return "✗ Error: at least one of new_ip or new_description must be provided"
        
        fw = get_firewall()
        
        # Refresh to get current state
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
        logger.error(f"Failed to update address object: {str(e)}")
        return f"✗ Error: {str(e)}"

if __name__ == "__main__":
    server.run(transport="stdio")