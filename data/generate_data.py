import pandas as pd
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# PERSONS
# ============================================================

persons = [
    ["P001", "Arjun Mehta", "9876543210", "Delhi", "DL01AB1234"],
    ["P002", "Rohan Sharma", "9876501234", "Mumbai", "MH02CD4567"],
    ["P003", "Vikram Rao", "9812345678", "Hyderabad", "TS09EF7890"],
    ["P004", "Sameer Khan", "9898989898", "Delhi", "DL03GH1122"],
    ["P005", "Amit Verma", "9765432109", "Mumbai", "MH04IJ3344"],
    ["P006", "Karan Singh", "9988776655", "Chandigarh", "CH01KL5566"],
    ["P007", "Nikhil Patel", "9123456789", "Ahmedabad", "GJ05MN7788"],
    ["P008", "Rahul Das", "9001122334", "Kolkata", "WB06OP9900"],
    ["P009", "Suresh Iyer", "9334455667", "Bengaluru", "KA07QR2211"],
    ["P010", "Manish Gupta", "9445566778", "Lucknow", "UP08ST4433"],
    ["P011", "Dev Malhotra", "9556677889", "Delhi", "DL09UV6655"],
    ["P012", "Aditya Kapoor", "9667788990", "Jaipur", "RJ10WX8877"],
    ["P013", "Rajiv Nair", "9778899001", "Kochi", "KL11YZ1199"],
    ["P014", "Harsh Joshi", "9889900112", "Pune", "MH12AB2233"],
    ["P015", "Ankit Yadav", "9990011223", "Patna", "BR13CD4455"],
    ["P016", "Mohit Bansal", "9112233445", "Noida", "UP14EF6677"],
    ["P017", "Tarun Sethi", "9223344556", "Gurugram", "HR15GH8899"],
    ["P018", "Yash Thakur", "9334455000", "Shimla", "HP16IJ0011"],
    ["P019", "Vivek Menon", "9445566000", "Chennai", "TN17KL2233"],
    ["P020", "Ravi Choudhary", "9556677000", "Jaipur", "RJ18MN4455"],
    ["P021", "Kunal Arora", "9667788000", "Delhi", "DL19PQ6677"],
    ["P022", "Sanjay Reddy", "9778899000", "Hyderabad", "TS20RS8899"],
    ["P023", "Manoj Pillai", "9889900001", "Kochi", "KL21TU0011"],
    ["P024", "Ritesh Kumar", "9990011002", "Patna", "BR22VW2233"],
    ["P025", "Abhishek Jain", "9112233003", "Pune", "MH23XY4455"],
]

persons_df = pd.DataFrame(
    persons,
    columns=[
        "Person_ID",
        "Name",
        "Phone",
        "Location",
        "Vehicle"
    ]
)


# ============================================================
# CALLS
# ============================================================

calls = [
    ["C001", "P001", "P002", "2026-01-05", "10:15", 120],
    ["C002", "P001", "P003", "2026-01-06", "11:30", 240],
    ["C003", "P002", "P003", "2026-01-07", "14:20", 180],
    ["C004", "P003", "P004", "2026-01-08", "16:45", 300],
    ["C005", "P004", "P005", "2026-01-09", "09:10", 90],
    ["C006", "P005", "P006", "2026-01-10", "18:30", 210],
    ["C007", "P006", "P007", "2026-01-11", "12:15", 150],
    ["C008", "P007", "P008", "2026-01-12", "13:40", 200],
    ["C009", "P008", "P009", "2026-01-13", "15:25", 100],
    ["C010", "P009", "P010", "2026-01-14", "17:00", 170],

    ["C011", "P001", "P004", "2026-01-15", "10:30", 250],
    ["C012", "P001", "P005", "2026-01-16", "11:45", 190],
    ["C013", "P002", "P006", "2026-01-17", "12:20", 160],
    ["C014", "P003", "P007", "2026-01-18", "14:00", 220],
    ["C015", "P004", "P008", "2026-01-19", "15:15", 180],
    ["C016", "P005", "P009", "2026-01-20", "16:30", 140],
    ["C017", "P006", "P010", "2026-01-21", "17:45", 260],
    ["C018", "P007", "P011", "2026-01-22", "18:10", 120],
    ["C019", "P008", "P012", "2026-01-23", "09:45", 230],
    ["C020", "P009", "P013", "2026-01-24", "10:50", 190],

    ["C021", "P010", "P014", "2026-01-25", "11:25", 150],
    ["C022", "P011", "P015", "2026-01-26", "12:35", 200],
    ["C023", "P012", "P016", "2026-01-27", "13:50", 170],
    ["C024", "P013", "P017", "2026-01-28", "14:40", 280],
    ["C025", "P014", "P018", "2026-01-29", "15:30", 130],
    ["C026", "P015", "P019", "2026-01-30", "16:20", 210],
    ["C027", "P016", "P020", "2026-01-31", "17:10", 160],

    # Repeated calls
    ["C028", "P001", "P002", "2026-02-01", "10:10", 130],
    ["C029", "P001", "P002", "2026-02-02", "10:20", 140],
    ["C030", "P001", "P002", "2026-02-03", "10:25", 150],

    ["C031", "P003", "P004", "2026-02-04", "11:10", 180],
    ["C032", "P003", "P004", "2026-02-05", "11:15", 190],

    ["C033", "P005", "P006", "2026-02-06", "14:20", 200],
    ["C034", "P005", "P006", "2026-02-07", "14:25", 210],

    ["C035", "P010", "P011", "2026-02-08", "15:30", 170],
    ["C036", "P011", "P012", "2026-02-09", "16:40", 220],
    ["C037", "P012", "P013", "2026-02-10", "17:50", 160],
    ["C038", "P013", "P014", "2026-02-11", "18:10", 240],
    ["C039", "P014", "P015", "2026-02-12", "09:30", 150],
    ["C040", "P015", "P016", "2026-02-13", "10:40", 180],

    ["C041", "P017", "P018", "2026-02-14", "11:20", 200],
    ["C042", "P018", "P019", "2026-02-15", "12:30", 190],
    ["C043", "P019", "P020", "2026-02-16", "13:40", 220],
    ["C044", "P020", "P021", "2026-02-17", "14:50", 170],
    ["C045", "P021", "P022", "2026-02-18", "15:30", 210],
    ["C046", "P022", "P023", "2026-02-19", "16:40", 160],
    ["C047", "P023", "P024", "2026-02-20", "17:50", 230],
    ["C048", "P024", "P025", "2026-02-21", "18:20", 180],
]

calls_df = pd.DataFrame(
    calls,
    columns=[
        "Call_ID",
        "Caller",
        "Receiver",
        "Date",
        "Time",
        "Duration_Seconds"
    ]
)


# ============================================================
# TRANSACTIONS
# ============================================================

transactions = [
    ["T001", "P001", "P002", 5000, "2026-01-05", "Bank Transfer"],
    ["T002", "P002", "P003", 7500, "2026-01-07", "Bank Transfer"],
    ["T003", "P003", "P004", 12000, "2026-01-09", "UPI"],
    ["T004", "P004", "P005", 4500, "2026-01-11", "UPI"],
    ["T005", "P005", "P006", 9000, "2026-01-13", "Bank Transfer"],
    ["T006", "P006", "P007", 6500, "2026-01-15", "UPI"],
    ["T007", "P007", "P008", 8000, "2026-01-17", "Bank Transfer"],
    ["T008", "P008", "P009", 3500, "2026-01-19", "UPI"],
    ["T009", "P009", "P010", 11000, "2026-01-21", "Bank Transfer"],

    ["T010", "P001", "P004", 15000, "2026-01-23", "Bank Transfer"],
    ["T011", "P002", "P005", 18000, "2026-01-25", "UPI"],
    ["T012", "P003", "P006", 22000, "2026-01-27", "Bank Transfer"],
    ["T013", "P004", "P007", 9500, "2026-01-29", "UPI"],
    ["T014", "P005", "P008", 13500, "2026-01-31", "Bank Transfer"],
    ["T015", "P006", "P009", 7000, "2026-02-02", "UPI"],
    ["T016", "P007", "P010", 12500, "2026-02-04", "Bank Transfer"],

    # Large transactions for alert testing
    ["T017", "P001", "P003", 75000, "2026-02-06", "Bank Transfer"],
    ["T018", "P003", "P005", 85000, "2026-02-08", "Bank Transfer"],
    ["T019", "P005", "P007", 65000, "2026-02-10", "UPI"],
    ["T020", "P007", "P009", 92000, "2026-02-12", "Bank Transfer"],

    ["T021", "P010", "P012", 14500, "2026-02-14", "UPI"],
    ["T022", "P011", "P013", 16500, "2026-02-16", "Bank Transfer"],
    ["T023", "P012", "P014", 19000, "2026-02-18", "UPI"],
    ["T024", "P013", "P015", 21000, "2026-02-20", "Bank Transfer"],
    ["T025", "P014", "P016", 11500, "2026-02-22", "UPI"],
    ["T026", "P015", "P017", 13500, "2026-02-24", "Bank Transfer"],
    ["T027", "P016", "P018", 15500, "2026-02-26", "UPI"],
    ["T028", "P017", "P019", 17500, "2026-02-28", "Bank Transfer"],
    ["T029", "P018", "P020", 19500, "2026-03-02", "UPI"],

    ["T030", "P020", "P021", 22500, "2026-03-04", "Bank Transfer"],
    ["T031", "P021", "P022", 24500, "2026-03-06", "UPI"],
    ["T032", "P022", "P023", 27500, "2026-03-08", "Bank Transfer"],
    ["T033", "P023", "P024", 30500, "2026-03-10", "UPI"],
    ["T034", "P024", "P025", 32500, "2026-03-12", "Bank Transfer"],
]

transactions_df = pd.DataFrame(
    transactions,
    columns=[
        "Transaction_ID",
        "Sender",
        "Receiver",
        "Amount",
        "Date",
        "Type"
    ]
)


# ============================================================
# CASES
# ============================================================

cases = [
    ["CASE001", "P001", "Financial Investigation", "High", "Open"],
    ["CASE002", "P002", "Communication Analysis", "Medium", "Open"],
    ["CASE003", "P003", "Financial Investigation", "High", "Under Review"],
    ["CASE004", "P004", "Network Investigation", "High", "Open"],
    ["CASE005", "P005", "Financial Investigation", "Medium", "Closed"],
    ["CASE006", "P006", "Communication Analysis", "Low", "Under Review"],
    ["CASE007", "P007", "Network Investigation", "High", "Open"],
    ["CASE008", "P008", "Entity Investigation", "Medium", "Open"],
    ["CASE009", "P009", "Financial Investigation", "High", "Under Review"],
    ["CASE010", "P010", "Communication Analysis", "Low", "Closed"],
    ["CASE011", "P011", "Network Investigation", "Medium", "Open"],
    ["CASE012", "P012", "Financial Investigation", "High", "Open"],
    ["CASE013", "P013", "Entity Investigation", "Low", "Closed"],
    ["CASE014", "P014", "Network Investigation", "Medium", "Under Review"],
    ["CASE015", "P015", "Financial Investigation", "High", "Open"],
    ["CASE016", "P016", "Communication Analysis", "Medium", "Open"],
    ["CASE017", "P017", "Network Investigation", "Low", "Closed"],
    ["CASE018", "P018", "Entity Investigation", "Medium", "Under Review"],
    ["CASE019", "P019", "Financial Investigation", "High", "Open"],
    ["CASE020", "P020", "Network Investigation", "Medium", "Open"],
    ["CASE021", "P021", "Financial Investigation", "High", "Open"],
    ["CASE022", "P022", "Communication Analysis", "Medium", "Under Review"],
    ["CASE023", "P023", "Network Investigation", "High", "Open"],
    ["CASE024", "P024", "Entity Investigation", "Low", "Closed"],
    ["CASE025", "P025", "Financial Investigation", "High", "Open"],
]

cases_df = pd.DataFrame(
    cases,
    columns=[
        "Case_ID",
        "Person_ID",
        "Case_Type",
        "Priority",
        "Status"
    ]
)


# ============================================================
# SAVE CSV FILES
# ============================================================

persons_df.to_csv(
    os.path.join(DATA_DIR, "persons.csv"),
    index=False
)

calls_df.to_csv(
    os.path.join(DATA_DIR, "calls.csv"),
    index=False
)

transactions_df.to_csv(
    os.path.join(DATA_DIR, "transactions.csv"),
    index=False
)

cases_df.to_csv(
    os.path.join(DATA_DIR, "cases.csv"),
    index=False
)


# ============================================================
# VERIFY
# ============================================================

print("=" * 60)
print("CRIMEGRAPH AI DATA CREATED")
print("=" * 60)

print(f"Persons       : {len(persons_df)}")
print(f"Call records  : {len(calls_df)}")
print(f"Transactions  : {len(transactions_df)}")
print(f"Cases         : {len(cases_df)}")

print()
print("Created:")
print("  data/persons.csv")
print("  data/calls.csv")
print("  data/transactions.csv")
print("  data/cases.csv")

print("=" * 60)