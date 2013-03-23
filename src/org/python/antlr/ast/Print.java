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
import org.python.core.PyType;
import org.python.expose.ExposedGet;
import org.python.expose.ExposedMethod;
import org.python.expose.ExposedNew;
import org.python.expose.ExposedSet;
import org.python.expose.ExposedType;
import java.io.DataOutputStream;
import java.io.IOException;
import java.util.ArrayList;

@ExposedType(name = "_ast.Print", base = AST.class)
public class Print extends stmt {
public static final PyType TYPE = PyType.fromClass(Print.class);
    private expr dest;
    public expr getInternalDest() {
        return dest;
    }
    @ExposedGet(name = "dest")
    public PyObject getDest() {
        return dest;
    }
    @ExposedSet(name = "dest")
    public void setDest(PyObject dest) {
        this.dest = AstAdapters.py2expr(dest);
    }

    private java.util.List<expr> values;
    public java.util.List<expr> getInternalValues() {
        return values;
    }
    @ExposedGet(name = "values")
    public PyObject getValues() {
        return new AstList(values, AstAdapters.exprAdapter);
    }
    @ExposedSet(name = "values")
    public void setValues(PyObject values) {
        this.values = AstAdapters.py2exprList(values);
    }

    private Boolean nl;
    public Boolean getInternalNl() {
        return nl;
    }
    @ExposedGet(name = "nl")
    public PyObject getNl() {
        if (nl) return Py.True;
        return Py.False;
    }
    @ExposedSet(name = "nl")
    public void setNl(PyObject nl) {
        this.nl = AstAdapters.py2bool(nl);
    }


    private final static PyString[] fields =
    new PyString[] {new PyString("dest"), new PyString("values"), new PyString("nl")};
    @ExposedGet(name = "_fields")
    public PyString[] get_fields() { return fields; }

    private final static PyString[] attributes =
    new PyString[] {new PyString("lineno"), new PyString("col_offset")};
    @ExposedGet(name = "_attributes")
    public PyString[] get_attributes() { return attributes; }

    public Print(PyType subType) {
        super(subType);
    }
    public Print() {
        this(TYPE);
    }
    @ExposedNew
    @ExposedMethod
    public void Print___init__(PyObject[] args, String[] keywords) {
        ArgParser ap = new ArgParser("Print", args, keywords, new String[]
            {"dest", "values", "nl", "lineno", "col_offset"}, 3, true);
        setDest(ap.getPyObject(0, Py.None));
        setValues(ap.getPyObject(1, Py.None));
        setNl(ap.getPyObject(2, Py.None));
        int lin = ap.getInt(3, -1);
        if (lin != -1) {
            setLineno(lin);
        }

        int col = ap.getInt(4, -1);
        if (col != -1) {
            setLineno(col);
        }

    }

    public Print(PyObject dest, PyObject values, PyObject nl) {
        setDest(dest);
        setValues(values);
        setNl(nl);
    }

    public Print(Token token, expr dest, java.util.List<expr> values, Boolean nl) {
        super(token);
        this.dest = dest;
        addChild(dest);
        this.values = values;
        if (values == null) {
            this.values = new ArrayList<expr>();
        }
        for(PythonTree t : this.values) {
            addChild(t);
        }
        this.nl = nl;
    }

    public Print(Integer ttype, Token token, expr dest, java.util.List<expr> values, Boolean nl) {
        super(ttype, token);
        this.dest = dest;
        addChild(dest);
        this.values = values;
        if (values == null) {
            this.values = new ArrayList<expr>();
        }
        for(PythonTree t : this.values) {
            addChild(t);
        }
        this.nl = nl;
    }

    public Print(PythonTree tree, expr dest, java.util.List<expr> values, Boolean nl) {
        super(tree);
        this.dest = dest;
        addChild(dest);
        this.values = values;
        if (values == null) {
            this.values = new ArrayList<expr>();
        }
        for(PythonTree t : this.values) {
            addChild(t);
        }
        this.nl = nl;
    }

    @ExposedGet(name = "repr")
    public String toString() {
        return "Print";
    }

    public String toStringTree() {
        StringBuffer sb = new StringBuffer("Print(");
        sb.append("dest=");
        sb.append(dumpThis(dest));
        sb.append(",");
        sb.append("values=");
        sb.append(dumpThis(values));
        sb.append(",");
        sb.append("nl=");
        sb.append(dumpThis(nl));
        sb.append(",");
        sb.append(")");
        return sb.toString();
    }

    public <R> R accept(VisitorIF<R> visitor) throws Exception {
        return visitor.visitPrint(this);
    }

    public void traverse(VisitorIF<?> visitor) throws Exception {
        if (dest != null)
            dest.accept(visitor);
        if (values != null) {
            for (PythonTree t : values) {
                if (t != null)
                    t.accept(visitor);
            }
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
