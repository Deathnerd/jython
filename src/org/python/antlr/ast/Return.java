// Autogenerated AST node
package org.python.antlr.ast;
import org.antlr.runtime.CommonToken;
import org.antlr.runtime.Token;
import org.python.antlr.PythonTree;
import org.python.antlr.adapter.AstAdapters;
import org.python.core.AstList;
import org.python.core.Py;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.core.PyType;
import org.python.expose.ExposedGet;
import org.python.expose.ExposedMethod;
import org.python.expose.ExposedNew;
import org.python.expose.ExposedSet;
import org.python.expose.ExposedType;
import java.io.DataOutputStream;
import java.io.IOException;
import java.util.ArrayList;

@ExposedType(name = "_ast.Return", base = PyObject.class)
public class Return extends stmtType {
public static final PyType TYPE = PyType.fromClass(Return.class);
    private exprType value;
    public exprType getInternalValue() {
        return value;
    }
    @ExposedGet(name = "value")
    public PyObject getValue() {
        return value;
    }
    @ExposedSet(name = "value")
    public void setValue(PyObject value) {
        this.value = AstAdapters.py2expr(value);
    }


    private final static String[] fields = new String[] {"value"};
@ExposedGet(name = "_fields")
    public String[] get_fields() { return fields; }

    public Return() {
        this(TYPE);
    }
    public Return(PyType subType) {
        super(subType);
    }
    @ExposedNew
    @ExposedMethod
    public void Module___init__(PyObject[] args, String[] keywords) {}
    public Return(PyObject value) {
        setValue(value);
    }

    public Return(Token token, exprType value) {
        super(token);
        this.value = value;
        addChild(value);
    }

    public Return(Integer ttype, Token token, exprType value) {
        super(ttype, token);
        this.value = value;
        addChild(value);
    }

    public Return(PythonTree tree, exprType value) {
        super(tree);
        this.value = value;
        addChild(value);
    }

    @ExposedGet(name = "repr")
    public String toString() {
        return "Return";
    }

    public String toStringTree() {
        StringBuffer sb = new StringBuffer("Return(");
        sb.append("value=");
        sb.append(dumpThis(value));
        sb.append(",");
        sb.append(")");
        return sb.toString();
    }

    public <R> R accept(VisitorIF<R> visitor) throws Exception {
        return visitor.visitReturn(this);
    }

    public void traverse(VisitorIF visitor) throws Exception {
        if (value != null)
            value.accept(visitor);
    }

    private int lineno = -1;
@ExposedGet(name = "lineno")
    public int getLineno() {
        if (lineno != -1) {
            return lineno;
        }
        return getLine();
    }

@ExposedSet(name = "lineno")
    public void setLineno(int num) {
        lineno = num;
    }

    private int col_offset = -1;
@ExposedGet(name = "col_offset")
    public int getCol_offset() {
        if (col_offset != -1) {
            return col_offset;
        }
        return getCharPositionInLine();
    }

@ExposedSet(name = "col_offset")
    public void setCol_offset(int num) {
        col_offset = num;
    }

}
