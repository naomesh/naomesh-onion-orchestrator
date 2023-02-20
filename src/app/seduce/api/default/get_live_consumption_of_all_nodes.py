from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.get_live_consumption_of_all_nodes_response_200 import GetLiveConsumptionOfAllNodesResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    nodes: Union[Unset, None, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v1/live-consumption".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_nodes: Union[Unset, None, List[str]] = UNSET
    if not isinstance(nodes, Unset):
        if nodes is None:
            json_nodes = None
        else:
            json_nodes = nodes

    params["nodes"] = json_nodes

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
) -> Optional[Union[Any, GetLiveConsumptionOfAllNodesResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetLiveConsumptionOfAllNodesResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, GetLiveConsumptionOfAllNodesResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    nodes: Union[Unset, None, List[str]] = UNSET,
) -> Response[Union[Any, GetLiveConsumptionOfAllNodesResponse200]]:
    """Get live consumption of all nodes in watt specified by query parameter

    Args:
        nodes (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetLiveConsumptionOfAllNodesResponse200]]
    """

    kwargs = _get_kwargs(
        client=client,
        nodes=nodes,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    nodes: Union[Unset, None, List[str]] = UNSET,
) -> Optional[Union[Any, GetLiveConsumptionOfAllNodesResponse200]]:
    """Get live consumption of all nodes in watt specified by query parameter

    Args:
        nodes (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetLiveConsumptionOfAllNodesResponse200]]
    """

    return sync_detailed(
        client=client,
        nodes=nodes,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    nodes: Union[Unset, None, List[str]] = UNSET,
) -> Response[Union[Any, GetLiveConsumptionOfAllNodesResponse200]]:
    """Get live consumption of all nodes in watt specified by query parameter

    Args:
        nodes (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetLiveConsumptionOfAllNodesResponse200]]
    """

    kwargs = _get_kwargs(
        client=client,
        nodes=nodes,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    nodes: Union[Unset, None, List[str]] = UNSET,
) -> Optional[Union[Any, GetLiveConsumptionOfAllNodesResponse200]]:
    """Get live consumption of all nodes in watt specified by query parameter

    Args:
        nodes (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetLiveConsumptionOfAllNodesResponse200]]
    """

    return (
        await asyncio_detailed(
            client=client,
            nodes=nodes,
        )
    ).parsed
