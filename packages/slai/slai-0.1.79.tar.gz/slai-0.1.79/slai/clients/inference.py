import requests
import copy

from functools import lru_cache
from requests.auth import HTTPBasicAuth
from importlib import import_module
from slai.modules.parameters import from_config
from slai.config import get_api_base_urls
from slai.modules.runtime import detect_credentials
from slai.clients.model import get_model_client
from slai.types import ModelTypes, InvalidPayloadException, InvalidTypeException

REQUESTS_TIMEOUT = 180


def get_inference_client(*, org_name, model_name, model_version_name):
    import_path = from_config(
        "MODEL_INFERENCE_CLIENT",
        "slai.clients.inference.ModelInferenceClient",
    )
    class_ = import_path.split(".")[-1]
    path = ".".join(import_path.split(".")[:-1])

    return getattr(import_module(path), class_)(
        org_name=org_name,
        model_name=model_name,
        model_version_name=model_version_name,
    )


@lru_cache(maxsize=64)
def _get_model_info(
    base_url, client_id, client_secret, model_id, model_version_id=None
):
    body = {"model_id": model_id}
    if model_version_id is not None:
        body["model_version_id"] = model_version_id

    res = requests.post(
        f"{base_url}/model/info",
        auth=HTTPBasicAuth(client_id, client_secret),
        json=body,
        timeout=REQUESTS_TIMEOUT,
    )
    res.raise_for_status()
    model_info = res.json()

    input_schema = ModelTypes.load_schema(model_info["input_schema"])
    output_schema = ModelTypes.load_schema(model_info["output_schema"])
    inference_url = model_info["inference_url"]

    return input_schema, output_schema, inference_url


class ModelInferenceClient:
    BACKEND_BASE_URL, _ = get_api_base_urls()

    def __init__(self, *, org_name, model_name, model_version_name=None):
        credentials = detect_credentials()

        self.client_id = credentials["client_id"]
        self.client_secret = credentials["client_secret"]

        self.org_name = org_name
        self.model_name = model_name
        self.model_version_name = model_version_name

        self._load_model()

    def _load_model(self):
        self.model_client = get_model_client(
            org_name=self.org_name,
            model_name=self.model_name,
        )
        self.model = self.model_client.get_model()

        if self.model_version_name is not None:
            self.model_version = self.model_client.get_model_version_by_name(
                model_version_name=self.model_version_name
            )
            self.model_version_id = self.model_version["id"]
        else:
            self.model_version_id = None

    def call(self, payload):
        input_schema, output_schema, inference_url = _get_model_info(
            self.BACKEND_BASE_URL,
            self.client_id,
            self.client_secret,
            self.model["id"],
            self.model_version_id,
        )

        try:
            serialized_payload = ModelTypes.serialize(payload, input_schema)
        except (InvalidTypeException, InvalidPayloadException) as e:
            print(e, e.errors)
            return None

        res = requests.post(
            f"{inference_url}",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            json=serialized_payload,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        response_data = res.json()

        errors = response_data["result"].get("errors", [])
        if errors:
            print("An unhandled exception occurred in your handler:\n ")

            for e in errors:
                print(e)

            return None

        try:
            result = ModelTypes.deserialize(response_data["result"], output_schema)
        except (InvalidTypeException, InvalidPayloadException) as e:
            print(e, e.errors)
            return None

        return result

    def info(self):
        return copy.copy(
            _get_model_info(
                self.BACKEND_BASE_URL,
                self.client_id,
                self.client_secret,
                self.model["id"],
                self.model_version_id,
            )
        )
