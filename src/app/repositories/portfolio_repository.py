from src.app.database.models import Portfolio, PortfolioAsset, PortfolioTransaction
from .base_repository import Repository


class PortfolioRepostory(Repository):
    model = Portfolio


class PortfolioAsset(Repository):
    model = PortfolioAsset


class PortfolioTransaction(Repository):
    model = PortfolioTransaction
