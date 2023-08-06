[GitHub Pages](https://jameskabbes.github.io/database_connections)<br>
[PyPI](https://pypi.org/project/kabbes-database-connections)

# database_connections
Provides database-agnostic connection tools

<br> 

# Installation
`pip install kabbes_database_connections`

<br>

# Usage
For more in-depth documentation, read the information provided on the Pages. Or better yet, read the source code.

```python
import database_connections as dbconn
from database_connections import sql_support_functions as ssf
```

```python
sqlite_conn = sff.get_DatabaseConnection( connection_module = 'sqlite', db_path = 'test.db' )
```

```python
df = sqlite_conn.query( 'Select * from table_name' )
```

```python
sqlite_conn.write( df, 'new_table' )
```

<br>

# Author
James Kabbes
