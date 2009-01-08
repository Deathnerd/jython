#! /usr/bin/env python
"""Generate Java code from an ASDL description."""

# TO DO
# handle fields that have a type but no name

import os, sys, traceback

import asdl

TABSIZE = 4
MAX_COL = 100

def reflow_lines(s, depth):
    """Reflow the line s indented depth tabs.

    Return a sequence of lines where no line extends beyond MAX_COL
    when properly indented.  The first line is properly indented based
    exclusively on depth * TABSIZE.  All following lines -- these are
    the reflowed lines generated by this function -- start at the same
    column as the first character beyond the opening { in the first
    line.
    """
    size = MAX_COL - depth * TABSIZE
    if len(s) < size:
        return [s]

    lines = []
    cur = s
    padding = ""
    while len(cur) > size:
        i = cur.rfind(' ', 0, size)
        assert i != -1, "Impossible line to reflow: %s" % `s`
        lines.append(padding + cur[:i])
        if len(lines) == 1:
            # find new size based on brace
            j = cur.find('{', 0, i)
            if j >= 0:
                j += 2 # account for the brace and the space after it
                size -= j
                padding = " " * j
        cur = cur[i+1:]
    else:
        lines.append(padding + cur)
    return lines

class EmitVisitor(asdl.VisitorBase):
    """Visit that emits lines"""

    def __init__(self, dir):
        self.dir = dir
        super(EmitVisitor, self).__init__()

    def open(self, package, name, refersToPythonTree=1, useDataOutput=0):
        path = os.path.join(self.dir, package, "%s.java" % name)
        open(path, "w")
        self.file = open(os.path.join(self.dir, package, "%s.java" % name), "w")
        print >> self.file, "// Autogenerated AST node"
        print >> self.file, 'package org.python.antlr.%s;' % package
        if refersToPythonTree:
            print >> self.file, 'import org.antlr.runtime.CommonToken;'
            print >> self.file, 'import org.antlr.runtime.Token;'
            print >> self.file, 'import org.python.antlr.AST;'
            print >> self.file, 'import org.python.antlr.PythonTree;'
            print >> self.file, 'import org.python.antlr.adapter.AstAdapters;'
            print >> self.file, 'import org.python.antlr.base.excepthandler;'
            print >> self.file, 'import org.python.antlr.base.expr;'
            print >> self.file, 'import org.python.antlr.base.mod;'
            print >> self.file, 'import org.python.antlr.base.slice;'
            print >> self.file, 'import org.python.antlr.base.stmt;'
            print >> self.file, 'import org.python.core.ArgParser;'
            print >> self.file, 'import org.python.core.AstList;'
            print >> self.file, 'import org.python.core.Py;'
            print >> self.file, 'import org.python.core.PyObject;'
            print >> self.file, 'import org.python.core.PyString;'
            print >> self.file, 'import org.python.core.PyType;'
            print >> self.file, 'import org.python.expose.ExposedGet;'
            print >> self.file, 'import org.python.expose.ExposedMethod;'
            print >> self.file, 'import org.python.expose.ExposedNew;'
            print >> self.file, 'import org.python.expose.ExposedSet;'
            print >> self.file, 'import org.python.expose.ExposedType;'

        if useDataOutput:
            print >> self.file, 'import java.io.DataOutputStream;'
            print >> self.file, 'import java.io.IOException;'
            print >> self.file, 'import java.util.ArrayList;'
        print >> self.file
    
    def close(self):
        self.file.close()

    def emit(self, s, depth):
        # XXX reflow long lines?
        lines = reflow_lines(s, depth)
        for line in lines:
            line = (" " * TABSIZE * depth) + line + "\n"
            self.file.write(line)



# This step will add a 'simple' boolean attribute to all Sum and Product 
# nodes and add a 'typedef' link to each Field node that points to the
# Sum or Product node that defines the field.

class AnalyzeVisitor(EmitVisitor):
    index = 0
    def makeIndex(self):
        self.index += 1
        return self.index

    def visitModule(self, mod):
        self.types = {}
        for dfn in mod.dfns:
            self.types[str(dfn.name)] = dfn.value
        for dfn in mod.dfns:
            self.visit(dfn)

    def visitType(self, type, depth=0):
        self.visit(type.value, type.name, depth)

    def visitSum(self, sum, name, depth):
        sum.simple = 1
        for t in sum.types:
            if t.fields:
                sum.simple = 0
                break
        for t in sum.types:
            if not sum.simple:
                t.index = self.makeIndex()
            self.visit(t, name, depth)

    def visitProduct(self, product, name, depth):
        product.simple = 0
        product.index = self.makeIndex()
        for f in product.fields:
            self.visit(f, depth + 1)

    def visitConstructor(self, cons, name, depth):
        for f in cons.fields:
            self.visit(f, depth + 1)

    def visitField(self, field, depth):
        field.typedef = self.types.get(str(field.type))

# The code generator itself.
#
class JavaVisitor(EmitVisitor):
    def visitModule(self, mod):
        for dfn in mod.dfns:
            self.visit(dfn)

    def visitType(self, type, depth=0):
        self.visit(type.value, type.name, depth)

    def visitSum(self, sum, name, depth):
        if sum.simple and not name == "excepthandler":
            self.simple_sum(sum, name, depth)
            self.simple_sum_wrappers(sum, name, depth)
        else:
            self.sum_with_constructor(sum, name, depth)

    def simple_sum(self, sum, name, depth):
        self.open("ast", "%sType" % name, refersToPythonTree=0)
        self.emit('import org.python.antlr.AST;', depth)
        self.emit('', 0)

        self.emit("public enum %(name)sType {" % locals(), depth)
        self.emit("UNDEFINED,", depth + 1)
        for i in range(len(sum.types) - 1):
            type = sum.types[i]
            self.emit("%s," % type.name, depth + 1)
        self.emit("%s;" % sum.types[len(sum.types) - 1].name, depth + 1)

        self.emit("}", depth)
        self.close()

    def simple_sum_wrappers(self, sum, name, depth):
        for i in range(len(sum.types)):
            type = sum.types[i]
            self.open("op", type.name, refersToPythonTree=0)
            self.emit('import org.python.antlr.AST;', depth)
            self.emit('import org.python.antlr.PythonTree;', depth)
            self.emit('import org.python.core.Py;', depth)
            self.emit('import org.python.core.PyObject;', depth)
            self.emit('import org.python.core.PyString;', depth)
            self.emit('import org.python.core.PyType;', depth)
            self.emit('import org.python.expose.ExposedGet;', depth)
            self.emit('import org.python.expose.ExposedMethod;', depth)
            self.emit('import org.python.expose.ExposedNew;', depth)
            self.emit('import org.python.expose.ExposedSet;', depth)
            self.emit('import org.python.expose.ExposedType;', depth)
            self.emit('', 0)

            self.emit('@ExposedType(name = "_ast.%s", base = AST.class)' % type.name, depth)
            self.emit("public class %s extends PythonTree {" % type.name, depth)
            self.emit('public static final PyType TYPE = PyType.fromClass(%s.class);' % type.name, depth + 1)
            self.emit('', 0)

            self.emit("public %s() {" % (type.name), depth)
            self.emit("}", depth)
            self.emit('', 0)

            self.emit("public %s(PyType subType) {" % (type.name), depth)
            self.emit("super(subType);", depth + 1)
            self.emit("}", depth)
            self.emit('', 0)

            self.emit("@ExposedNew", depth)
            self.emit("@ExposedMethod", depth)
            self.emit("public void %s___init__(PyObject[] args, String[] keywords) {}" % type.name, depth)
            self.emit('', 0)

            self.attributes(type, name, depth);

            self.emit('@ExposedMethod', depth + 1)
            self.emit('public PyObject __int__() {', depth + 1)
            self.emit("return %s___int__();" % type.name, depth + 2)
            self.emit("}", depth + 1)
            self.emit('', 0)

            self.emit("final PyObject %s___int__() {" % type.name, depth + 1)
            self.emit('return Py.newInteger(%s);' % str(i + 1), depth + 2)
            self.emit("}", depth + 1)
            self.emit('', 0)

            self.emit("}", depth)
            self.close()


    def attributes(self, obj, name, depth):
        field_list = []
        if hasattr(obj, "fields"):
            for f in obj.fields:
                field_list.append('new PyString("%s")' % f.name)
        if len(field_list) > 0:
            self.emit("private final static PyString[] fields =", depth + 1)
            self.emit("new PyString[] {%s};" % ", ".join(field_list), depth+1)
            self.emit('@ExposedGet(name = "_fields")', depth + 1)
            self.emit("public PyString[] get_fields() { return fields; }", depth+1)
            self.emit("", 0)
        else:
            self.emit("private final static PyString[] fields = new PyString[0];", depth+1)
            self.emit('@ExposedGet(name = "_fields")', depth + 1)
            self.emit("public PyString[] get_fields() { return fields; }", depth+1)
            self.emit("", 0)

        if str(name) in ('stmt', 'expr', 'excepthandler'):
            att_list = ['new PyString("lineno")', 'new PyString("col_offset")']
            self.emit("private final static PyString[] attributes =", depth + 1)
            self.emit("new PyString[] {%s};" % ", ".join(att_list), depth + 1)
            self.emit('@ExposedGet(name = "_attributes")', depth + 1)
            self.emit("public PyString[] get_attributes() { return attributes; }", depth + 1)
            self.emit("", 0)
        else:
            self.emit("private final static PyString[] attributes = new PyString[0];", depth+1)
            self.emit('@ExposedGet(name = "_attributes")', depth + 1)
            self.emit("public PyString[] get_attributes() { return attributes; }", depth+1)
            self.emit("", 0)
   
    def sum_with_constructor(self, sum, name, depth):
        self.open("base", "%s" % name)

        self.emit('@ExposedType(name = "_ast.%s", base = AST.class)' % name, depth)
        self.emit("public abstract class %(name)s extends PythonTree {" %
                    locals(), depth)
        self.emit("", 0)
        self.emit("public static final PyType TYPE = PyType.fromClass(%s.class);" % name, depth + 1);

        self.attributes(sum, name, depth);

        self.emit("public %(name)s() {" % locals(), depth+1)
        self.emit("}", depth+1)
        self.emit("", 0)

        self.emit("public %(name)s(PyType subType) {" % locals(), depth+1)
        self.emit("}", depth+1)
        self.emit("", 0)

        self.emit("public %(name)s(int ttype, Token token) {" % locals(), depth+1)
        self.emit("super(ttype, token);", depth+2)
        self.emit("}", depth+1)
        self.emit("", 0)

        self.emit("public %(name)s(Token token) {" % locals(), depth+1)
        self.emit("super(token);", depth+2)
        self.emit("}", depth+1)
        self.emit("", 0)

        self.emit("public %(name)s(PythonTree node) {" % locals(), depth+1)
        self.emit("super(node);", depth+2)
        self.emit("}", depth+1)
        self.emit("", 0)

        self.emit("}", depth)
        self.close()
        for t in sum.types:
            self.visit(t, name, depth)

    def visitProduct(self, product, name, depth):

        self.open("ast", "%s" % name, useDataOutput=1)
        self.emit('@ExposedType(name = "_ast.%s", base = AST.class)' % name, depth)
        self.emit("public class %(name)s extends PythonTree {" % locals(), depth)
        self.emit("public static final PyType TYPE = PyType.fromClass(%s.class);" % name, depth + 1);
        for f in product.fields:
            self.visit(f, depth + 1)
        self.emit("", depth)

        self.attributes(product, name, depth)

        self.javaMethods(product, name, name, True, product.fields,
                         depth+1)

        self.emit("}", depth)
        self.close()

    def visitConstructor(self, cons, name, depth):
        self.open("ast", cons.name, useDataOutput=1)
        ifaces = []
        for f in cons.fields:
            if str(f.type) == "expr_context":
                ifaces.append("Context")
        if ifaces:
            s = "implements %s " % ", ".join(ifaces)
        else:
            s = ""
        self.emit('@ExposedType(name = "_ast.%s", base = AST.class)' % cons.name, depth);
        self.emit("public class %s extends %s %s{" %
                    (cons.name, name, s), depth)
        self.emit("public static final PyType TYPE = PyType.fromClass(%s.class);" % cons.name, depth);
        for f in cons.fields:
            self.visit(f, depth + 1)
        self.emit("", depth)

        self.attributes(cons, name, depth)

        self.javaMethods(cons, name, cons.name, False, cons.fields, depth+1)

        if "Context" in ifaces:
            self.emit("public void setContext(expr_contextType c) {", depth + 1)
            self.emit('this.ctx = c;', depth + 2)
            self.emit("}", depth + 1)
            self.emit("", 0)

        if str(name) in ('stmt', 'expr', 'excepthandler'):
            # The lineno property
            self.emit("private int lineno = -1;", depth + 1)
            self.emit('@ExposedGet(name = "lineno")', depth + 1)
            self.emit("public int getLineno() {", depth + 1)
            self.emit("if (lineno != -1) {", depth + 2);
            self.emit("return lineno;", depth + 3);
            self.emit("}", depth + 2)
            self.emit('return getLine();', depth + 2)
            self.emit("}", depth + 1)
            self.emit("", 0)
            self.emit('@ExposedSet(name = "lineno")', depth + 1)
            self.emit("public void setLineno(int num) {", depth + 1)
            self.emit("lineno = num;", depth + 2);
            self.emit("}", depth + 1)
            self.emit("", 0)

            # The col_offset property
            self.emit("private int col_offset = -1;", depth + 1)
            self.emit('@ExposedGet(name = "col_offset")', depth + 1)
            self.emit("public int getCol_offset() {", depth + 1)
            self.emit("if (col_offset != -1) {", depth + 2);
            self.emit("return col_offset;", depth + 3);
            self.emit("}", depth + 2)
            self.emit('return getCharPositionInLine();', depth + 2)
            self.emit("}", depth + 1)
            self.emit("", 0)
            self.emit('@ExposedSet(name = "col_offset")', depth + 1)
            self.emit("public void setCol_offset(int num) {", depth + 1)
            self.emit("col_offset = num;", depth + 2);
            self.emit("}", depth + 1)
            self.emit("", 0)


        self.emit("}", depth)
        self.close()

    def javaConstructorHelper(self, fields, depth):
        for f in fields:
            #if f.seq:
            #    self.emit("this.%s = new %s(%s);" % (f.name,
            #        self.javaType(f), f.name), depth+1)
            #else:
            self.emit("this.%s = %s;" % (f.name, f.name), depth+1)

            fparg = self.fieldDef(f)

            not_simple = True
            if f.typedef is not None and f.typedef.simple:
                not_simple = False
            #For now ignoring String -- will want to revisit
            if not_simple and fparg.find("String") == -1:
                if f.seq:
                    self.emit("if (%s == null) {" % f.name, depth+1);
                    self.emit("this.%s = new ArrayList<%s>();" % (f.name, self.javaType(f, False)), depth+2)
                    self.emit("}", depth+1)
                    self.emit("for(PythonTree t : this.%(name)s) {" % {"name":f.name}, depth+1)
                    self.emit("addChild(t);", depth+2)
                    self.emit("}", depth+1)
                elif str(f.type) == "expr":
                    self.emit("addChild(%s);" % (f.name), depth+1)

    #XXX: this method used to emit a pickle(DataOutputStream ostream) for cPickle support.
    #     If we want to re-add it, see Jython 2.2's pickle method in its ast nodes.
    def javaMethods(self, type, name, clsname, is_product, fields, depth):

        self.javaConstructors(type, name, clsname, is_product, fields, depth)

        # The toString() method
        self.emit('@ExposedGet(name = "repr")', depth)
        self.emit("public String toString() {", depth)
        self.emit('return "%s";' % clsname, depth+1)
        self.emit("}", depth)
        self.emit("", 0)

        # The toStringTree() method
        self.emit("public String toStringTree() {", depth)
        self.emit('StringBuffer sb = new StringBuffer("%s(");' % clsname,
                    depth+1)
        for f in fields:
            self.emit('sb.append("%s=");' % f.name, depth+1)
            self.emit("sb.append(dumpThis(%s));" % f.name, depth+1)
            self.emit('sb.append(",");', depth+1)
        self.emit('sb.append(")");', depth+1)
        self.emit("return sb.toString();", depth+1)
        self.emit("}", depth)
        self.emit("", 0)

        # The accept() method
        self.emit("public <R> R accept(VisitorIF<R> visitor) throws Exception {", depth)
        if is_product:
            self.emit('traverse(visitor);' % clsname, depth+1)
            self.emit('return null;' % clsname, depth+1)
        else:
            self.emit('return visitor.visit%s(this);' % clsname, depth+1)
        self.emit("}", depth)
        self.emit("", 0)

        # The visitChildren() method
        self.emit("public void traverse(VisitorIF visitor) throws Exception {", depth)
        for f in fields:
            if self.bltinnames.has_key(str(f.type)):
                continue
            if f.typedef.simple:
                continue
            if f.seq:
                self.emit('if (%s != null) {' % f.name, depth+1)
                self.emit('for (PythonTree t : %s) {' % f.name,
                        depth+2)
                self.emit('if (t != null)', depth+3)
                self.emit('t.accept(visitor);', depth+4)
                self.emit('}', depth+2)
                self.emit('}', depth+1)
            else:
                self.emit('if (%s != null)' % f.name, depth+1)
                self.emit('%s.accept(visitor);' % f.name, depth+2)
        self.emit('}', depth)
        self.emit("", 0)

    def javaConstructors(self, type, name, clsname, is_product, fields, depth):
        self.emit("public %s(PyType subType) {" % (clsname), depth)
        self.emit("super(subType);", depth + 1)
        self.emit("}", depth)

        if len(fields) > 0:
            self.emit("public %s() {" % (clsname), depth)
            self.emit("this(TYPE);", depth + 1)
            self.emit("}", depth)
            fnames = ['"%s"' % f.name for f in fields]
        else:
            fnames = []

        if str(name) in ('stmt', 'expr', 'excepthandler'):
            fnames.extend(['"lineno"', '"col_offset"'])
        fpargs = ", ".join(fnames)
        self.emit("@ExposedNew", depth)
        self.emit("@ExposedMethod", depth)
        self.emit("public void %s___init__(PyObject[] args, String[] keywords) {" % clsname, depth)
        self.emit('ArgParser ap = new ArgParser("%s", args, keywords, new String[]' % clsname, depth + 1)
        self.emit('{%s}, %s);' % (fpargs, len(fields)), depth + 2)
        i = 0
        for f in fields:
            self.emit("set%s(ap.getPyObject(%s));" % (self.processFieldName(f.name),
                str(i)), depth+1)
            i += 1
        if str(name) in ('stmt', 'expr', 'excepthandler'):
            self.emit("int lin = ap.getInt(%s, -1);" % str(i), depth + 1) 
            self.emit("if (lin != -1) {", depth + 1) 
            self.emit("setLineno(lin);", depth + 2) 
            self.emit("}", depth + 1)
            self.emit("", 0)

            self.emit("int col = ap.getInt(%s, -1);" % str(i+1), depth + 1) 
            self.emit("if (col != -1) {", depth + 1) 
            self.emit("setLineno(col);", depth + 2) 
            self.emit("}", depth + 1)
            self.emit("", 0)

        self.emit("}", depth)
        self.emit("", 0)

        fpargs = ", ".join(["PyObject %s" % f.name for f in fields])
        self.emit("public %s(%s) {" % (clsname, fpargs), depth)
        for f in fields:
            self.emit("set%s(%s);" % (self.processFieldName(f.name), f.name), depth+1)
        self.emit("}", depth)
        self.emit("", 0)

        token = asdl.Field('Token', 'token')
        token.typedef = False
        fpargs = ", ".join([self.fieldDef(f) for f in [token] + fields])
        self.emit("public %s(%s) {" % (clsname, fpargs), depth)
        self.emit("super(token);", depth+1)
        self.javaConstructorHelper(fields, depth)
        self.emit("}", depth)
        self.emit("", 0)

        ttype = asdl.Field('int', 'ttype')
        ttype.typedef = False
        fpargs = ", ".join([self.fieldDef(f) for f in [ttype, token] + fields])
        self.emit("public %s(%s) {" % (clsname, fpargs), depth)
        self.emit("super(ttype, token);", depth+1)
        self.javaConstructorHelper(fields, depth)
        self.emit("}", depth)
        self.emit("", 0)

        tree = asdl.Field('PythonTree', 'tree')
        tree.typedef = False
        fpargs = ", ".join([self.fieldDef(f) for f in [tree] + fields])
        self.emit("public %s(%s) {" % (clsname, fpargs), depth)
        self.emit("super(tree);", depth+1)
        self.javaConstructorHelper(fields, depth)
        self.emit("}", depth)
        self.emit("", 0)


    #This is mainly a kludge to turn get/setType -> get/setExceptType because
    #getType conflicts with a method on PyObject.
    def processFieldName(self, name):
        name = str(name).capitalize()
        if name == "Type":
            name = "ExceptType"
        return name

    def visitField(self, field, depth):
        self.emit("private %s;" % self.fieldDef(field), depth)
        self.emit("public %s getInternal%s() {" % (self.javaType(field),
            str(field.name).capitalize()), depth)
        self.emit("return %s;" % field.name, depth+1)
        self.emit("}", depth)
        self.emit('@ExposedGet(name = "%s")' % field.name, depth)
        self.emit("public PyObject get%s() {" % self.processFieldName(field.name), depth)
        if field.seq:
            self.emit("return new AstList(%s, AstAdapters.%sAdapter);" % (field.name, field.type), depth+1)
        else:
            if str(field.type) == 'identifier':
                self.emit("if (%s == null) return Py.None;" % field.name, depth+1)
                self.emit("return new PyString(%s);" % field.name, depth+1)
            elif str(field.type) == 'string' or str(field.type) == 'object':
                self.emit("return (PyObject)%s;" % field.name, depth+1)
            elif str(field.type) == 'bool':
                self.emit("if (%s) return Py.True;" % field.name, depth+1)
                self.emit("return Py.False;" % field.name, depth+1)
            elif str(field.type) == 'int':
                self.emit("return Py.newInteger(%s);" % field.name, depth+1)
            elif field.typedef.simple:
                self.emit("return AstAdapters.%s2py(%s);" % (str(field.type), field.name), depth+1)
            else:
                self.emit("return %s;" % field.name, depth+1)
            #self.emit("return Py.None;", depth+1)
        self.emit("}", depth)
        self.emit('@ExposedSet(name = "%s")' % field.name, depth)
        self.emit("public void set%s(PyObject %s) {" % (self.processFieldName(field.name), field.name), depth)
        if field.seq:
            #self.emit("this.%s = new %s(" % (field.name, self.javaType(field)), depth+1)
            self.emit("this.%s = AstAdapters.py2%sList(%s);" % (field.name, str(field.type), field.name), depth+1)
        else:
            self.emit("this.%s = AstAdapters.py2%s(%s);" % (field.name, str(field.type), field.name), depth+1)
        self.emit("}", depth)
        self.emit("", 0)

    bltinnames = {
        'int' : 'Integer',
        'bool' : 'Boolean',
        'identifier' : 'String',
        'string' : 'Object',
        'object' : 'Object', # was PyObject

        #Below are for enums
        'boolop' : 'boolopType',
        'cmpop' : 'cmpopType',
        'expr_context' : 'expr_contextType',
        'operator' : 'operatorType',
        'unaryop' : 'unaryopType',
    }

    def fieldDef(self, field):
        jtype = self.javaType(field)
        name = field.name
        return "%s %s" % (jtype, name)

    def javaType(self, field, check_seq=True):
        jtype = str(field.type)
        jtype = self.bltinnames.get(jtype, jtype)
        if check_seq and field.seq:
            return "java.util.List<%s>" % jtype
        return jtype

class VisitorVisitor(EmitVisitor):
    def __init__(self, dir):
        EmitVisitor.__init__(self, dir)
        self.ctors = []

    def visitModule(self, mod):
        for dfn in mod.dfns:
            self.visit(dfn)
        self.open("ast", "VisitorIF", refersToPythonTree=0)
        self.emit('public interface VisitorIF<R> {', 0)
        for ctor in self.ctors:
            self.emit("public R visit%s(%s node) throws Exception;" % 
                    (ctor, ctor), 1)
        self.emit('}', 0)
        self.close()

        self.open("ast", "VisitorBase")
        self.emit('public abstract class VisitorBase<R> implements VisitorIF<R> {', 0)
        for ctor in self.ctors:
            self.emit("public R visit%s(%s node) throws Exception {" % 
                    (ctor, ctor), 1)
            self.emit("R ret = unhandled_node(node);", 2)
            self.emit("traverse(node);", 2)
            self.emit("return ret;", 2)
            self.emit('}', 1)
            self.emit('', 0)

        self.emit("abstract protected R unhandled_node(PythonTree node) throws Exception;", 1)
        self.emit("abstract public void traverse(PythonTree node) throws Exception;", 1)
        self.emit('}', 0)
        self.close()

    def visitType(self, type, depth=1):
        self.visit(type.value, type.name, depth)

    def visitSum(self, sum, name, depth):
        if not sum.simple:
            for t in sum.types:
                self.visit(t, name, depth)

    def visitProduct(self, product, name, depth):
        pass

    def visitConstructor(self, cons, name, depth):
        self.ctors.append(cons.name)

class ChainOfVisitors:
    def __init__(self, *visitors):
        self.visitors = visitors

    def visit(self, object):
        for v in self.visitors:
            v.visit(object)

def main(outdir, grammar="Python.asdl"):
    mod = asdl.parse(grammar)
    if not asdl.check(mod):
        sys.exit(1)
    c = ChainOfVisitors(AnalyzeVisitor(outdir),
                        JavaVisitor(outdir),
                        VisitorVisitor(outdir))
    c.visit(mod)

if __name__ == "__main__":
    import sys
    import getopt

    usage = "Usage: python %s [-o outdir] [grammar]" % sys.argv[0]

    OUT_DIR = '../src/org/python/antlr/'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'o:')
    except:
       print usage
       sys.exit(1)
    for o, v in opts:
        if o == '-o' and v != '':
            OUT_DIR = v
    if len(opts) > 1 or len(args) > 1:
        print usage
        sys.exit(1)
    if len(args) == 1:
        main(OUT_DIR, args[0])
    else:
        main(OUT_DIR)

