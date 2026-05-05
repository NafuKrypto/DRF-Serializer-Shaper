# drf-serializer-shaper

**Shape your Django REST Framework serializers dynamically — clean, strict, and code-first.**

---

## Why this library?

Working with nested serializers in DRF often leads to:

* Over-fetching unnecessary fields
* Rigid serializer definitions
* Messy customization logic

Most tools (like drf-flex-fields) focus on **query-parameter driven APIs**.

But what if you want **full control directly in Python code**?

That’s where **drf-serializer-shaper** comes in.

---

## Features

* Include only specific fields
* Exclude fields (including nested)
* Nested field control using `__` syntax
* Works with `many=True`
* Strict validation (no silent failures)
* No dependency on request/query params

---

## 📦 Installation

```bash
pip install drf-serializer-shaper
```

---

## ⚡ Quick Example

### Serializers

```python
from rest_framework import serializers
from drf_serializer_shaper.mixins import DynamicFieldsMixin


class CategorySerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"
```

---

### Usage

```python
serializer = ProductSerializer(
    product,
    exclude=["category__created_at"]
)

print(serializer.data)
```

---

### Output

```json
{
  "id": 1,
  "name": "Laptop",
  "category": {
    "id": 5,
    "name": "Electronics"
  }
}
```

---

## 🎯 Include Fields

```python
serializer = ProductSerializer(
    product,
    include=["id", "name"]
)
```

---

## 🔥 Nested Include

```python
serializer = ProductSerializer(
    product,
    include=["category__id", "category__name"]
)
```

---

##  Validation

Invalid fields will raise an error:

```python
ProductSerializer(product, include=["wrong_field"])
```

```
InvalidFieldError: {'wrong_field'}
```

---

## Design Philosophy

* **Code-first control** (no dependency on request)
* **Explicit > implicit**
* **Fail fast on mistakes**
* **Minimal magic, maximum clarity**

---

## Comparison

| Feature             | drf-serializer-shaper | drf-flex-fields |
| ------------------- | --------------------- | --------------- |
| Code-level control  | true                 | ❌               |
| Nested exclude      | true                   | ⚠️          |
| Strict validation   | true                   | ❌          |
| Query param support |false(planned)          | true        |

---

## Roadmap

* [ ] Dict-based nested API (`{"category": ["id", "name"]}`)
* [ ] Query optimization (`select_related`, `only`)
* [ ] Optional query-param support
* [ ] Performance benchmarks

---

## Contributing

PRs are welcome! Please:

* Add tests
* Keep API simple
* Avoid breaking changes

---

## 📄 License

MIT License

---

## ⭐ Support

If this helps you, consider giving the repo a star ⭐
