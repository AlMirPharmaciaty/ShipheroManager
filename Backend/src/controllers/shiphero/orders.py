from datetime import date
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

from src.config.settings import Settings
from src.schemas.shiphero_schema import shiphero_schema


settings = Settings()
SHIPHERO_URL = settings.SHIPHERO_URL
SHIPHERO_TOKEN = settings.SHIPHERO_TOKEN


class OrdersController:
    """Shiphero Orders Controller"""

    def __init__(self):
        self.graphql = HTTPEndpoint(
            SHIPHERO_URL,
            base_headers={'Authorization': f'Bearer {SHIPHERO_TOKEN}'})

    def extract(self,
                from_date: str | None = str(date.today()),
                limit: int | None = 10,
                after: str | None = ''):
        """
        Extract data from orders repo
        """
        # Build the query
        op = Operation(shiphero_schema.Query)
        # Building the orders query
        query = op.orders(order_date_from=from_date)
        # Make sure to request the complexity and request_id
        query.complexity()
        query.request_id()
        # Get the first N data and define the selections
        query_data = query.data(first=limit, after=after)
        select = query_data.edges.node
        select.id()
        select.order_number()
        select.fulfillment_status()
        select.source()
        select.shop_name()
        select.total_price()
        select.tags()
        select.order_history.id()
        select.order_history.information()
        select.order_history.created_at()
        select.order_history.username()
        # Pagination info
        query_data.page_info.has_next_page()
        query_data.page_info.end_cursor()
        # Executing the call
        return self.graphql(op)
