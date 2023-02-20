from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.get_production_solar_panels_response_200 import GetProductionSolarPanelsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    from_: Union[Unset, None, int] = 2,
) -> Dict[str, Any]:
    url = "{}/v1/production-solar-panels".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["from"] = from_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[GetProductionSolarPanelsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetProductionSolarPanelsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[GetProductionSolarPanelsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    from_: Union[Unset, None, int] = 2,
) -> Response[GetProductionSolarPanelsResponse200]:
    """Get production of solar panels

    Args:
        from_ (Union[Unset, None, int]):  Default: 2. Example: 2.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProductionSolarPanelsResponse200]
    """

    kwargs = _get_kwargs(
        client=client,
        from_=from_,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    from_: Union[Unset, None, int] = 2,
) -> Optional[GetProductionSolarPanelsResponse200]:
    """Get production of solar panels

    Args:
        from_ (Union[Unset, None, int]):  Default: 2. Example: 2.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProductionSolarPanelsResponse200]
    """

    return sync_detailed(
        client=client,
        from_=from_,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    from_: Union[Unset, None, int] = 2,
) -> Response[GetProductionSolarPanelsResponse200]:
    """Get production of solar panels

    Args:
        from_ (Union[Unset, None, int]):  Default: 2. Example: 2.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProductionSolarPanelsResponse200]
    """

    kwargs = _get_kwargs(
        client=client,
        from_=from_,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    from_: Union[Unset, None, int] = 2,
) -> Optional[GetProductionSolarPanelsResponse200]:
    """Get production of solar panels

    Args:
        from_ (Union[Unset, None, int]):  Default: 2. Example: 2.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProductionSolarPanelsResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            from_=from_,
        )
    ).parsed
