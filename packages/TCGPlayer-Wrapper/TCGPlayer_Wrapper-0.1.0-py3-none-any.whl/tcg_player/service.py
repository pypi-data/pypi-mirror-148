import logging
import platform
from json import JSONDecodeError
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from ratelimit import limits, sleep_and_retry
from requests import get, post
from requests.exceptions import ConnectionError, HTTPError

from tcg_player import __version__
from tcg_player.schemas.category import Category
from tcg_player.schemas.condition import Condition
from tcg_player.schemas.group import Group
from tcg_player.schemas.language import Language
from tcg_player.schemas.price import Price
from tcg_player.schemas.printing import Printing
from tcg_player.schemas.product import Product
from tcg_player.schemas.rarity import Rarity
from tcg_player.sqlite_cache import SQLiteCache

LOGGER = logging.getLogger(__name__)
MINUTE = 60


class TCGPlayer:
    API_URL = "https://api.tcgplayer.com/v1.39.0"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        access_token: Optional[str] = None,
        cache: Optional[SQLiteCache] = None,
    ):
        self.headers = {
            "Accept": "application/json",
            "User-Agent": f"TCG-Player-Wrapper/{__version__}"
            f"/{platform.system()}: {platform.release()}",
        }
        self.cache = cache
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

        if self.access_token:
            self.headers["Authorization"] = f"Bearer {self.access_token}"

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def _perform_get_request(self, url: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        if params is None:
            params = {}

        try:
            response = get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except ConnectionError as ce:
            LOGGER.error(f"Unable to connect to `{url}`: {ce}")
        except HTTPError as he:
            LOGGER.error(he.response.text)
        except JSONDecodeError as de:
            LOGGER.error(f"Invalid response from `{url}`: {de}")

        return {}

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def _post_request(
        self, endpoint: str, params: Dict[str, str] = None, body: Dict[str, str] = None
    ) -> Dict[str, Any]:
        if params is None:
            params = {}
        if body is None:
            body = {}

        url = self.API_URL + endpoint

        content = {}
        try:
            response = post(url, params=params, data=body, headers=self.headers)
            response.raise_for_status()
            content = response.json()
            if "error_description" in content and content["error_description"]:
                LOGGER.error(content["error_description"])
                content = {}
        except ConnectionError as ce:
            LOGGER.error(f"Unable to connect to `{url}`: {ce}")
        except HTTPError as he:
            LOGGER.error(he.response.text)
        except JSONDecodeError as de:
            LOGGER.error(f"Invalid response from `{url}`: {de}")

        return content

    def _get_request(
        self,
        endpoint: str,
        params: Dict[str, str] = None,
        skip_cache: bool = False,
    ) -> Dict[str, Any]:
        cache_params = f"?{urlencode(params)}" if params else ""

        url = self.API_URL + endpoint
        cache_key = f"{url}{cache_params}"

        if self.cache and not skip_cache:
            if cached_response := self.cache.select(cache_key):
                return cached_response

        response = self._perform_get_request(url=url, params=params)
        if not response:
            return {}
        if "error_description" in response and response["error_description"]:
            LOGGER.error(response["error_description"])
            return {}

        if self.cache and not skip_cache:
            self.cache.insert(cache_key, response)

        return response

    def generate_token(self) -> str:
        LOGGER.info("Generating new Auth Token")
        if "Authorization" in self.headers:
            del self.headers["Authorization"]
        token = self._post_request(
            endpoint="/token",
            body={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )["access_token"]
        self.access_token = token
        self.headers["Authorization"] = f"Bearer {token}"
        return token

    def authorization_check(self) -> bool:
        if self._get_request(endpoint="/catalog/categories", skip_cache=True):
            return True
        self.access_token = None
        if "Authorization" in self.headers:
            del self.headers["Authorization"]
        return False

    def list_categories(self) -> List[Category]:
        results = self._retrieve_all_results(endpoint="/catalog/categories")
        if results:
            return [Category.from_dict(x) for x in results]
        return []

    def category(self, category_id: int) -> Optional[Category]:
        response = self._get_request(endpoint=f"/catalog/categories/{category_id}")
        if response:
            return Category.from_dict(response["results"][0])
        return None

    def list_category_groups(self, category_id: int) -> List[Group]:
        results = self._retrieve_all_results(endpoint=f"/catalog/categories/{category_id}/groups")
        if results:
            return [Group.from_dict(x) for x in results]
        return []

    def list_category_rarities(self, category_id: int) -> List[Rarity]:
        results = self._get_request(endpoint=f"/catalog/categories/{category_id}/rarities")
        if results:
            return [Rarity.from_dict(x) for x in results["results"]]
        return []

    def list_category_printings(self, category_id: int) -> List[Printing]:
        results = self._get_request(endpoint=f"/catalog/categories/{category_id}/printings")
        if results:
            return [Printing.from_dict(x) for x in results["results"]]
        return []

    def list_category_conditions(self, category_id: int) -> List[Condition]:
        results = self._get_request(endpoint=f"/catalog/categories/{category_id}/conditions")
        if results:
            return [Condition.from_dict(x) for x in results["results"]]
        return []

    def list_category_languages(self, category_id: int) -> List[Language]:
        results = self._get_request(endpoint=f"/catalog/categories/{category_id}/languages")
        if results:
            return [Language.from_dict(x) for x in results["results"]]
        return []

    def group(self, group_id: int) -> Optional[Group]:
        response = self._get_request(endpoint=f"/catalog/groups/{group_id}")
        if response:
            return Group.from_dict(response["results"][0])
        return None

    def list_group_products(self, category_id: int, group_id: int) -> List[Product]:
        results = self._get_request(
            endpoint="/catalog/products",
            params={"categoryId": category_id, "groupId": group_id, "productTypes": "Cards"},
        )
        if results:
            return [Product.from_dict(x) for x in results["results"]]
        return []

    def product(self, product_id: int) -> Optional[Product]:
        response = self._get_request(endpoint=f"/catalog/products/{product_id}")
        if response:
            return Product.from_dict(response["results"][0])
        return None

    def list_group_prices(self, group_id: int) -> List[Price]:
        results = self._get_request(endpoint=f"/pricing/group/{group_id}")
        if results:
            return [Price.from_dict(x) for x in results["results"]]
        return []

    def product_prices(self, product_id: int) -> Optional[Price]:
        response = self._get_request(endpoint=f"/pricing/product/{product_id}")
        if response:
            return Price.from_dict(response["results"][0])
        return None

    def _retrieve_all_results(self, endpoint: str, params: Dict[str, str] = None) -> List[Any]:
        if params is None:
            params = {}
        params["limit"] = 100
        params["offset"] = 0

        response = self._get_request(endpoint, params=params)
        results = response["results"]
        while response["totalItems"] > len(results):
            params["offset"] = len(results)
            response = self._get_request(endpoint, params=params)
            results.extend(response["results"])
        return results
