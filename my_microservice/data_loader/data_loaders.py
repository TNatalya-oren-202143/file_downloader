import pandas as pd
import json
import yaml
import pdfplumber
#from docx import Document
import logging
import os
from typing import Dict


# Логирование
def setup_logging(config: Dict):
    log_level = getattr(logging, config.get("logging", {}).get("level", "DEBUG").upper())
    log_file = config.get("logging", {}).get("log_file", "app.log")

    logging.basicConfig(level=log_level,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler(), logging.FileHandler(log_file)])


# Абстрактный класс для загрузчиков данных
class DataLoader:
    def load_data(self, file_path: str, **kwargs) -> pd.DataFrame:
        raise NotImplementedError


# Класс для загрузки данных из Excel
class ExcelDataLoader(DataLoader):
    def load_data(self, file_path: str, sheet_name=0) -> pd.DataFrame:
        logging.info(f"Загрузка данных из {file_path}, лист {sheet_name}")
        print("!!", os.path.exists(file_path))
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден.")
        return pd.read_excel(file_path, sheet_name=sheet_name)


# Класс для загрузки данных из CSV
class CsvDataLoader(DataLoader):
    def load_data(self, file_path: str, **kwargs) -> pd.DataFrame:
        logging.info(f"Загрузка данных из {file_path}")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден.")
        return pd.read_csv(file_path)


# Класс для загрузки данных из JSON
class JsonDataLoader(DataLoader):
    def load_data(self, file_path: str, **kwargs) -> pd.DataFrame:
        logging.info(f"Загрузка данных из {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден.")

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return pd.json_normalize(data)
        except json.JSONDecodeError as e:
            logging.error(f"Ошибка декодирования JSON: {e}")
            raise ValueError(f"Ошибка при загрузке JSON файла {file_path}")
        except Exception as e:
            logging.error(f"Ошибка при загрузке данных из {file_path}: {e}")
            raise


# Класс для загрузки данных из YAML
class YamlDataLoader(DataLoader):
    def load_data(self, file_path: str, **kwargs) -> pd.DataFrame:
        logging.info(f"Загрузка данных из {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден.")

        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
            return pd.json_normalize(data)
        except yaml.YAMLError as e:
            logging.error(f"Ошибка при загрузке YAML файла: {e}")
            raise ValueError(f"Ошибка при загрузке YAML файла {file_path}")
        except Exception as e:
            logging.error(f"Ошибка при загрузке данных из {file_path}: {e}")
            raise


# Класс для загрузки данных из PDF
class PdfDataLoader(DataLoader):
    def load_data(self, file_path: str, **kwargs) -> pd.DataFrame:
        logging.info(f"Загрузка данных из {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден.")

        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
                # Преобразуем текст в DataFrame
                data = text.split('\n')
                return pd.DataFrame(data, columns=["Content"])
        except Exception as e:
            logging.error(f"Ошибка при загрузке PDF файла: {e}")
            raise

'''
# Класс для загрузки данных из DOCX
class DocxDataLoader(DataLoader):
    def load_data(self, file_path: str, **kwargs) -> pd.DataFrame:
        logging.info(f"Загрузка данных из {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден.")

        try:
            doc = Document(file_path)
            data = []
            for para in doc.paragraphs:
                data.append(para.text)
            return pd.DataFrame(data, columns=["Content"])
        except Exception as e:
            logging.error(f"Ошибка при загрузке DOCX файла: {e}")
            raise
'''