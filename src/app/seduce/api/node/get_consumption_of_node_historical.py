from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.get_consumption_of_node_historical_response_200 import GetConsumptionOfNodeHistoricalResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    node_id: str,
    *,
    client: Client,
    step: Union[Unset, None, float] = 500.0,
    range_: Union[Unset, None, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v1/{nodeID}/consumption".format(client.base_url, nodeID=node_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["step"] = step

    json_range_: Union[Unset, None, List[str]] = UNSET
    if not isinstance(range_, Unset):
        if range_ is None:
            json_range_ = None
        else:
            json_range_ = range_

    params["range"] = json_range_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, GetConsumptionOfNodeHistoricalResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetConsumptionOfNodeHistoricalResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, GetConsumptionOfNodeHistoricalResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    node_id: str,
    *,
    client: Client,
    step: Union[Unset, None, float] = 500.0,
    range_: Union[Unset, None, List[str]] = UNSET,
) -> Response[Union[Any, GetConsumptionOfNodeHistoricalResponse200]]:
    """Get consumption of node with historical data

     historical data

    Args:
        node_id (str):  Example: ecotype-25_pdu-Z1.2.
        step (Union[Unset, None, float]):  Default: 500.0. Example: 500.
        range_ (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetConsumptionOfNodeHistoricalResponse200]]
    """

    kwargs = _get_kwargs(
        node_id=node_id,
        client=client,
        step=step,
        range_=range_,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    node_id: str,
    *,
    client: Client,
    step: Union[Unset, None, float] = 500.0,
    range_: Union[Unset, None, List[str]] = UNSET,
) -> Optional[Union[Any, GetConsumptionOfNodeHistoricalResponse200]]:
    """Get consumption of node with historical data

     historical data

    Args:
        node_id (str):  Example: ecotype-25_pdu-Z1.2.
        step (Union[Unset, None, float]):  Default: 500.0. Example: 500.
        range_ (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetConsumptionOfNodeHistoricalResponse200]]
    """

    return sync_detailed(
        node_id=node_id,
        client=client,
        step=step,
        range_=range_,
    ).parsed


async def asyncio_detailed(
    node_id: str,
    *,
    client: Client,
    step: Union[Unset, None, float] = 500.0,
    range_: Union[Unset, None, List[str]] = UNSET,
) -> Response[Union[Any, GetConsumptionOfNodeHistoricalResponse200]]:
    """Get consumption of node with historical data

     historical data

    Args:
        node_id (str):  Example: ecotype-25_pdu-Z1.2.
        step (Union[Unset, None, float]):  Default: 500.0. Example: 500.
        range_ (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetConsumptionOfNodeHistoricalResponse200]]
    """

    kwargs = _get_kwargs(
        node_id=node_id,
        client=client,
        step=step,
        range_=range_,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    node_id: str,
    *,
    client: Client,
    step: Union[Unset, None, float] = 500.0,
    range_: Union[Unset, None, List[str]] = UNSET,
) -> Optional[Union[Any, GetConsumptionOfNodeHistoricalResponse200]]:
    """Get consumption of node with historical data

     historical data

    Args:
        node_id (str):  Example: ecotype-25_pdu-Z1.2.
        step (Union[Unset, None, float]):  Default: 500.0. Example: 500.
        range_ (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetConsumptionOfNodeHistoricalResponse200]]
    """

    return (
        await asyncio_detailed(
            node_id=node_id,
            client=client,
            step=step,
            range_=range_,
        )
    ).parsed
