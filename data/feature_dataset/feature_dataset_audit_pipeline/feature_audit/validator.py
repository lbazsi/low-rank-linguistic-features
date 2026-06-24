from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Tuple

from .utils import canonicalize_text, parse_example_id, split_from_index, is_empty_value


REQUIRED_FIELDS = [
    "id",
    "variable_id",
    "variable",
    "approach",
    "language",
    "surface_type",
    "contrast",
    "split",
    "pair",
]

ALLOWED_APPROACHES = {"EN", "EN+ctrl", "XL", "EN+XL"}
ALLOWED_LANGUAGES = {"en", "tr", "ja", "ko", "es", "ru", "ar", "zh"}
ALLOWED_SURFACE_TYPES = {"en", "en_ctrl", "xl", "pseudo"}
ALLOWED_SPLITS = {"train", "val", "test"}
PAIR_TYPES = {"basis", "changed"}


@dataclass
class ValidationConfig:
    min_sentence_chars: int = 5
    max_sentence_chars: int = 600
    max_examples_per_variable: int = 500
    strict_surface_type: bool = True


@dataclass
class ValidationState:
    seen_ids: Set[str] = field(default_factory=set)
    seen_pairs: Set[Tuple[str, str]] = field(default_factory=set)


def validate_example(
    obj: Dict[str, Any],
    *,
    source_file: str,
    line_number: int,
    state: ValidationState,
    config: ValidationConfig,
) -> Tuple[bool, Dict[str, Any]]:
    errors: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []

    def err(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    def warn(code: str, message: str) -> None:
        warnings.append({"code": code, "message": message})

    for field_name in REQUIRED_FIELDS:
        if field_name not in obj:
            err("missing_required_field", f"Missing required field: {field_name}")
        elif is_empty_value(obj[field_name]):
            err("empty_required_field", f"Required field is empty: {field_name}")

    example_id = obj.get("id")
    variable_id = obj.get("variable_id")

    parsed_id = None
    if isinstance(example_id, str):
        parsed_id = parse_example_id(example_id)
        if parsed_id is None:
            err("invalid_id_format", "ID must match format '<variable_id>_<three_digit_index>', e.g. '26_001'.")
        else:
            id_variable, id_index = parsed_id
            if not (1 <= id_variable <= 40):
                err("id_variable_out_of_range", "Variable ID encoded in ID must be between 1 and 40.")
            if not (1 <= id_index <= config.max_examples_per_variable):
                err("id_index_out_of_range", f"Example index must be between 001 and {config.max_examples_per_variable:03d}.")
    else:
        err("id_not_string", "Field 'id' must be a string.")

    if isinstance(example_id, str):
        if example_id in state.seen_ids:
            err("duplicate_id", f"Duplicate example ID: {example_id}")
        else:
            state.seen_ids.add(example_id)

    if not isinstance(variable_id, int):
        err("variable_id_not_int", "Field 'variable_id' must be an integer.")
    elif not (1 <= variable_id <= 40):
        err("variable_id_out_of_range", "Field 'variable_id' must be between 1 and 40.")

    if parsed_id and isinstance(variable_id, int):
        id_variable, id_index = parsed_id
        if id_variable != variable_id:
            err("variable_id_mismatch", f"ID encodes variable_id={id_variable}, but field variable_id={variable_id}.")

    approach = obj.get("approach")
    if approach not in ALLOWED_APPROACHES:
        err("invalid_approach", f"Approach must be one of {sorted(ALLOWED_APPROACHES)}.")

    language = obj.get("language")
    if language not in ALLOWED_LANGUAGES:
        err("invalid_language_code", f"Language must be one of {sorted(ALLOWED_LANGUAGES)}.")

    surface_type = obj.get("surface_type")
    if surface_type not in ALLOWED_SURFACE_TYPES:
        err("invalid_surface_type", f"surface_type must be one of {sorted(ALLOWED_SURFACE_TYPES)}.")

    if config.strict_surface_type and approach in ALLOWED_APPROACHES and language in ALLOWED_LANGUAGES and surface_type in ALLOWED_SURFACE_TYPES:
        if approach == "EN" and not (language == "en" and surface_type == "en"):
            err("surface_type_approach_mismatch", "EN examples should use language='en' and surface_type='en'.")
        elif approach == "EN+ctrl" and not (language == "en" and surface_type in {"en", "en_ctrl"}):
            err("surface_type_approach_mismatch", "EN+ctrl examples should use language='en' and surface_type='en' or 'en_ctrl'.")
        elif approach == "XL" and not (language != "en" and surface_type == "xl"):
            err("surface_type_approach_mismatch", "XL examples should use a non-English language and surface_type='xl'.")
        elif approach == "EN+XL":
            if language == "en" and surface_type not in {"en", "en_ctrl"}:
                err("surface_type_approach_mismatch", "EN+XL English-side examples should use surface_type='en' or 'en_ctrl'.")
            if language != "en" and surface_type != "xl":
                err("surface_type_approach_mismatch", "EN+XL non-English examples should use surface_type='xl'.")

    contrast = obj.get("contrast")
    if not isinstance(contrast, str) or not contrast.strip():
        err("invalid_contrast", "Field 'contrast' must be a non-empty string.")
    elif " " in contrast:
        warn("contrast_contains_spaces", "Contrast labels should usually use snake_case, e.g. direct_to_reported.")

    split = obj.get("split")
    if split not in ALLOWED_SPLITS:
        err("invalid_split", f"Split must be one of {sorted(ALLOWED_SPLITS)}.")
    elif parsed_id:
        _, id_index = parsed_id
        expected_split = split_from_index(id_index)
        if expected_split == "out_of_range":
            err("split_id_out_of_range", "ID index is outside the configured split range.")
        elif split != expected_split:
            err("split_mismatch", f"ID index {id_index:03d} implies split='{expected_split}', but field split='{split}'.")

    pair = obj.get("pair")
    basis_sentence = None
    changed_sentence = None

    if not isinstance(pair, list):
        err("pair_not_list", "Field 'pair' must be a list.")
    elif len(pair) != 2:
        err("pair_wrong_length", "Field 'pair' must contain exactly two items: basis and changed.")
    else:
        found_types = set()
        for i, item in enumerate(pair):
            if not isinstance(item, dict):
                err("pair_item_not_object", f"Pair item {i} must be an object.")
                continue

            item_type = item.get("type")
            sentence = item.get("sentence")

            if item_type not in PAIR_TYPES:
                err("invalid_pair_type", f"Pair item {i} has invalid type: {item_type}. Must be basis or changed.")
            else:
                if item_type in found_types:
                    err("duplicate_pair_type", f"Pair has duplicate type: {item_type}.")
                found_types.add(item_type)

            if not isinstance(sentence, str) or not sentence.strip():
                err("invalid_sentence", f"Pair item {i} has missing or empty sentence.")
            else:
                sentence_stripped = sentence.strip()
                if len(sentence_stripped) < config.min_sentence_chars:
                    err("sentence_too_short", f"Sentence in pair item {i} is shorter than {config.min_sentence_chars} characters.")
                if len(sentence_stripped) > config.max_sentence_chars:
                    err("sentence_too_long", f"Sentence in pair item {i} is longer than {config.max_sentence_chars} characters.")
                if item_type == "basis":
                    basis_sentence = sentence_stripped
                elif item_type == "changed":
                    changed_sentence = sentence_stripped

        missing_types = PAIR_TYPES - found_types
        if missing_types:
            err("missing_pair_type", f"Pair is missing type(s): {sorted(missing_types)}.")

    if basis_sentence and changed_sentence:
        canon_pair = (canonicalize_text(basis_sentence), canonicalize_text(changed_sentence))
        reverse_pair = (canon_pair[1], canon_pair[0])

        if canon_pair[0] == canon_pair[1]:
            err("basis_changed_identical", "Basis and changed sentences are identical after normalization.")

        if canon_pair in state.seen_pairs or reverse_pair in state.seen_pairs:
            err("duplicate_sentence_pair", "Duplicate or reversed duplicate sentence pair detected.")
        else:
            state.seen_pairs.add(canon_pair)

    passed = len(errors) == 0

    result = {
        "source_file": source_file,
        "line_number": line_number,
        "id": example_id if isinstance(example_id, str) else None,
        "passed": passed,
        "errors": errors,
        "warnings": warnings,
        "example": obj,
    }

    return passed, result
