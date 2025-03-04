"""utility functions for preprocessor tests"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from base64 import b64encode

from nbformat import v4 as nbformat

from ...exporters.exporter import ResourcesDict
from ...tests.base import TestsBase


class PreprocessorTestsBase(TestsBase):
    """Contains test functions preprocessor tests"""

    def build_notebook(self, with_json_outputs=False, with_attachment=False):
        """Build a notebook in memory for use with preprocessor tests"""

        outputs = [
            nbformat.new_output("stream", name="stdout", text="a"),
            nbformat.new_output("display_data", data={"text/plain": "b"}),
            nbformat.new_output("stream", name="stdout", text="c"),
            nbformat.new_output("stream", name="stdout", text="d"),
            nbformat.new_output("stream", name="stderr", text="e"),
            nbformat.new_output("stream", name="stderr", text="f"),
            nbformat.new_output("display_data", data={"image/png": "Zw=="}),  # g
            nbformat.new_output("display_data", data={"application/pdf": "aA=="}),  # h
        ]
        if with_json_outputs:
            outputs.extend(
                [
                    nbformat.new_output("display_data", data={"application/json": [1, 2, 3]}),  # j
                    nbformat.new_output(
                        "display_data", data={"application/json": {"a": 1, "c": {"b": 2}}}
                    ),  # k
                    nbformat.new_output("display_data", data={"application/json": "abc"}),  # l
                    nbformat.new_output("display_data", data={"application/json": 15.03}),  # m
                ]
            )

        cells = [
            nbformat.new_code_cell(source="$ e $", execution_count=1, outputs=outputs),
            nbformat.new_markdown_cell(source="$ e $"),
        ]

        if with_attachment:
            data = b"test"
            encoded_data = b64encode(data)
            # this is conversion of bytes to string, not base64 decoding
            attachments = {"image.png": {"image/png": encoded_data.decode()}}
            cells.extend(
                [
                    nbformat.new_markdown_cell(
                        source="![image.png](attachment:image.png)", attachments=attachments
                    )
                ]
            )

        return nbformat.new_notebook(cells=cells)

    def build_resources(self):
        """Build an empty resources dictionary."""

        res = ResourcesDict()
        res["metadata"] = ResourcesDict()
        return res
