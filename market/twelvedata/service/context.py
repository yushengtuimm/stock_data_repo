class Context:
    http_client = None
    apikey = None
    base_url = None
    params = None

    @classmethod
    def from_context(cls, ctx):
        instance = cls()
        instance.http_client = ctx.http_client
        instance.apikey = ctx.apikey
        instance.base_url = ctx.base_url
        instance.params = dict(ctx.params or {})
        return instance
