from main import get_firewall, logger
from typing import Optional

def register(server):
    @server.tool()
    async def run_op_command(
        command: str,
        sessionId: Optional[str] = None,
        action: Optional[str] = None,
        chatInput: Optional[str] = None,
        toolCallId: Optional[str] = None
    ) -> str:
        """
        Run an operational CLI command on the Palo Alto firewall.
        Args:
            command (str): Any supported operational command, e.g.:
                - "show system info"
                - "show interface all"
                - "show session info"
                - "request system software info"
        Returns:
            str: Raw XML or text output from the firewall
        """
        try:
            if not command:
                return "✗ Error: command is required"
            fw = get_firewall()
            logger.info(f"Running operational command: {command}")
            # Run op command
            result = fw.op(
                command,
                xml=True
            )
            # result is a dict (XML parsed)
            # Convert nicely to string for readability
            output = result if isinstance(result, str) else str(result)
            
            return f"✓ Output for '{command}':\n\n{output}"
        except Exception as e:
            logger.error(f"Failed to run op command '{command}': {str(e)}")
            return f"✗ Error: {str(e)}"
