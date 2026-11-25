import pandas as pd


def find_duplicates(df, date_window_days=7, amount_tolerance=1.0):
    """يرجع الداتا مع عمود duplicate_flag (True إذا عندها تكرار محتمل)"""
    df = df.copy()

    # تنظيف
    df["supplier"] = df["supplier"].str.strip().str.lower()
    df["amount"] = df["amount"].round(2)
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])

    # نقارن كل زوج بنفس المورد
    pairs = df.merge(df, on="supplier", suffixes=("", "_other"))
    pairs = pairs[pairs["invoice_id"] < pairs["invoice_id_other"]]

    # فرق المبلغ المسموح به (هامش صغير)
    same_amount = (pairs["amount"] - pairs["amount_other"]).abs() <= amount_tolerance
    # فرق التاريخ ضمن النافذة
    same_window = (pairs["invoice_date"] - pairs["invoice_date_other"]).abs() <= pd.Timedelta(days=date_window_days)

    pairs = pairs[same_amount & same_window]

    dup_ids = set(pairs["invoice_id"]) | set(pairs["invoice_id_other"])
    df["duplicate_flag"] = df["invoice_id"].isin(dup_ids)
    return df
