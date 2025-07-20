import os
import unittest
from backend.tools.search_tools import (
    serpapi_search,
    google_cse_search,
    brave_search,
)


class ToolEnvTest(unittest.TestCase):
    def test_serpapi_requires_key(self):
        env_var = os.environ.pop("SERPAPI_API_KEY", None)
        try:
            with self.assertRaises(ValueError):
                serpapi_search("OpenAI")
        finally:
            if env_var is not None:
                os.environ["SERPAPI_API_KEY"] = env_var

    def test_google_cse_requires_keys(self):
        key = os.environ.pop("GOOGLE_API_KEY", None)
        cse = os.environ.pop("GOOGLE_CSE_ID", None)
        try:
            with self.assertRaises(ValueError):
                google_cse_search("OpenAI")
        finally:
            if key is not None:
                os.environ["GOOGLE_API_KEY"] = key
            if cse is not None:
                os.environ["GOOGLE_CSE_ID"] = cse

    def test_brave_search_requires_key(self):
        key = os.environ.pop("BRAVE_API_KEY", None)
        try:
            with self.assertRaises(ValueError):
                brave_search("OpenAI")
        finally:
            if key is not None:
                os.environ["BRAVE_API_KEY"] = key


if __name__ == "__main__":
    unittest.main()
