import types
import pytest
import nbformat


class TestNotebookFile:
    @pytest.fixture
    def open_ipynb(self):
        return nbformat.read("main.ipynb", as_version=4)

    @pytest.fixture
    def get_notebook_function(self, open_ipynb):
        def _get_function(function_name: str):
            nb = open_ipynb
            code_cells = [cell for cell in nb.cells[:20] if cell.cell_type == "code"]

            code = ""
            for cell in code_cells:
                code += cell.source + "\n"

            module = types.ModuleType("notebook_module")
            exec(code, module.__dict__)

            if function_name in module.__dict__:
                return module.__dict__[function_name]
            else:
                raise ValueError(f"Function {function_name} not found in notebook")

        return _get_function

    def test_load_notebook(self, open_ipynb):
        notebook = open_ipynb

        assert notebook.nbformat == 4
        assert len(notebook.cells) == 35
        assert notebook.cells[0].cell_type == "markdown"
        assert notebook.cells[1].cell_type == "code"

    def test_basic_count(self, get_notebook_function):
        counted_digits = get_notebook_function("counted_digits")
        """Test basic digit counting in a simple range."""
        assert counted_digits(1, 10, 1) == 2
        assert counted_digits(1, 100, 0) == 10

    def test_single_number_range(self, get_notebook_function):
        """Test when min_num equals max_num."""
        counted_digits = get_notebook_function("counted_digits")
        assert counted_digits(5, 5, 5) == 1
        assert counted_digits(5, 5, 6) == 0

    def test_digit_not_in_range(self, get_notebook_function):
        """Test when the digit is not present in the range."""
        counted_digits = get_notebook_function("counted_digits")
        assert counted_digits(4, 8, 9) == 0
