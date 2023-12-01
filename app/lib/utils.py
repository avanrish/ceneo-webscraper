import csv
import pandas as pd
from io import StringIO, BytesIO


class Utils:
    @staticmethod
    def dict_to_csv(dict):
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=dict[0].keys())
        writer.writeheader()
        for row in dict:
            writer.writerow(row)
        csv_content = output.getvalue()
        output.close()
        return csv_content

    @staticmethod
    def dict_to_xlsx(dict):
        df = pd.DataFrame(dict)
        for column in df.columns:
            if pd.api.types.is_datetime64tz_dtype(df[column]):
                df[column] = df[column].dt.tz_convert('UTC').dt.tz_localize(None)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        excel_content = output.getvalue()
        output.close()
        return excel_content
