import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000
df = pd.DataFrame({
    "invoice_id": [f"INV-{i:04d}" for i in range(1, n + 1)],
    "supplier": np.random.choice(["Supplier A", "Supplier B", "Supplier C", "Supplier D"], n),
    "amount": np.round(np.random.uniform(100, 20000, n), 2),
    "invoice_date": pd.Timestamp("2026-11-01") + pd.to_timedelta(np.random.randint(0, 30, n), unit="D"),
    "duplicate_of": "",
    "is_duplicate": False,
})

# نختار 30 فاتورة ونعمل لكل واحدة نسخة مكررة
sampled = df.sample(30, random_state=1)
copies = sampled.copy()
copies["invoice_id"] = [f"INV-{i:04d}" for i in range(n + 1, n + 31)]
copies["duplicate_of"] = sampled["invoice_id"].values
copies["is_duplicate"] = True

# الزوج كامل (الأصل + النسخة) يتعلّم كمكرر
df.loc[sampled.index, "is_duplicate"] = True

df = pd.concat([df, copies], ignore_index=True)
df.to_csv("invoices.csv", index=False)
print(df.shape, df["is_duplicate"].sum())
