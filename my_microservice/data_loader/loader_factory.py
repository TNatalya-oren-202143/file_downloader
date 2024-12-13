from .data_loaders import ( ExcelDataLoader, CsvDataLoader, JsonDataLoader, YamlDataLoader, PdfDataLoader #, DocxDataLoader
                            )


class DataLoaderFactory:
    def create_loader(self, file_path: str):
        extension = file_path.split('.')[-1].lower()
        if extension == 'xlsx':
            return ExcelDataLoader()
        elif extension == 'csv':
            return CsvDataLoader()
        elif extension == 'json':
            return JsonDataLoader()
        elif extension == 'yaml' or extension == 'yml':
            return YamlDataLoader()
        elif extension == 'pdf':
            return PdfDataLoader()
        # elif extension == 'docx':
        #     return DocxDataLoader()
        else:
            raise ValueError(f"Формат файла {extension} не поддерживается.")
