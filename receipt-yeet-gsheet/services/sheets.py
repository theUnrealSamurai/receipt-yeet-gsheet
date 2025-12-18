import gspread
from gspread_formatting import CellFormat, TextFormat, format_cell_range

sheet = gspread.service_account(filename="/Users/mits-mac-001/Code/receipt-yeet-gsheet/receipt-yeet-gsheet-181e3b509ddb.json").open("Expenses")



def create_new_sheet(date_str: str):
    """Create a new worksheet for the given date string (YYYY-MM-DD)."""
    try:
        year, month, day = date_str.split("-")
        worksheet = sheet.add_worksheet(title=f"{year}_{month}", rows="100", cols="20")
        
        headers = ["Datetime", "PaymentMethod", "Category", "Items", "StoreName", "Location", "Total Amount", "Misc"]
        worksheet.append_row(headers)
        
        # make headers bold
        fmt = CellFormat(textFormat=TextFormat(bold=True))
        format_cell_range(worksheet, 'A1:H1', fmt)

        
        return worksheet
    except Exception as e:
        raise RuntimeError(f"Failed to create new sheet: {e}")



def append_row(row_data: dict):
    """Append a row of data to the specified worksheet without timezone/locale checks."""
    try:
        # Require Datetime from the receipt parsing
        dt = row_data.get("Datetime") or ""
        sheetname = dt[:7].replace("-", "_")
        worksheet = sheet.worksheet(sheetname)
        
        row = [
            dt,
            row_data.get("PaymentMethod", ""),
            row_data.get("Category", ""),
            row_data.get("Items", ""),
            row_data.get("StoreName", ""),
            row_data.get("Location", ""),
            row_data.get("TotalAmount", row_data.get("Total Amount", "")),
            row_data.get("Misc", ""),
        ]
        worksheet.append_row(row, value_input_option='USER_ENTERED')
        
    except gspread.exceptions.WorksheetNotFound:
        dt = row_data.get("Datetime") or ""
        worksheet = create_new_sheet(dt[:10])
        append_row(row_data)  # hehe recursion
        
    except Exception as e:
        raise RuntimeError(f"Failed to append row: {e}")
    


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    from ocr import ocr_image
    from llm import parse_receipt_text

    test_image = "/Users/mits-mac-001/Code/receipt-yeet-gsheet/test3.jpg"
    ocr_text = ocr_image(test_image)
    parsed = parse_receipt_text(ocr_text)
    append_row(parsed)
    print("Appended row:", parsed)