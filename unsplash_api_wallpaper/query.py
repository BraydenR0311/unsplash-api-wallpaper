class Query:
    """A simple container for URL query string."""

    def __init__(self, params: dict[str, str] = {}):
        """Start with specified query."""
        self.base = "?" + self.format_query(params).lstrip("&")

    def __call__(self, params: dict[str, str] = {}) -> str:
        """Return the base_query along with additional."""
        return self.base + self.format_query(params)

    @staticmethod
    def format_query(params: dict[str, str] = {}) -> str:
        """Format query str from dict."""
        param_str = ""
        for k, v in params.items():
            param_str = f"{param_str}&{k}={v}"
        return param_str
