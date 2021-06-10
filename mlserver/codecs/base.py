from typing import Any, Dict, Type

from ..types import InferenceRequest, InferenceResponse, RequestInput, ResponseOutput


class InputCodec:
    """
    The InputCodec interface lets you define type conversions of your raw input
    data to / from the V2 Inference Protocol level.
    Note that this codec applies at the individual input level.
    For request-wide transformations (e.g. dataframes), use the RequestCodec
    interface instead.
    """

    def encode(self, name: str, payload: Any) -> ResponseOutput:
        raise NotImplementedError()

    def decode(self, request_input: RequestInput) -> Any:
        raise NotImplementedError()


class RequestCodec:
    """
    The RequestCodec interface lets you define request-level conversions.
    This can be useful where the encoding of your payload encompases multiple
    input heads (e.g. dataframes).
    For individual input-level encoding / decoding, use the InputCodec
    interface instead.
    """

    def encode(self, name: str, payload: Any) -> InferenceResponse:
        raise NotImplementedError()

    def decode(self, request: InferenceRequest) -> Any:
        raise NotImplementedError()


class _CodecRegistry:
    """
    CodecRegistry is a "fancy" dictionary to register and find codecs.
    This class has a singleton instance exposed at the module leve, which
    should be used preferably.
    """

    def __init__(
        self,
        input_codecs: Dict[str, InputCodec] = {},
        request_codecs: Dict[str, RequestCodec] = {},
    ):
        self._input_codecs = input_codecs
        self._request_codecs = request_codecs

    def register_input_codec(self, content_type: str, codec: InputCodec):
        # TODO: Raise error if codec exists?
        self._input_codecs[content_type] = codec

    def find_input_codec(self, content_type: str) -> InputCodec:
        # TODO: Raise error if codec doesn't exist
        return self._input_codecs[content_type]

    def register_request_codec(self, content_type: str, codec: RequestCodec):
        # TODO: Raise error if codec exists?
        self._request_codecs[content_type] = codec

    def find_request_codec(self, content_type: str) -> RequestCodec:
        # TODO: Raise error if codec doesn't exist
        return self._request_codecs[content_type]


_codec_registry = _CodecRegistry()

find_request_codec = _codec_registry.find_request_codec
find_input_codec = _codec_registry.find_input_codec


def register_request_codec(content_type: str):
    def inner(CodecKlass: Type[RequestCodec]):
        _codec_registry.register_request_codec(content_type, CodecKlass())
        return CodecKlass

    return inner


def register_input_codec(content_type: str):
    def inner(CodecKlass: Type[InputCodec]):
        _codec_registry.register_input_codec(content_type, CodecKlass())
        return CodecKlass

    return inner
