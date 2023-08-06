"""Huggingface chatbot interface client implementation."""
from typing import List
import zmq
from npc_engine.service_clients.service_client import ServiceClient


class SimilarityClient(ServiceClient):
    """Json rpc client for chatbot service."""

    def __init__(
        self, zmq_context: zmq.Context, port: str, service_id: str = "SimilarityAPI"
    ):
        """Connect to the server on the port."""
        super().__init__(zmq_context, port, service_id)

    def compare(self, query: str, context: List[str]) -> str:
        """Send a chatbot request to the server.

        Args:
            context: A dictionary containing the chatbot request.
        """
        request = {
            "jsonrpc": "2.0",
            "method": "compare",
            "id": 0,
            "params": [query, context],
        }
        reply = self.send_request(request)
        return reply
