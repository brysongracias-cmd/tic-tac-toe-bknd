# Generate an Excel API test report for the tic-tac-toe backend.
from dotenv import load_dotenv
load_dotenv('.env_93882a75-762a-45f3-a2b2-f23fdc62ca0d', override=True)
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

results = [
    ("GET", "/health", "Health check", 200, "PASS", "Real server boot verified OK on port 46999"),
    ("GET", "/", "Root status", 200, "PASS", "Route present and import/server checks passed"),
    ("POST", "/api/v1/auth/register", "Register user", 201, "PASS", "pytest test_register passed"),
    ("POST", "/api/v1/auth/login", "Login user", 200, "PASS", "pytest test_login passed"),
    ("GET", "/api/v1/auth/me", "Read current user", 200, "PASS", "pytest test_me passed; invalid token also returned 401"),
    ("POST", "/api/v1/games/", "Create game", 201, "PASS", "pytest test_create_game passed"),
    ("GET", "/api/v1/games/", "List games", 200, "PASS", "pytest test_list_games passed"),
    ("GET", "/api/v1/games/{game_id}", "Get game", 200, "PASS", "pytest test_get_game passed"),
    ("PATCH", "/api/v1/games/{game_id}", "Update game", 200, "PASS", "pytest test_update_game passed"),
    ("DELETE", "/api/v1/games/{game_id}", "Delete game", 204, "PASS", "pytest test_delete_game passed"),
    ("POST", "/api/v1/games/{game_id}/moves", "Make move", 201, "PASS", "pytest test_make_move passed"),
]

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "API Test Report"
hf = Font(bold=True, color="FFFFFF", size=11)
hbg = PatternFill("solid", fgColor="2F5496")
pg = PatternFill("solid", fgColor="C6EFCE")
fr = PatternFill("solid", fgColor="FFC7CE")
ctr = Alignment(horizontal="center", vertical="center", wrap_text=True)
lft = Alignment(horizontal="left", vertical="center", wrap_text=True)
t = Side(style="thin")
bdr = Border(left=t, right=t, top=t, bottom=t)
for c, h in enumerate(["#", "Method", "Endpoint", "Description", "Status Code", "Pass/Fail", "Reason"], 1):
    cell = ws.cell(row=1, column=c, value=h)
    cell.font = hf
    cell.fill = hbg
    cell.alignment = ctr
    cell.border = bdr
for row, (m, ep, desc, code, pf, rsn) in enumerate(results, 2):
    bg = pg if pf == "PASS" else fr
    for c, (v, a) in enumerate(zip([row - 1, m, ep, desc, code, pf, rsn], [ctr, ctr, lft, lft, ctr, ctr, lft]), 1):
        cell = ws.cell(row=row, column=c, value=v)
        cell.fill = bg
        cell.alignment = a
        cell.border = bdr
        if c == 6:
            cell.font = Font(bold=True, color="375623" if pf == "PASS" else "9C0006")
for i, w in enumerate([5, 10, 42, 32, 12, 12, 50], 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = "A2"
wb.save("api_test_report.xlsx")
print("Saved: api_test_report.xlsx")
