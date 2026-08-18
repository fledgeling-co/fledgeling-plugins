"""A stdlib JSON Schema subset, enough to validate what a model returns.

Covers: type, required, properties, additionalProperties, enum, items,
minimum, maximum, minItems, maxItems, minLength, maxLength, const, oneOf.

Deliberately not a full implementation. It validates the plugin's own schemas
and nothing else, and it reports every violation rather than the first, because
a verdict rejected for one reason usually has two.
"""

from __future__ import annotations

from typing import Any

_TYPES: dict[str, type | tuple[type, ...]] = {
    "object": dict,
    "array": list,
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "null": type(None),
}


def validate(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Return a list of human-readable violations. Empty means valid."""
    errs: list[str] = []

    if "const" in schema and instance != schema["const"]:
        errs.append(f"{path}: expected the constant {schema['const']!r}, got {instance!r}")

    if "enum" in schema and instance not in schema["enum"]:
        errs.append(f"{path}: {instance!r} is not one of {schema['enum']!r}")

    if "oneOf" in schema:
        matches = [i for i, sub in enumerate(schema["oneOf"])
                   if not validate(instance, sub, path)]
        if len(matches) != 1:
            errs.append(f"{path}: matched {len(matches)} of the oneOf branches, expected exactly 1")

    expected = schema.get("type")
    if expected:
        wanted = expected if isinstance(expected, list) else [expected]
        # bool is a subclass of int in Python; JSON Schema treats them apart.
        def ok(name: str) -> bool:
            if name in ("number", "integer") and isinstance(instance, bool):
                return False
            return isinstance(instance, _TYPES[name])
        if not any(ok(w) for w in wanted if w in _TYPES):
            errs.append(f"{path}: expected type {expected!r}, got {type(instance).__name__}")
            return errs                      # further checks would be noise

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errs.append(f"{path}: missing required key {key!r}")
        props = schema.get("properties", {})
        for key, sub in props.items():
            if key in instance:
                errs.extend(validate(instance[key], sub, f"{path}.{key}"))
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in props:
                    errs.append(f"{path}: unexpected key {key!r}")

    if isinstance(instance, list):
        if "items" in schema:
            for i, item in enumerate(instance):
                errs.extend(validate(item, schema["items"], f"{path}[{i}]"))
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errs.append(f"{path}: {len(instance)} item(s), minimum {schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errs.append(f"{path}: {len(instance)} item(s), maximum {schema['maxItems']}")

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errs.append(f"{path}: length {len(instance)}, minimum {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errs.append(f"{path}: length {len(instance)}, maximum {schema['maxLength']}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errs.append(f"{path}: {instance} is below the minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errs.append(f"{path}: {instance} is above the maximum {schema['maximum']}")

    return errs


def selftest() -> list[tuple[str, bool]]:
    """Each rule has to be observed failing as well as passing."""
    cases: list[tuple[str, bool]] = []

    s = {"type": "object", "required": ["a"], "additionalProperties": False,
         "properties": {"a": {"type": "string", "enum": ["x", "y"]},
                        "n": {"type": "integer", "minimum": 1, "maximum": 3}}}
    cases.append(("valid object passes", validate({"a": "x"}, s) == []))
    cases.append(("missing required fires", any("required" in e for e in validate({}, s))))
    cases.append(("enum fires", any("is not one of" in e for e in validate({"a": "z"}, s))))
    cases.append(("additionalProperties fires",
                  any("unexpected key" in e for e in validate({"a": "x", "q": 1}, s))))
    cases.append(("minimum fires", any("below the minimum" in e for e in validate({"a": "x", "n": 0}, s))))
    cases.append(("maximum fires", any("above the maximum" in e for e in validate({"a": "x", "n": 9}, s))))
    cases.append(("wrong type fires", any("expected type" in e for e in validate({"a": 1}, s))))
    cases.append(("bool is not an integer",
                  any("expected type" in e for e in validate(True, {"type": "integer"}))))

    arr = {"type": "array", "minItems": 1, "items": {"type": "string"}}
    cases.append(("array item type fires", any("expected type" in e for e in validate([1], arr))))
    cases.append(("minItems fires", any("minimum 1" in e for e in validate([], arr))))
    cases.append(("array valid passes", validate(["a"], arr) == []))

    one = {"oneOf": [{"type": "string"}, {"type": "integer"}]}
    cases.append(("oneOf single match passes", validate("a", one) == []))
    cases.append(("oneOf no match fires", any("oneOf" in e for e in validate([], one))))

    cases.append(("const fires", any("constant" in e for e in validate("b", {"const": "a"}))))
    cases.append(("maxLength fires", any("maximum 2" in e for e in validate("abc", {"type": "string", "maxLength": 2}))))
    return cases


if __name__ == "__main__":
    import sys
    results = selftest()
    for name, passed in results:
        print(f"  {'ok  ' if passed else 'FAIL'}  {name}")
    bad = sum(1 for _, p in results if not p)
    print(f"{len(results)} case(s), {bad} failure(s)")
    sys.exit(0 if bad == 0 else 2)
