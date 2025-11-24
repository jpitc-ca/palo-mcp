from panos.policies import Rulebase, SecurityRule
from main import get_firewall, logger

def register(server):

    @server.tool()
    async def create_security_policy(
        name: str,
        source_zone: str,
        destination_zone: str,
        source_address: str,
        destination_address: str,
        application: str = "any",
        action: str = "allow",
        description: str = "",
    ) -> str:
        """
        Create a new security policy on the Palo Alto firewall.
    
        Args:
            name: Name of the security policy
            source_zone: Source zone (can be comma-separated for multiple, e.g., "trust,dmz")
            destination_zone: Destination zone (can be comma-separated for multiple, e.g., "untrust,dmz")
            source_address: Source address object name (can be comma-separated for multiple, e.g., "any,10.0.0.1")
            destination_address: Destination address object name (can be comma-separated for multiple, e.g., "any,8.8.8.8")
            application: Application name (can be comma-separated for multiple, e.g., "dns,ssh", default: 'any')
            action: 'allow' or 'deny' (default: 'allow')
            description: Optional description
    
        Returns:
            str: Success or error message
        """
        try:
            fw = get_firewall()
    
            rulebase = Rulebase()
            fw.add(rulebase)
    
            rule = SecurityRule(
                name=name,
                fromzone=[zone.strip() for zone in source_zone.split(',')],
                tozone=[zone.strip() for zone in destination_zone.split(',')],
                source=[addr.strip() for addr in source_address.split(',')],
                destination=[addr.strip() for addr in destination_address.split(',')],
                application=[app.strip() for app in application.split(',')],
                action=action,
                description=description,
            )
    
            rulebase.add(rule)
            rule.create()
    
            logger.info(f"Created security policy: {name}")
            return f"✓ Successfully created security policy '{name}'"
    
        except Exception as e:
            logger.error(f"Failed to create security policy '{name}': {str(e)}")
            return f"✗ Error: {str(e)}"