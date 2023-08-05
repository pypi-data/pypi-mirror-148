import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":  # pragma: no cover
    raise RuntimeError(
        "Calling `nlu_bf.core.evaluate` directly is no longer supported. Please use "
        "`nlu_bf test` to test a combined Core and NLU model or `nlu_bf test core` "
        "to test a Core model."
    )
