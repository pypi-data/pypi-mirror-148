'''# PySubversion
## A command-line SVN client wrapper.

Subversion is a tool for version control.
For additional information, see the [github](https://github.com/ryanbender2/pysvn) page.

This client currently supports the `revert`, `log`, `diff`, and `update` operations.
Please put in a feature request if you would like more operations to be added!



### Examples

```python
import pysvn

svn = pysvn.Client()
```

#### revert

* Revert a given path + options...

```python
svn.revert('foo.txt')
```

```python
svn.revert('foo/', recursive=True)
```

```python
svn.revert('foo.txt', remove_added=True)
```

#### log

* Show the log messages for a set of revision(s) and/or path(s)..

```python
svn.log()
```

```python
svn.log(revision=12)
```

```python
svn.log(revision='1:3')
```

```python
svn.log(file='foo.txt', revision=Revision.HEAD)
```

#### diff

* Display local changes or differences between two revisions or paths

```python
svn.diff(1)
```

```python
svn.diff(3, 4)
```

#### update

* Bring changes from the repository into the working copy.

```python
svn.update()
```

```python
svn.update(path='foo.txt')
```

```python
svn.update(path=['foo.txt', 'bar.c'])
```



### Contact

Ryan Bender - [@itsmeryan.hihello](https://www.instagram.com/itsmeryan.hihello/) - [ryan.bender@cfacorp.com](mailto:ryan.bender@cfacorp.com)
'''

from pysvn.client import Client
from pysvn.utils import *
from pysvn.models import *
from pysvn.errors import *
from pysvn.constants import *


name = "pysvn"

__doc__ = """
A Python package that can operate svn, provide log, diff, numstat operation.
"""