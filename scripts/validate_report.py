#!/usr/bin/env python3
"""Validate a JSON report against one of this skill's schemas.

Usage:
  python validate_report.py --schema schemas/critic_report.schema.json \
                            --data quality-control/critic_report.json
  (the --schema/--data pair may be repeated to validate several files)
Implements the JSON-Schema subset this skill's schemas use: type, required,
properties, items, enum, const, minimum, maximum, pattern, additionalProperties,
minItems, maxItems, minLength, maxLength, oneOf, anyOf.
Exit codes: 0 all valid, 1 validation errors, 2 usage errors.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def validate(value, schema: dict, path: str, errors: list):
    if "oneOf" in schema:
        ok = 0
        for sub in schema["oneOf"]:
            tmp = []
            validate(value, sub, path, tmp)
            if not tmp:
                ok += 1
        if ok != 1:
            errors.append(f"{path}: matches {ok} of oneOf branches, expected exactly 1")
        return
    if "anyOf" in schema:
        tmp = []
        for sub in schema["anyOf"]:
            validate(value, sub, path, tmp)
        if tmp and len(tmp) == len(schema["anyOf"]):
            errors.append(f"{path}: matches none of anyOf branches")
        return
    t = schema.get("type")
    if t:
        types = t if isinstance(t, list) else [t]
        type_ok = any({
            "object": isinstance(value, dict),
            "array": isinstance(value, list),
            "string": isinstance(value, str),
            "boolean": isinstance(value, bool),
            "null": value is None,
            "number": isinstance(value, (int, float)) and not isinstance(value, bool),
            "integer": isinstance(value, int) and not isinstance(value, bool),
        }.get(tt, True) for tt in types)
        if not type_ok:
            errors.append(f"{path}: expected type {t}, got {type(value).__name__}")
            return
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in enum {schema['enum']}")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: longer than maxLength {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: does not match pattern {schema['pattern']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: above maximum {schema['maximum']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: fewer than minItems {schema['minItems']}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: more than maxItems {schema['maxItems']}")
        items = schema.get("items")
        if items:
            for i, item in enumerate(value):
                validate(item, items, f"{path}[{i}]", errors)
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for r in schema.get("required", []):
            if r not in value:
                errors.append(f"{path}: missing required property '{r}'")
        for k, v in value.items():
            if k in props:
                validate(v, props[k], f"{path}.{k}", errors)
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: additional property '{k}' not allowed")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--schema", action="append", required=True)
    ap.add_argument("--data", action="append", required=True)
    a = ap.parse_args()
    if len(a.schema) != len(a.data):
        print("error: each --data needs a matching --schema", file=sys.stderr)
        return 2
    total_errors = 0
    for s_path, d_path in zip(a.schema, a.data):
        try:
            schema = json.loads(Path(s_path).read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"error: cannot read schema {s_path}: {e}", file=sys.stderr)
            return 2
        try:
            data = json.loads(Path(d_path).read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"error: cannot read data {d_path}: {e}", file=sys.stderr)
            total_errors += 1
            continue
        errors: list = []
        validate(data, schema, "$", errors)
        if errors:
            print(f"INVALID {d_path} (schema {s_path}):")
            for e in errors[:50]:
                print(f"  - {e}")
            total_errors += len(errors)
        else:
            print(f"VALID   {d_path} (schema {s_path})")
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
