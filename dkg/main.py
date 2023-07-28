from functools import wraps

from dkg.asset import ContentAsset
from dkg.graph import Graph
from dkg.manager import DefaultRequestManager
from dkg.module import Module
from dkg.node import Node
from dkg.providers import BlockchainProvider, NodeHTTPProvider
from dkg.types import UAL, Address, ChecksumAddress
from dkg.utils.ual import format_ual, parse_ual


class DKG(Module):
    asset: ContentAsset
    node: Node
    graph: Graph

    @staticmethod
    @wraps(format_ual)
    def format_ual(
        blockchain: str, contract_address: Address | ChecksumAddress, token_id: int
    ) -> UAL:
        return format_ual(blockchain, contract_address, token_id)

    @staticmethod
    @wraps(parse_ual)
    def parse_ual(ual: UAL) -> dict[str, str | Address | int]:
        return parse_ual(ual)

    def __init__(
        self,
        node_provider: NodeHTTPProvider,
        blockchain_provider: BlockchainProvider,
    ):
        self.manager = DefaultRequestManager(node_provider, blockchain_provider)
        modules = {
            "asset": ContentAsset(self.manager),
            "node": Node(self.manager),
            "graph": Graph(self.manager),
        }
        self._attach_modules(modules)

    @property
    def node_provider(self) -> NodeHTTPProvider:
        return self.manager.node_provider

    @node_provider.setter
    def node_provider(self, node_provider: NodeHTTPProvider) -> None:
        self.manager.node_provider = node_provider

    @property
    def blockchain_provider(self) -> BlockchainProvider:
        return self.manager.blockchain_provider

    @blockchain_provider.setter
    def blockchain_provider(self, blockchain_provider: BlockchainProvider) -> None:
        self.manager.blockchain_provider = blockchain_provider