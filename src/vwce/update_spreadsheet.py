import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from zoneinfo import ZoneInfo

from auth.google_credentials import load_google_credentials_dict

SPREADSHEET_NAME = "Situazione patrimoniale"
PAC_WORKSHEET_NAME = "PAC_allocazione_geografica"


def _get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(load_google_credentials_dict(), scope)
    return gspread.authorize(credentials)


def authenticate_google_sheets():
    client = _get_gspread_client()
    return client.open(SPREADSHEET_NAME)


def _get_pac_worksheet():
    return authenticate_google_sheets().worksheet(PAC_WORKSHEET_NAME)


def log_portfolio_weights(optimal_weights):
    sheet = _get_pac_worksheet()

    col_a = sheet.col_values(1)
    next_row = max(len(col_a) + 1, 6)

    now = datetime.now(ZoneInfo("Europe/Rome")).strftime("%Y-%m-%d %H:%M:%S")
    row = [now, round(float(optimal_weights[0]), 6), round(float(optimal_weights[1]), 6)]

    sheet.update([row], f'A{next_row}:C{next_row}')


def update_spreadsheet_with_allocation(optimal_weights, balanced_portfolio, comparison_df):
    try:
        sheet = _get_pac_worksheet()
    except Exception as e:
        print(f"Error authenticating with Google Sheets: {e}")
        return

    try:
        # Current weights and last-update timestamp (top of sheet)
        sheet.update_acell('B2', round(float(optimal_weights[0]), 6))
        sheet.update_acell('C2', round(float(optimal_weights[1]), 6))
        timestamp = datetime.now(ZoneInfo("Europe/Rome")).strftime("%Y-%m-%d %H:%M:%S")
        sheet.update_acell('A2', timestamp)

        # Geographical allocation table (columns E, F, G)
        sheet.batch_clear(["E2:G1000"])

        comparison_df = comparison_df.sort_values(by='VWCE', ascending=False)
        N = comparison_df.shape[0]

        country_list = [[x] for x in comparison_df.index.tolist()]
        balanced_portfolio_col = [[x] for x in comparison_df['SWDA+XMME'].values.tolist()]
        target_portfolio = [[x] for x in comparison_df['VWCE'].values.tolist()]

        last_row = N + 1
        sheet.update(country_list, f'E2:E{last_row}')
        sheet.update(balanced_portfolio_col, f'F2:F{last_row}')
        sheet.update(target_portfolio, f'G2:G{last_row}')

    except Exception as e:
        print(f"Error updating the spreadsheet: {e}")