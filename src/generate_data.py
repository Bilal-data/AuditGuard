import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000
df = pd.DataFrame({
    "invoice_id": [f"INV-{i:04d}" for i in range(1, n + 1)],
    "supplier": np.random.choice(["Supplier A", "Supplier B", "Supplier C", "Supplier D"], n),
    "amount": np.round(np.random.uniform(100, 20000, n), 2),
    "invoice_date": pd.Timestamp("2026-11-01") + pd.to_timedelta(np.random.randint(0, 30, n), unit="D"),
    "duplicate_type": "",
    "is_duplicate": False,
})

# نختار 80 فاتورة أصلية، ونقسمهم على 4 أنواع تكرار
originals = df.sample(80, random_state=1)
groups = np.array_split(originals.index.to_numpy(), 4)
types = ["exact", "late_resend", "amount_diff", "name_variant"]

copies = []
next_id = n + 1
for idx, kind in zip(groups, types):
    c = df.loc[idx].copy()
    c["invoice_id"] = [f"INV-{i:04d}" for i in range(next_id, next_id + len(c))]
    next_id += len(c)
    c["duplicate_type"] = kind
    c["is_duplicate"] = True

    if kind == "late_resend":
        # نفس الفاتورة أُعيد إرسالها بعد 3 إلى 20 يوم
        c["invoice_date"] = c["invoice_date"] + pd.to_timedelta(np.random.randint(3, 21, len(c)), unit="D")
    elif kind == "amount_diff":
        # نفس الفاتورة بفرق 0.50 في المبلغ
        c["amount"] = c["amount"] + 0.5
    elif kind == "name_variant":
        # نفس المورد لكن بمسافات وحروف كبيرة
        c["supplier"] = " " + c["supplier"].str.upper() + " "

    copies.append(c)

# الأصل أيضاً يُعلَّم، لأن الزوج كامل تكرار
df.loc[originals.index, "is_duplicate"] = True
df = pd.concat([df] + copies, ignore_index=True)

df.to_csv("invoices.csv", index=False)
print(df.shape, df["is_duplicate"].sum())
