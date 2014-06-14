// Autogenerated AST node
package org.python.antlr.ast;
import org.antlr.runtime.CommonToken;
import org.antlr.runtime.Token;
import org.python.antlr.AST;
import org.python.antlr.PythonTree;
import org.python.antlr.adapter.AstAdapters;
import org.python.antlr.base.excepthandler;
import org.python.antlr.base.expr;
import org.python.antlr.base.mod;
import org.python.antlr.base.slice;
import org.python.antlr.base.stmt;
import org.python.core.ArgParser;
import org.python.core.AstList;
import org.python.core.Py;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.core.PyStringMap;
import org.python.core.PyType;
import org.python.expose.ExposedGet;
import org.python.expose.ExposedMethod;
import org.python.expose.ExposedNew;
import org.python.expose.ExposedSet;
import org.python.expose.ExposedType;
import java.io.DataOutputStream;
import java.io.IOException;
import java.util.ArrayList;

@ExposedType(name = "_ast.Raise", base = stmt.class)
public class Raise extends stmt {
public static final PyType TYPE = PyType.fromClass(Raise.class);
    private expr type;
    public expr getInternalType() {
        return type;
    }
    @ExposedGet(name = "type")
    public PyObject getExceptType() {
        return type;
    }
    @ExposedSet(name = "type")
    public void setExceptType(PyObject type) {
        this.type = AstAdapters.py2expr(type);
    }

    private expr inst;
    public expr getInternalInst() {
        return inst;
    }
    @ExposedGet(name = "inst")
    public PyObject getInst() {
        return inst;
    }
    @ExposedSet(name = "inst")
    public void setInst(PyObject inst) {
        this.inst = AstAdapters.py2expr(inst);
    }

    private expr tback;
    public expr getInternalTback() {
        return tback;
    }
    @ExposedGet(name = "tback")
    public PyObject getTback() {
        return tback;
    }
    @ExposedSet(name = "tback")
    public void setTback(PyObject tback) {
        this.tback = AstAdapters.py2expr(tback);
    }


    private final static PyString[] fields =
    new PyString[] {new PyString("type"), new PyString("inst"), new PyString("tback")};
    @ExposedGet(name = "_fields")
    public PyString[] get_fields() { return fields; }

    private final static PyString[] attributes =
    new PyString[] {new PyString("lineno"), new PyString("col_offset")};
    @ExposedGet(name = "_attributes")
    public PyString[] get_attributes() { return attributes; }

    public Raise(PyType subType) {
        super(subType);
    }
    public Raise() {
        this(TYPE);
    }
    @ExposedNew
    @ExposedMethod
    public void Raise___init__(PyObject[] args, String[] keywords) {
        ArgParser ap = new ArgParser("Raise", args, keywords, new String[]
            {"type", "inst", "tback", "lineno", "col_offset"}, 3, true);
        setExceptType(ap.getPyObject(0, Py.None));
        setInst(ap.getPyObject(1, Py.None));
        setTback(ap.getPyObject(2, Py.None));
        int lin = ap.getInt(3, -1);
        if (lin != -1) {
            setLineno(lin);
        }

        int col = ap.getInt(4, -1);
        if (col != -1) {
            setLineno(col);
        }

    }

    public Raise(PyObject type, PyObject inst, PyObject tback) {
        setExceptType(type);
        setInst(inst);
        setTback(tback);
    }

    public Raise(Token token, expr type, expr inst, expr tback) {
        super(token);
        this.type = type;
        addChild(type);
        this.inst = inst;
        addChild(inst);
        this.tback = tback;
        addChild(tback);
    }

    public Raise(Integer ttype, Token token, expr type, expr inst, expr tback) {
        super(ttype, token);
        this.type = type;
        addChild(type);
        this.inst = inst;
        addChild(inst);
        this.tback = tback;
        addChild(tback);
    }

    public Raise(PythonTree tree, expr type, expr inst, expr tback) {
        super(tree);
        this.type = type;
        addChild(type);
        this.inst = inst;
        addChild(inst);
        this.tback = tback;
        addChild(tback);
    }

    @ExposedGet(name = "repr")
    public String toString() {
        return "Raise";
    }

    public String toStringTree() {
        StringBuffer sb = new StringBuffer("Raise(");
        sb.append("type=");
        sb.append(dumpThis(type));
        sb.append(",");
        sb.append("inst=");
        sb.append(dumpThis(inst));
        sb.append(",");
        sb.append("tback=");
        sb.append(dumpThis(tback));
        sb.append(",");
        sb.append(")");
        return sb.toString();
    }

    public <R> R accept(VisitorIF<R> visitor) throws Exception {
        return visitor.visitRaise(this);
    }

    public void traverse(VisitorIF<?> visitor) throws Exception {
        if (type != null)
            type.accept(visitor);
        if (inst != null)
            inst.accept(visitor);
        if (tback != null)
            tback.accept(visitor);
    }

    public PyObject __dict__;

    @Override
    public PyObject fastGetDict() {
        ensureDict();
        return __dict__;
    }

    @ExposedGet(name = "__dict__")
    public PyObject getDict() {
        return fastGetDict();
    }

    private void ensureDict() {
        if (__dict__ == null) {
            __dict__ = new PyStringMap();
        }
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
