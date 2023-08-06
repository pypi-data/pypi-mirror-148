[GitHub Pages](https://jameskabbes.github.io/analytics_packages)<br>
[PyPI](https://pypi.org/project/kabbes-analytics-packages)

# analytics_packages
Helper functions for generic analysis and iteracting with Excel files

<br> 

# Installation
`pip install kabbes_analytics_packages`

<br>

# Usage
For more in-depth documentation, read the information provided on the Pages. Or better yet, read the source code.

```python
import analytics_packages.custom_xlwings as cxw
```

```python
wb = cxw.get_wb( 'excel_data.xlsx' )
ws = cxw.get_ws( wb, sheet = 'Sheet1' ) 
df = cxw.get_df_from_ws( ws ) #Pandas DataFrame
```

```python
cxw.delete_sheet( ws )
```

```python
import analytics_packages.custom_pandas as cpd
import pandas as pd
```

```
df = pd.DataFrame( {'A': [ 1,2,3 ], 'B': [ 4,5,6 ] } )
df_new = cpd.move_last_column_to_first( df )
print (df_new)
```

```
>>>
   B  A
0  4  1
1  5  2
2  6  3
```


<br>

# Author
James Kabbes
