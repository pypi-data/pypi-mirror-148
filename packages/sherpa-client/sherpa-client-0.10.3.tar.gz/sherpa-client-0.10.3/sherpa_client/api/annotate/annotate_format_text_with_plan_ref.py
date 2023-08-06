from io import BytesIO
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    project_name: str,
    plan_name: str,
    *,
    client: Client,
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/plans/{planName}/_annotate_format_text".format(
        client.base_url, projectName=project_name, planName=plan_name
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "inlineLabels": inline_labels,
        "inlineLabelIds": inline_label_ids,
        "inlineText": inline_text,
        "debug": debug,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[File]:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.json()))

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[File]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    project_name: str,
    plan_name: str,
    *,
    client: Client,
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
) -> Response[File]:
    kwargs = _get_kwargs(
        project_name=project_name,
        plan_name=plan_name,
        client=client,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
    )

    response = httpx.post(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    project_name: str,
    plan_name: str,
    *,
    client: Client,
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
) -> Optional[File]:
    """ """

    return sync_detailed(
        project_name=project_name,
        plan_name=plan_name,
        client=client,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    plan_name: str,
    *,
    client: Client,
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
) -> Response[File]:
    kwargs = _get_kwargs(
        project_name=project_name,
        plan_name=plan_name,
        client=client,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    project_name: str,
    plan_name: str,
    *,
    client: Client,
    inline_labels: Union[Unset, None, bool] = True,
    inline_label_ids: Union[Unset, None, bool] = True,
    inline_text: Union[Unset, None, bool] = True,
    debug: Union[Unset, None, bool] = False,
) -> Optional[File]:
    """ """

    return (
        await asyncio_detailed(
            project_name=project_name,
            plan_name=plan_name,
            client=client,
            inline_labels=inline_labels,
            inline_label_ids=inline_label_ids,
            inline_text=inline_text,
            debug=debug,
        )
    ).parsed
