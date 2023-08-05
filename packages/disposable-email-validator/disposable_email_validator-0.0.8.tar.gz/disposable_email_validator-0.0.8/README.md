# disposable-email-validator

### installation

```
pip install disposable-email-validator
```


### usage

```python
from disposable_email_validator import is_disposable_email

is_disposable_email("some_email@inpwa.com") # True
is_disposable_email("some_email@gmail.com") # False
```


### uploading new fake emails

```text
1) update file /disposable_email_validator/disposable_emails (pickle file)
2) increase version of the package in setup.py
3) upload updated package to pypi
4) change version of the package in backend repo
```