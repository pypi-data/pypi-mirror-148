## FP ARITHMATIC LIBRARY (*version = 0.1.0*)
This is my *first* python library to test and publish python package on PyPI.  
It includes three arithmatic functions as follows:
- add -> adds two numbers
- mul -> multiplies two numbers
- dot -> returns dot (inner) product of two vectors (lists)

### INSTALLATION
```
pip install fp-arithmatic
```

### GET STARTED
How to take dot products of two vectors using this library

```python
import fp_arithmatic as fpa
x = [1,2,3]
y = [2, 3, 5]
result = fpa.dot(x,y)
print(result)
```