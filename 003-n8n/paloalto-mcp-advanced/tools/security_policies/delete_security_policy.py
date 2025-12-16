from panos.policies import Rulebase, SecurityRule
from main import get_firewall, logger
from typing import Optional

def register(server):
    @server.tool()
    async def delete_security_policy(
        name: str,
        sessionId: Optional[str] = None,
        action: Optional[str] = None,
        chatInput: Optional[str] = None,
        toolCallId: Optional[str] = None
    ) -> str:
        """
        Delete a security policy by name.
        Args:
            name: Name of the security rule to delete
        Returns:
            str: Success or error message
        """
        try:
            if not name:
                return "✗ Error: Rule name is required"
            fw = get_firewall()
            rulebase = Rulebase()
            fw.add(rulebase)
            # Pull existing rules
            rulebase.refresh()
            # Find rule
            rule = rulebase.find(name, SecurityRule)
            if not rule:
                return f"✗ Error: Security policy '{name}' not found"
            rule.delete()
            logger.info(f"Deleted security policy: {name}")
            return f"✓ Successfully deleted security policy '{name}'"
        except Exception as e:
            logger.error(f"Failed to delete security policy '{name}': {str(e)}")
            return f"✗ Error: {str(e)}"
