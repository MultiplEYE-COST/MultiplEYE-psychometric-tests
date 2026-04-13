import os
import re
import tempfile
import zipfile

import pandas as pd


def resolve_table_file(base_path_without_ext, file_label='input file'):
    """
    Resolve a table file path, preferring xlsx but allowing csv.
    """
    candidate_extensions = ('.xlsx', '.csv')
    for extension in candidate_extensions:
        candidate_path = f'{base_path_without_ext}{extension}'
        if os.path.exists(candidate_path):
            return candidate_path

    tried_paths = ", ".join(f"{base_path_without_ext}{ext}" for ext in candidate_extensions)
    raise FileNotFoundError(f"Could not find {file_label}. Tried: {tried_paths}")


def load_table_file(table_path, **kwargs):
    """
    Load a tabular file from csv/xlsx based on file extension.
    """
    if table_path.endswith('.csv'):
        return pd.read_csv(table_path, **kwargs)

    # pandas/openpyxl can fail on malformed xlsx merge metadata in some files.
    excel_kwargs = dict(kwargs)
    excel_kwargs.pop('encoding', None)  # not used by read_excel
    try:
        return pd.read_excel(table_path, **excel_kwargs)
    except Exception as excel_error:
        base_path, _ = os.path.splitext(table_path)
        fallback_csv_path = f'{base_path}.csv'
        if os.path.exists(fallback_csv_path):
            return pd.read_csv(fallback_csv_path, **kwargs)

        # Final fallback: strip malformed merge metadata from workbook XML
        # and retry with pandas/openpyxl.
        try:
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
                sanitized_path = temp_file.name

            with zipfile.ZipFile(table_path, 'r') as source_zip, zipfile.ZipFile(sanitized_path, 'w') as target_zip:
                for item in source_zip.infolist():
                    data = source_zip.read(item.filename)
                    if item.filename.startswith('xl/worksheets/sheet') and item.filename.endswith('.xml'):
                        # Remove mergeCells block; merge metadata is optional for data reads
                        # and malformed merge refs can crash openpyxl parsing.
                        try:
                            xml_text = data.decode('utf-8')
                            xml_text = re.sub(r'<mergeCells[^>]*>.*?</mergeCells>', '', xml_text, flags=re.DOTALL)
                            data = xml_text.encode('utf-8')
                        except UnicodeDecodeError:
                            pass
                    target_zip.writestr(item, data)

            try:
                return pd.read_excel(sanitized_path, **excel_kwargs)
            finally:
                if os.path.exists(sanitized_path):
                    os.remove(sanitized_path)
        except Exception:
            raise excel_error
