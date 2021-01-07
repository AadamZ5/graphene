#https://github.com/graphql-python/graphene/issues/1301

from graphene.types.field import Field, FieldDecorator
from graphene import String, Int, ObjectType, field_property

def test_issue():
    class MyType(ObjectType):
        my_attr1 = String()
        my_attr2 = Int()

        @field_property(type_=String)
        def my_property(self):
            return self._inside_property

        def __init__(self):
            super().__init__()
            self._inside_property = "special"

    mytype_inst = MyType()

    # When referenced by the type and not an instance, the type is returned as FieldDecorator, which inherits from Field.
    assert isinstance(MyType.my_property, FieldDecorator)
    # FieldDecorator inherits from Field
    assert isinstance(MyType.my_property, Field)

    # On an instance, the attribute becomes an actual value.
    assert mytype_inst.my_property == "special"
    # The attribute on an INSTANCE is not able to be detected as FieldDecorator or Field.
    assert isinstance(mytype_inst.my_property, Field) == False
