# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock
except ImportError:
    import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule


from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.aiplatform_v1beta1.services.index_endpoint_service import (
    IndexEndpointServiceAsyncClient,
)
from google.cloud.aiplatform_v1beta1.services.index_endpoint_service import (
    IndexEndpointServiceClient,
)
from google.cloud.aiplatform_v1beta1.services.index_endpoint_service import pagers
from google.cloud.aiplatform_v1beta1.services.index_endpoint_service import transports
from google.cloud.aiplatform_v1beta1.types import accelerator_type
from google.cloud.aiplatform_v1beta1.types import index_endpoint
from google.cloud.aiplatform_v1beta1.types import index_endpoint as gca_index_endpoint
from google.cloud.aiplatform_v1beta1.types import index_endpoint_service
from google.cloud.aiplatform_v1beta1.types import machine_resources
from google.cloud.aiplatform_v1beta1.types import operation as gca_operation
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert IndexEndpointServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        IndexEndpointServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        IndexEndpointServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        IndexEndpointServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        IndexEndpointServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        IndexEndpointServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (IndexEndpointServiceClient, "grpc"),
        (IndexEndpointServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_index_endpoint_service_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("aiplatform.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.IndexEndpointServiceGrpcTransport, "grpc"),
        (transports.IndexEndpointServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_index_endpoint_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (IndexEndpointServiceClient, "grpc"),
        (IndexEndpointServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_index_endpoint_service_client_from_service_account_file(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("aiplatform.googleapis.com:443")


def test_index_endpoint_service_client_get_transport_class():
    transport = IndexEndpointServiceClient.get_transport_class()
    available_transports = [
        transports.IndexEndpointServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = IndexEndpointServiceClient.get_transport_class("grpc")
    assert transport == transports.IndexEndpointServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            IndexEndpointServiceClient,
            transports.IndexEndpointServiceGrpcTransport,
            "grpc",
        ),
        (
            IndexEndpointServiceAsyncClient,
            transports.IndexEndpointServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    IndexEndpointServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(IndexEndpointServiceClient),
)
@mock.patch.object(
    IndexEndpointServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(IndexEndpointServiceAsyncClient),
)
def test_index_endpoint_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(IndexEndpointServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(IndexEndpointServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            IndexEndpointServiceClient,
            transports.IndexEndpointServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            IndexEndpointServiceAsyncClient,
            transports.IndexEndpointServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            IndexEndpointServiceClient,
            transports.IndexEndpointServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            IndexEndpointServiceAsyncClient,
            transports.IndexEndpointServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    IndexEndpointServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(IndexEndpointServiceClient),
)
@mock.patch.object(
    IndexEndpointServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(IndexEndpointServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_index_endpoint_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                )


@pytest.mark.parametrize(
    "client_class", [IndexEndpointServiceClient, IndexEndpointServiceAsyncClient]
)
@mock.patch.object(
    IndexEndpointServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(IndexEndpointServiceClient),
)
@mock.patch.object(
    IndexEndpointServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(IndexEndpointServiceAsyncClient),
)
def test_index_endpoint_service_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            IndexEndpointServiceClient,
            transports.IndexEndpointServiceGrpcTransport,
            "grpc",
        ),
        (
            IndexEndpointServiceAsyncClient,
            transports.IndexEndpointServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_index_endpoint_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            IndexEndpointServiceClient,
            transports.IndexEndpointServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            IndexEndpointServiceAsyncClient,
            transports.IndexEndpointServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_index_endpoint_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


def test_index_endpoint_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.aiplatform_v1beta1.services.index_endpoint_service.transports.IndexEndpointServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = IndexEndpointServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            IndexEndpointServiceClient,
            transports.IndexEndpointServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            IndexEndpointServiceAsyncClient,
            transports.IndexEndpointServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_index_endpoint_service_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "aiplatform.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="aiplatform.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        index_endpoint_service.CreateIndexEndpointRequest,
        dict,
    ],
)
def test_create_index_endpoint(request_type, transport: str = "grpc"):
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.CreateIndexEndpointRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_index_endpoint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_index_endpoint), "__call__"
    ) as call:
        client.create_index_endpoint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.CreateIndexEndpointRequest()


@pytest.mark.asyncio
async def test_create_index_endpoint_async(
    transport: str = "grpc_asyncio",
    request_type=index_endpoint_service.CreateIndexEndpointRequest,
):
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.CreateIndexEndpointRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_index_endpoint_async_from_dict():
    await test_create_index_endpoint_async(request_type=dict)


def test_create_index_endpoint_field_headers():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.CreateIndexEndpointRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_index_endpoint), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_index_endpoint_field_headers_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.CreateIndexEndpointRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_index_endpoint), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_index_endpoint_flattened():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_index_endpoint(
            parent="parent_value",
            index_endpoint=gca_index_endpoint.IndexEndpoint(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].index_endpoint
        mock_val = gca_index_endpoint.IndexEndpoint(name="name_value")
        assert arg == mock_val


def test_create_index_endpoint_flattened_error():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_index_endpoint(
            index_endpoint_service.CreateIndexEndpointRequest(),
            parent="parent_value",
            index_endpoint=gca_index_endpoint.IndexEndpoint(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_index_endpoint_flattened_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_index_endpoint(
            parent="parent_value",
            index_endpoint=gca_index_endpoint.IndexEndpoint(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].index_endpoint
        mock_val = gca_index_endpoint.IndexEndpoint(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_index_endpoint_flattened_error_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_index_endpoint(
            index_endpoint_service.CreateIndexEndpointRequest(),
            parent="parent_value",
            index_endpoint=gca_index_endpoint.IndexEndpoint(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        index_endpoint_service.GetIndexEndpointRequest,
        dict,
    ],
)
def test_get_index_endpoint(request_type, transport: str = "grpc"):
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = index_endpoint.IndexEndpoint(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
            network="network_value",
            enable_private_service_connect=True,
        )
        response = client.get_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.GetIndexEndpointRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, index_endpoint.IndexEndpoint)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.network == "network_value"
    assert response.enable_private_service_connect is True


def test_get_index_endpoint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_index_endpoint), "__call__"
    ) as call:
        client.get_index_endpoint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.GetIndexEndpointRequest()


@pytest.mark.asyncio
async def test_get_index_endpoint_async(
    transport: str = "grpc_asyncio",
    request_type=index_endpoint_service.GetIndexEndpointRequest,
):
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            index_endpoint.IndexEndpoint(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                etag="etag_value",
                network="network_value",
                enable_private_service_connect=True,
            )
        )
        response = await client.get_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.GetIndexEndpointRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, index_endpoint.IndexEndpoint)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.network == "network_value"
    assert response.enable_private_service_connect is True


@pytest.mark.asyncio
async def test_get_index_endpoint_async_from_dict():
    await test_get_index_endpoint_async(request_type=dict)


def test_get_index_endpoint_field_headers():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.GetIndexEndpointRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_index_endpoint), "__call__"
    ) as call:
        call.return_value = index_endpoint.IndexEndpoint()
        client.get_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_index_endpoint_field_headers_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.GetIndexEndpointRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_index_endpoint), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            index_endpoint.IndexEndpoint()
        )
        await client.get_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_index_endpoint_flattened():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = index_endpoint.IndexEndpoint()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_index_endpoint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_index_endpoint_flattened_error():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_index_endpoint(
            index_endpoint_service.GetIndexEndpointRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_index_endpoint_flattened_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = index_endpoint.IndexEndpoint()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            index_endpoint.IndexEndpoint()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_index_endpoint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_index_endpoint_flattened_error_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_index_endpoint(
            index_endpoint_service.GetIndexEndpointRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        index_endpoint_service.ListIndexEndpointsRequest,
        dict,
    ],
)
def test_list_index_endpoints(request_type, transport: str = "grpc"):
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_index_endpoints), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = index_endpoint_service.ListIndexEndpointsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_index_endpoints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.ListIndexEndpointsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListIndexEndpointsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_index_endpoints_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_index_endpoints), "__call__"
    ) as call:
        client.list_index_endpoints()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.ListIndexEndpointsRequest()


@pytest.mark.asyncio
async def test_list_index_endpoints_async(
    transport: str = "grpc_asyncio",
    request_type=index_endpoint_service.ListIndexEndpointsRequest,
):
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_index_endpoints), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            index_endpoint_service.ListIndexEndpointsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_index_endpoints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.ListIndexEndpointsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListIndexEndpointsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_index_endpoints_async_from_dict():
    await test_list_index_endpoints_async(request_type=dict)


def test_list_index_endpoints_field_headers():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.ListIndexEndpointsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_index_endpoints), "__call__"
    ) as call:
        call.return_value = index_endpoint_service.ListIndexEndpointsResponse()
        client.list_index_endpoints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_index_endpoints_field_headers_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.ListIndexEndpointsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_index_endpoints), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            index_endpoint_service.ListIndexEndpointsResponse()
        )
        await client.list_index_endpoints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_index_endpoints_flattened():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_index_endpoints), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = index_endpoint_service.ListIndexEndpointsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_index_endpoints(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_index_endpoints_flattened_error():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_index_endpoints(
            index_endpoint_service.ListIndexEndpointsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_index_endpoints_flattened_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_index_endpoints), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = index_endpoint_service.ListIndexEndpointsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            index_endpoint_service.ListIndexEndpointsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_index_endpoints(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_index_endpoints_flattened_error_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_index_endpoints(
            index_endpoint_service.ListIndexEndpointsRequest(),
            parent="parent_value",
        )


def test_list_index_endpoints_pager(transport_name: str = "grpc"):
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_index_endpoints), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[
                    index_endpoint.IndexEndpoint(),
                    index_endpoint.IndexEndpoint(),
                    index_endpoint.IndexEndpoint(),
                ],
                next_page_token="abc",
            ),
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[],
                next_page_token="def",
            ),
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[
                    index_endpoint.IndexEndpoint(),
                ],
                next_page_token="ghi",
            ),
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[
                    index_endpoint.IndexEndpoint(),
                    index_endpoint.IndexEndpoint(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_index_endpoints(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, index_endpoint.IndexEndpoint) for i in results)


def test_list_index_endpoints_pages(transport_name: str = "grpc"):
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_index_endpoints), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[
                    index_endpoint.IndexEndpoint(),
                    index_endpoint.IndexEndpoint(),
                    index_endpoint.IndexEndpoint(),
                ],
                next_page_token="abc",
            ),
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[],
                next_page_token="def",
            ),
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[
                    index_endpoint.IndexEndpoint(),
                ],
                next_page_token="ghi",
            ),
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[
                    index_endpoint.IndexEndpoint(),
                    index_endpoint.IndexEndpoint(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_index_endpoints(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_index_endpoints_async_pager():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_index_endpoints),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[
                    index_endpoint.IndexEndpoint(),
                    index_endpoint.IndexEndpoint(),
                    index_endpoint.IndexEndpoint(),
                ],
                next_page_token="abc",
            ),
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[],
                next_page_token="def",
            ),
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[
                    index_endpoint.IndexEndpoint(),
                ],
                next_page_token="ghi",
            ),
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[
                    index_endpoint.IndexEndpoint(),
                    index_endpoint.IndexEndpoint(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_index_endpoints(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, index_endpoint.IndexEndpoint) for i in responses)


@pytest.mark.asyncio
async def test_list_index_endpoints_async_pages():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_index_endpoints),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[
                    index_endpoint.IndexEndpoint(),
                    index_endpoint.IndexEndpoint(),
                    index_endpoint.IndexEndpoint(),
                ],
                next_page_token="abc",
            ),
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[],
                next_page_token="def",
            ),
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[
                    index_endpoint.IndexEndpoint(),
                ],
                next_page_token="ghi",
            ),
            index_endpoint_service.ListIndexEndpointsResponse(
                index_endpoints=[
                    index_endpoint.IndexEndpoint(),
                    index_endpoint.IndexEndpoint(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_index_endpoints(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        index_endpoint_service.UpdateIndexEndpointRequest,
        dict,
    ],
)
def test_update_index_endpoint(request_type, transport: str = "grpc"):
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_index_endpoint.IndexEndpoint(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
            network="network_value",
            enable_private_service_connect=True,
        )
        response = client.update_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.UpdateIndexEndpointRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_index_endpoint.IndexEndpoint)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.network == "network_value"
    assert response.enable_private_service_connect is True


def test_update_index_endpoint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_index_endpoint), "__call__"
    ) as call:
        client.update_index_endpoint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.UpdateIndexEndpointRequest()


@pytest.mark.asyncio
async def test_update_index_endpoint_async(
    transport: str = "grpc_asyncio",
    request_type=index_endpoint_service.UpdateIndexEndpointRequest,
):
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_index_endpoint.IndexEndpoint(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                etag="etag_value",
                network="network_value",
                enable_private_service_connect=True,
            )
        )
        response = await client.update_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.UpdateIndexEndpointRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_index_endpoint.IndexEndpoint)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.network == "network_value"
    assert response.enable_private_service_connect is True


@pytest.mark.asyncio
async def test_update_index_endpoint_async_from_dict():
    await test_update_index_endpoint_async(request_type=dict)


def test_update_index_endpoint_field_headers():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.UpdateIndexEndpointRequest()

    request.index_endpoint.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_index_endpoint), "__call__"
    ) as call:
        call.return_value = gca_index_endpoint.IndexEndpoint()
        client.update_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "index_endpoint.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_index_endpoint_field_headers_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.UpdateIndexEndpointRequest()

    request.index_endpoint.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_index_endpoint), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_index_endpoint.IndexEndpoint()
        )
        await client.update_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "index_endpoint.name=name_value",
    ) in kw["metadata"]


def test_update_index_endpoint_flattened():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_index_endpoint.IndexEndpoint()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_index_endpoint(
            index_endpoint=gca_index_endpoint.IndexEndpoint(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].index_endpoint
        mock_val = gca_index_endpoint.IndexEndpoint(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_index_endpoint_flattened_error():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_index_endpoint(
            index_endpoint_service.UpdateIndexEndpointRequest(),
            index_endpoint=gca_index_endpoint.IndexEndpoint(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_index_endpoint_flattened_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_index_endpoint.IndexEndpoint()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_index_endpoint.IndexEndpoint()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_index_endpoint(
            index_endpoint=gca_index_endpoint.IndexEndpoint(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].index_endpoint
        mock_val = gca_index_endpoint.IndexEndpoint(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_index_endpoint_flattened_error_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_index_endpoint(
            index_endpoint_service.UpdateIndexEndpointRequest(),
            index_endpoint=gca_index_endpoint.IndexEndpoint(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        index_endpoint_service.DeleteIndexEndpointRequest,
        dict,
    ],
)
def test_delete_index_endpoint(request_type, transport: str = "grpc"):
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.DeleteIndexEndpointRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_index_endpoint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_index_endpoint), "__call__"
    ) as call:
        client.delete_index_endpoint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.DeleteIndexEndpointRequest()


@pytest.mark.asyncio
async def test_delete_index_endpoint_async(
    transport: str = "grpc_asyncio",
    request_type=index_endpoint_service.DeleteIndexEndpointRequest,
):
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.DeleteIndexEndpointRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_index_endpoint_async_from_dict():
    await test_delete_index_endpoint_async(request_type=dict)


def test_delete_index_endpoint_field_headers():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.DeleteIndexEndpointRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_index_endpoint), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_index_endpoint_field_headers_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.DeleteIndexEndpointRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_index_endpoint), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_index_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_index_endpoint_flattened():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_index_endpoint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_index_endpoint_flattened_error():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_index_endpoint(
            index_endpoint_service.DeleteIndexEndpointRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_index_endpoint_flattened_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_index_endpoint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_index_endpoint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_index_endpoint_flattened_error_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_index_endpoint(
            index_endpoint_service.DeleteIndexEndpointRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        index_endpoint_service.DeployIndexRequest,
        dict,
    ],
)
def test_deploy_index(request_type, transport: str = "grpc"):
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.deploy_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.DeployIndexRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_deploy_index_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_index), "__call__") as call:
        client.deploy_index()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.DeployIndexRequest()


@pytest.mark.asyncio
async def test_deploy_index_async(
    transport: str = "grpc_asyncio",
    request_type=index_endpoint_service.DeployIndexRequest,
):
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.deploy_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.DeployIndexRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_deploy_index_async_from_dict():
    await test_deploy_index_async(request_type=dict)


def test_deploy_index_field_headers():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.DeployIndexRequest()

    request.index_endpoint = "index_endpoint_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_index), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.deploy_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "index_endpoint=index_endpoint_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_deploy_index_field_headers_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.DeployIndexRequest()

    request.index_endpoint = "index_endpoint_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_index), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.deploy_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "index_endpoint=index_endpoint_value",
    ) in kw["metadata"]


def test_deploy_index_flattened():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.deploy_index(
            index_endpoint="index_endpoint_value",
            deployed_index=gca_index_endpoint.DeployedIndex(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].index_endpoint
        mock_val = "index_endpoint_value"
        assert arg == mock_val
        arg = args[0].deployed_index
        mock_val = gca_index_endpoint.DeployedIndex(id="id_value")
        assert arg == mock_val


def test_deploy_index_flattened_error():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.deploy_index(
            index_endpoint_service.DeployIndexRequest(),
            index_endpoint="index_endpoint_value",
            deployed_index=gca_index_endpoint.DeployedIndex(id="id_value"),
        )


@pytest.mark.asyncio
async def test_deploy_index_flattened_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.deploy_index(
            index_endpoint="index_endpoint_value",
            deployed_index=gca_index_endpoint.DeployedIndex(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].index_endpoint
        mock_val = "index_endpoint_value"
        assert arg == mock_val
        arg = args[0].deployed_index
        mock_val = gca_index_endpoint.DeployedIndex(id="id_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_deploy_index_flattened_error_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.deploy_index(
            index_endpoint_service.DeployIndexRequest(),
            index_endpoint="index_endpoint_value",
            deployed_index=gca_index_endpoint.DeployedIndex(id="id_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        index_endpoint_service.UndeployIndexRequest,
        dict,
    ],
)
def test_undeploy_index(request_type, transport: str = "grpc"):
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.undeploy_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.UndeployIndexRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_undeploy_index_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_index), "__call__") as call:
        client.undeploy_index()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.UndeployIndexRequest()


@pytest.mark.asyncio
async def test_undeploy_index_async(
    transport: str = "grpc_asyncio",
    request_type=index_endpoint_service.UndeployIndexRequest,
):
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.undeploy_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.UndeployIndexRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_undeploy_index_async_from_dict():
    await test_undeploy_index_async(request_type=dict)


def test_undeploy_index_field_headers():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.UndeployIndexRequest()

    request.index_endpoint = "index_endpoint_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_index), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.undeploy_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "index_endpoint=index_endpoint_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_undeploy_index_field_headers_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.UndeployIndexRequest()

    request.index_endpoint = "index_endpoint_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_index), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.undeploy_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "index_endpoint=index_endpoint_value",
    ) in kw["metadata"]


def test_undeploy_index_flattened():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.undeploy_index(
            index_endpoint="index_endpoint_value",
            deployed_index_id="deployed_index_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].index_endpoint
        mock_val = "index_endpoint_value"
        assert arg == mock_val
        arg = args[0].deployed_index_id
        mock_val = "deployed_index_id_value"
        assert arg == mock_val


def test_undeploy_index_flattened_error():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undeploy_index(
            index_endpoint_service.UndeployIndexRequest(),
            index_endpoint="index_endpoint_value",
            deployed_index_id="deployed_index_id_value",
        )


@pytest.mark.asyncio
async def test_undeploy_index_flattened_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_index), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.undeploy_index(
            index_endpoint="index_endpoint_value",
            deployed_index_id="deployed_index_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].index_endpoint
        mock_val = "index_endpoint_value"
        assert arg == mock_val
        arg = args[0].deployed_index_id
        mock_val = "deployed_index_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_undeploy_index_flattened_error_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.undeploy_index(
            index_endpoint_service.UndeployIndexRequest(),
            index_endpoint="index_endpoint_value",
            deployed_index_id="deployed_index_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        index_endpoint_service.MutateDeployedIndexRequest,
        dict,
    ],
)
def test_mutate_deployed_index(request_type, transport: str = "grpc"):
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mutate_deployed_index), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.mutate_deployed_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.MutateDeployedIndexRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_mutate_deployed_index_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mutate_deployed_index), "__call__"
    ) as call:
        client.mutate_deployed_index()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.MutateDeployedIndexRequest()


@pytest.mark.asyncio
async def test_mutate_deployed_index_async(
    transport: str = "grpc_asyncio",
    request_type=index_endpoint_service.MutateDeployedIndexRequest,
):
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mutate_deployed_index), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.mutate_deployed_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == index_endpoint_service.MutateDeployedIndexRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_mutate_deployed_index_async_from_dict():
    await test_mutate_deployed_index_async(request_type=dict)


def test_mutate_deployed_index_field_headers():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.MutateDeployedIndexRequest()

    request.index_endpoint = "index_endpoint_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mutate_deployed_index), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.mutate_deployed_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "index_endpoint=index_endpoint_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_mutate_deployed_index_field_headers_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = index_endpoint_service.MutateDeployedIndexRequest()

    request.index_endpoint = "index_endpoint_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mutate_deployed_index), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.mutate_deployed_index(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "index_endpoint=index_endpoint_value",
    ) in kw["metadata"]


def test_mutate_deployed_index_flattened():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mutate_deployed_index), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.mutate_deployed_index(
            index_endpoint="index_endpoint_value",
            deployed_index=gca_index_endpoint.DeployedIndex(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].index_endpoint
        mock_val = "index_endpoint_value"
        assert arg == mock_val
        arg = args[0].deployed_index
        mock_val = gca_index_endpoint.DeployedIndex(id="id_value")
        assert arg == mock_val


def test_mutate_deployed_index_flattened_error():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.mutate_deployed_index(
            index_endpoint_service.MutateDeployedIndexRequest(),
            index_endpoint="index_endpoint_value",
            deployed_index=gca_index_endpoint.DeployedIndex(id="id_value"),
        )


@pytest.mark.asyncio
async def test_mutate_deployed_index_flattened_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mutate_deployed_index), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.mutate_deployed_index(
            index_endpoint="index_endpoint_value",
            deployed_index=gca_index_endpoint.DeployedIndex(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].index_endpoint
        mock_val = "index_endpoint_value"
        assert arg == mock_val
        arg = args[0].deployed_index
        mock_val = gca_index_endpoint.DeployedIndex(id="id_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_mutate_deployed_index_flattened_error_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.mutate_deployed_index(
            index_endpoint_service.MutateDeployedIndexRequest(),
            index_endpoint="index_endpoint_value",
            deployed_index=gca_index_endpoint.DeployedIndex(id="id_value"),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.IndexEndpointServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = IndexEndpointServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.IndexEndpointServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = IndexEndpointServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.IndexEndpointServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = IndexEndpointServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = IndexEndpointServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.IndexEndpointServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = IndexEndpointServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.IndexEndpointServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = IndexEndpointServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.IndexEndpointServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.IndexEndpointServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.IndexEndpointServiceGrpcTransport,
        transports.IndexEndpointServiceGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
    ],
)
def test_transport_kind(transport_name):
    transport = IndexEndpointServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.IndexEndpointServiceGrpcTransport,
    )


def test_index_endpoint_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.IndexEndpointServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_index_endpoint_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.aiplatform_v1beta1.services.index_endpoint_service.transports.IndexEndpointServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.IndexEndpointServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_index_endpoint",
        "get_index_endpoint",
        "list_index_endpoints",
        "update_index_endpoint",
        "delete_index_endpoint",
        "deploy_index",
        "undeploy_index",
        "mutate_deployed_index",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_index_endpoint_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.aiplatform_v1beta1.services.index_endpoint_service.transports.IndexEndpointServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.IndexEndpointServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_index_endpoint_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.aiplatform_v1beta1.services.index_endpoint_service.transports.IndexEndpointServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.IndexEndpointServiceTransport()
        adc.assert_called_once()


def test_index_endpoint_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        IndexEndpointServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.IndexEndpointServiceGrpcTransport,
        transports.IndexEndpointServiceGrpcAsyncIOTransport,
    ],
)
def test_index_endpoint_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.IndexEndpointServiceGrpcTransport, grpc_helpers),
        (transports.IndexEndpointServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_index_endpoint_service_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "aiplatform.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="aiplatform.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.IndexEndpointServiceGrpcTransport,
        transports.IndexEndpointServiceGrpcAsyncIOTransport,
    ],
)
def test_index_endpoint_service_grpc_transport_client_cert_source_for_mtls(
    transport_class,
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_index_endpoint_service_host_no_port(transport_name):
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="aiplatform.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("aiplatform.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_index_endpoint_service_host_with_port(transport_name):
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="aiplatform.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("aiplatform.googleapis.com:8000")


def test_index_endpoint_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.IndexEndpointServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_index_endpoint_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.IndexEndpointServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.IndexEndpointServiceGrpcTransport,
        transports.IndexEndpointServiceGrpcAsyncIOTransport,
    ],
)
def test_index_endpoint_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.IndexEndpointServiceGrpcTransport,
        transports.IndexEndpointServiceGrpcAsyncIOTransport,
    ],
)
def test_index_endpoint_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_index_endpoint_service_grpc_lro_client():
    client = IndexEndpointServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_index_endpoint_service_grpc_lro_async_client():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_index_path():
    project = "squid"
    location = "clam"
    index = "whelk"
    expected = "projects/{project}/locations/{location}/indexes/{index}".format(
        project=project,
        location=location,
        index=index,
    )
    actual = IndexEndpointServiceClient.index_path(project, location, index)
    assert expected == actual


def test_parse_index_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "index": "nudibranch",
    }
    path = IndexEndpointServiceClient.index_path(**expected)

    # Check that the path construction is reversible.
    actual = IndexEndpointServiceClient.parse_index_path(path)
    assert expected == actual


def test_index_endpoint_path():
    project = "cuttlefish"
    location = "mussel"
    index_endpoint = "winkle"
    expected = "projects/{project}/locations/{location}/indexEndpoints/{index_endpoint}".format(
        project=project,
        location=location,
        index_endpoint=index_endpoint,
    )
    actual = IndexEndpointServiceClient.index_endpoint_path(
        project, location, index_endpoint
    )
    assert expected == actual


def test_parse_index_endpoint_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "index_endpoint": "abalone",
    }
    path = IndexEndpointServiceClient.index_endpoint_path(**expected)

    # Check that the path construction is reversible.
    actual = IndexEndpointServiceClient.parse_index_endpoint_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = IndexEndpointServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = IndexEndpointServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = IndexEndpointServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = IndexEndpointServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = IndexEndpointServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = IndexEndpointServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = IndexEndpointServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = IndexEndpointServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = IndexEndpointServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = IndexEndpointServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = IndexEndpointServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = IndexEndpointServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = IndexEndpointServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = IndexEndpointServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = IndexEndpointServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.IndexEndpointServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = IndexEndpointServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.IndexEndpointServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = IndexEndpointServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = IndexEndpointServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = IndexEndpointServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = IndexEndpointServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (IndexEndpointServiceClient, transports.IndexEndpointServiceGrpcTransport),
        (
            IndexEndpointServiceAsyncClient,
            transports.IndexEndpointServiceGrpcAsyncIOTransport,
        ),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )
