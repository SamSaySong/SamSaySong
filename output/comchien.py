from neww_student import com_chien
import pandas as pd
import numpy as np

index = pd.date_range("1/1/2000", periods=8)

# s = pd.Series(np.random.randn(5), index=["a", "b", "c", "d", "e"])
# print(s.head())
# print(s.tail())

df = pd.DataFrame(np.random.randn(8, 3), index=index, columns=["A", "B", "C"])
print(pd.DataFrame.to_numpy(df["B"]))