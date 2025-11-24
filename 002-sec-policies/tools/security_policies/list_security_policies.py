from panos.policies import Rulebase, SecurityRule
from main import get_firewall, logger

def register(server):

    @server.tool()
    async def list_security_policies() -> str:
        """
        List all security policies on the Palo Alto firewall.

        Returns:
            str: A formatted list of rule names and key fields
        """
        try:
            fw = get_firewall()

            rulebase = Rulebase()
            fw.add(rulebase)

            rulebase.refresh()

            rules = rulebase.findall(SecurityRule)

            if not rules:
                return "No security policies found."
            
            logger.info(f"Found {len(rules)} security policies")

            output = ["Security Policies:\n"]
            for rule in rules:
                output.append(
                    f"- {rule.name}: from {rule.fromzone} to {rule.tozone}, "
                    f"src {rule.source}, dst {rule.destination}, application {rule.application}, action {rule.action}"
                )

            return "\n".join(output)

        except Exception as e:
            logger.error(f"Failed to list security policies: {str(e)}")
            return f"✗ Error: {str(e)}"
