# transition module to convert from new types to old types

import vyper.codegen.types as old
import vyper.semantics.types as new
from vyper.exceptions import InvalidType


def new_type_to_old_type(typ: new.BasePrimitive) -> old.NodeType:
    if isinstance(typ, new.BoolDefinition):
        return old.BaseType("bool")
    if isinstance(typ, new.AddressDefinition):
        return old.BaseType("address")
    if isinstance(typ, new.Bytes32Definition):
        return old.BaseType("bytes32")
    if isinstance(typ, new.BytesArrayDefinition):
        return old.ByteArrayType(typ.length)
    if isinstance(typ, new.StringDefinition):
        return old.StringType(typ.length)
    if isinstance(typ, new.DecimalDefinition):
        return old.BaseType("decimal")
    if isinstance(typ, new.SignedIntegerAbstractType):
        bits = typ._bits  # type: ignore
        return old.BaseType("int" + str(bits))
    if isinstance(typ, new.UnsignedIntegerAbstractType):
        bits = typ._bits  # type: ignore
        return old.BaseType("uint" + str(bits))
    if isinstance(typ, new.ArrayDefinition):
        return old.SArrayType(new_type_to_old_type(typ.value_type), typ.length)
    if isinstance(typ, new.DynamicArrayDefinition):
        return old.DArrayType(new_type_to_old_type(typ.value_type), typ.length)
    if isinstance(typ, new.TupleDefinition):
        return old.TupleType(typ.value_type)
    if isinstance(typ, new.StructDefinition):
        return old.StructType(
            {n: new_type_to_old_type(t) for (n, t) in typ.members.items()}, typ._id
        )
    raise InvalidType(f"unknown type {typ}")
