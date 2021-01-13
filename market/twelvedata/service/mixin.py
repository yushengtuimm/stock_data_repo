import csv


__all__ = ("JsonMixin", "Mixin")


class JsonMixin:
    def as_json(self):
        resp = self.execute(format="JSON")
        json = resp.json()
        if hasattr(self, "is_batch") and self.is_batch:
            return json
        if json.get("status") == "ok":
            return json.get("data") or json.get("values") or json.get("earnings") or []
        return json

    def as_raw_json(self):
        resp = self.execute(format="JSON")
        return resp.text


class Mixin(JsonMixin):
    pass
