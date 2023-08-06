from model import model
from fields import FieldType

class t(model):
    a= FieldType(str,"SERVICE.host")
    b= FieldType(str,"SERVICE.name")

if __name__ == "__main__":
    a= t(r"C:\Home\dev\Python\pypi\src\TDhelper\document\ini\1.ini")
    print(a.a)
    print(a.b)