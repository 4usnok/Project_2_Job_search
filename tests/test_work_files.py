import json
import tempfile

from src.working_with_file import CreatedJson
from unittest.mock import patch


test_path = "data/test_stop_words.json"


def test_add_file():

