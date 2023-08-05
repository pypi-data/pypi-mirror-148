"""Cofactr graph API client."""
# Python Modules
from functools import partial
import json
from typing import List, Literal, Optional

# 3rd Party Modules
import urllib3

from cofactr.cursor import Cursor

Protocol = Literal["http", "https"]


drop_none_values = lambda d: {k: v for k, v in d.items() if v is not None}


def get_products(http, url, query, fields, before, after, limit, external):
    res = http.request(
        "GET",
        f"{url}/products",
        fields=drop_none_values(
            {
                "q": query,
                "fields": fields and ",".join(fields),
                "before": before,
                "after": after,
                "limit": limit,
                "external": external,
            }
        ),
    )

    data = json.loads(res.data.decode("utf-8"))

    return data


def get_orgs(http, url, query, before, after, limit):
    res = http.request(
        "GET",
        f"{url}/orgs",
        fields=drop_none_values(
            {
                "q": query,
                "before": before,
                "after": after,
                "limit": limit,
            }
        ),
    )

    data = json.loads(res.data.decode("utf-8"))

    return data


class GraphAPI:
    """A client-side representation of the Cofactr graph API."""

    PROTOCOL: Protocol = "https"
    HOST = "graph.cofactr.com"

    def __init__(
        self, protocol: Optional[Protocol] = PROTOCOL, host: Optional[str] = HOST
    ):

        self.url = f"{protocol}://{host}"
        self.http = urllib3.PoolManager()

    def check_health(self):
        """Check the operational status of the service."""

        res = self.http.request("GET", self.url)

        return json.loads(res.data.decode("utf-8"))

    def get_products(
        self,
        query: Optional[str] = None,
        fields: Optional[List[str]] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
        batch_size: int = 10,
        external: Optional[bool] = True,
    ) -> Cursor:
        """Get products.

        Args:
            query: Search query.
            fields: Used to filter properties that the response should contain. A field can be a
                concrete property like "mpn" or an abstract group of properties like "assembly".
            before: Upper page boundry, expressed as a product ID.
            after: Lower page boundry, expressed as a product ID.
            limit: Restrict the results of the query to a particular number of documents.
            batch_size: The size of each batch of results requested.
            external: Whether to query external sources.
        """

        request = partial(
            get_products,
            http=self.http,
            url=self.url,
            query=query,
            fields=fields,
            external=external,
        )

        return Cursor(
            request=request,
            before=before,
            after=after,
            limit=limit,
            batch_size=batch_size,
        )

    def get_orgs(
        self,
        query: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
        batch_size: int = 10,
    ):
        """Get organizations.

        Args:
            query: Search query.
            before: Upper page boundry, expressed as a product ID.
            after: Lower page boundry, expressed as a product ID.
            limit: Restrict the results of the query to a particular number of documents.
            batch_size: The size of each batch of results requested.
        """

        request = partial(
            get_orgs,
            http=self.http,
            url=self.url,
            query=query,
        )

        return Cursor(
            request=request,
            before=before,
            after=after,
            limit=limit,
            batch_size=batch_size,
        )

    def get_product(
        self,
        id: str,
        fields: Optional[List[str]] = None,
        external: Optional[bool] = True,
    ):
        """Get product.

        Args:
            fields: Used to filter properties that the response should contain. A field can be a
                concrete property like "mpn" or an abstract group of properties like "assembly".
            external: Whether to query external sources in order to update information for the
                given product.
        """

        res = self.http.request(
            "GET",
            f"{self.url}/products/{id}",
            fields=drop_none_values(
                {
                    "fields": fields and ",".join(fields),
                    "external": external,
                }
            ),
        )

        return json.loads(res.data.decode("utf-8"))

    def get_org(self, id: str):
        """Get organization."""

        res = self.http.request("GET", f"{self.url}/orgs/{id}")

        return json.loads(res.data.decode("utf-8"))
