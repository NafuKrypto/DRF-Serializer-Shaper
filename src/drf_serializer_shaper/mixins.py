from rest_framework import serializers
from .utils import build_nested_tree, flatten_tree
from .exceptions import InvalidFieldError


class DynamicFieldsMixin:
    def __init__(self, *args, **kwargs):
        self.include = kwargs.pop("include", None)
        self.exclude = kwargs.pop("exclude", None)

        super().__init__(*args, **kwargs)

        self._validate_fields()
        self._apply_root_filter()
        self._apply_nested_filter()

    # -----------------------
    # VALIDATION
    # -----------------------
    def _validate_fields(self):
        existing = set(self.fields.keys())

        if self.include:
            invalid = set(self.include) - existing
            if invalid:
                raise InvalidFieldError(f"Invalid include fields: {invalid}")

        if self.exclude:
            roots = {f.split("__")[0] for f in self.exclude}
            invalid = roots - existing
            if invalid:
                raise InvalidFieldError(f"Invalid exclude fields: {invalid}")

    # -----------------------
    # ROOT FILTERING
    # -----------------------
    def _apply_root_filter(self):
        if self.include:
            allowed = set(self.include)
            for field in list(self.fields.keys()):
                if field not in allowed:
                    self.fields.pop(field)

        if self.exclude:
            for field in self.exclude:
                root = field.split("__")[0]
                self.fields.pop(root, None)

    # -----------------------
    # NESTED FILTERING
    # -----------------------
    def _apply_nested_filter(self):
        if not self.exclude:
            return

        tree = build_nested_tree(self.exclude)

        for field_name, nested in tree.items():
            field = self.fields.get(field_name)
            if not field:
                continue

            serializer = self._get_child_serializer(field)

            if serializer and nested:
                nested_paths = [
                    "__".join(p) for p in flatten_tree(nested)
                ]

                serializer.exclude = nested_paths

                if hasattr(serializer, "_apply_root_filter"):
                    serializer._apply_root_filter()
                    serializer._apply_nested_filter()

    def _get_child_serializer(self, field):
        if isinstance(field, serializers.ListSerializer):
            return field.child
        elif hasattr(field, "fields"):
            return field
        return None