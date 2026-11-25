import pandas as pd


def find_duplicates(df, date_window_days=7):
    """يرجع قائمة الفواتير اللي عندها تكرار محتمل"""
    df = df.copy()

    # تنظيف: إزالة المسافات وتوحيد الحروف
    df["supplier"] = df["supplier"].str.strip().str.lower()
    df["amount"] = df["amount"].round(2)
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])

    # نقارن كل زوج بنفس المورد والمبلغ
    pairs = df.merge(df, on=["supplier", "amount"], suffixes=("", "_other"))
    pairs = pairs[
        (pairs["invoice_id"] < pairs["invoice_id_other"])
        & ((pairs["invoice_date"] - pairs["invoice_date_other"]).abs()
           <= pd.Timedelta(days=date_window_days))
    ]

    dup_ids = set(pairs["invoice_id"]) | set(pairs["invoice_id_other"])
    df["duplicate_flag"] = df["invoice_id"].isin(dup_ids)
    return df
