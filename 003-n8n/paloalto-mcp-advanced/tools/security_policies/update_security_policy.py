from panos.policies import Rulebase, SecurityRule
from main import get_firewall, logger
from typing import Optional

def register(server):
    @server.tool()
    async def update_security_policy(
        name: str,
        source_zone: Optional[str] = None,
        destination_zone: Optional[str] = None,
        source_address: Optional[str] = None,
        destination_address: Optional[str] = None,
        application: Optional[str] = None,
        action_type: Optional[str] = None,
        description: Optional[str] = None,
        sessionId: Optional[str] = None,
        action: Optional[str] = None,
        chatInput: Optional[str] = None,
        toolCallId: Optional[str] = None
    ) -> str:
        """
        Update an existing security policy. Only provided fields will be updated.
        Args:
            name: Rule name (required)
            source_zone: New source zone (can be comma-separated for multiple, e.g., "trust,dmz")
            destination_zone: New dest zone (can be comma-separated for multiple, e.g., "untrust,dmz")
            source_address: New source address (can be comma-separated for multiple, e.g., "any,10.0.0.1")
            destination_address: New dest address (can be comma-separated for multiple, e.g., "any,8.8.8.8")
            application: New application (can be comma-separated for multiple, e.g., "dns,ssh")
            action_type: New action (allow/deny)
            description: New description
        Returns:
            str: Success or error message
        """
        try:
            if not name:
                return "✗ Error: Rule name is required"
            fw = get_firewall()
            rulebase = Rulebase()
            fw.add(rulebase)
            rulebase.refresh()
            rule = rulebase.find(name, SecurityRule)
            if not rule:
                return f"✗ Error: Security policy '{name}' not found"
            # Update only provided fields
            # These fields accept lists, so split on comma
            if source_zone:
                rule.fromzone = [zone.strip() for zone in source_zone.split(',')]
            if destination_zone:
                rule.tozone = [zone.strip() for zone in destination_zone.split(',')]
            if source_address:
                rule.source = [addr.strip() for addr in source_address.split(',')]
            if destination_address:
                rule.destination = [addr.strip() for addr in destination_address.split(',')]
            if application:
                rule.application = [app.strip() for app in application.split(',')]
            
            # These fields are single values
            if action_type:
                rule.action = action_type
            if description:
                rule.description = description
            rule.apply()
            logger.info(f"Updated security policy: {name}")
            return f"✓ Successfully updated security policy '{name}'"
        except Exception as e:
            logger.error(f"Failed to update security policy '{name}': {str(e)}")
            return f"✗ Error: {str(e)}"
