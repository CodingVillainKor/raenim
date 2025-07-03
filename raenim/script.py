from manim import *
from .utils import MONO_FONT
from manim import __version__ as MANIM_VERSION
from .mobject import SurroundingRect
import ast
import sys

__all__ = ["PythonCode"]

class ExecutionTracer:
    """Trace Python code execution line by line"""
    def __init__(self, code_string, filename="<string>"):
        self.code_string = code_string
        self.filename = filename
        self.execution_order = []
        self.namespace = {}
        
    def trace_execution(self):
        """Execute the code with tracing to capture line execution order"""
        # Compile the code
        try:
            compiled_code = compile(self.code_string, self.filename, 'exec')
        except SyntaxError:
            return []
        
        # Set up the trace function
        def trace_func(frame, event, arg):
            if event == 'line':
                # Get the line number in the original file
                line_no = frame.f_lineno
                self.execution_order.append(line_no)
            return trace_func
        
        # Execute with tracing
        old_trace = sys.gettrace()
        sys.settrace(trace_func)
        try:
            exec(compiled_code, self.namespace)
        except Exception:
            # Ignore execution errors for visualization purposes
            pass
        finally:
            sys.settrace(old_trace)
        
        return self.execution_order

class ASTExecutionSimulator:
    """Simulate Python code execution based on AST analysis"""
    def __init__(self, ast_tree, code_lines):
        self.ast_tree = ast_tree
        self.code_lines = code_lines
        self.execution_order = []
        
    def simulate(self, max_iterations=100):
        """Simulate execution and return line numbers in execution order"""
        self.execution_order = []
        self._visit_block(self.ast_tree.body, max_iterations)
        return self.execution_order
    
    def _visit_block(self, statements, max_iterations):
        """Visit a block of statements"""
        for stmt in statements:
            self._visit_statement(stmt, max_iterations)
    
    def _visit_statement(self, node, max_iterations):
        """Visit a single statement and record its execution"""
        if not hasattr(node, 'lineno'):
            return
            
        if isinstance(node, ast.FunctionDef):
            # Record function definition but don't execute body
            self.execution_order.append(node.lineno)
            
        elif isinstance(node, ast.ClassDef):
            # Record class definition
            self.execution_order.append(node.lineno)
            # Execute class body statements (but not methods)
            for stmt in node.body:
                if not isinstance(stmt, ast.FunctionDef):
                    self._visit_statement(stmt, max_iterations)
                    
        elif isinstance(node, ast.If):
            # Record the if statement
            self.execution_order.append(node.lineno)
            # Simulate visiting both branches (for visualization)
            # First the if body
            self._visit_block(node.body, max_iterations)
            # Then the else body
            if node.orelse:
                if isinstance(node.orelse[0], ast.If) and hasattr(node.orelse[0], 'lineno'):
                    # This is an elif
                    self._visit_statement(node.orelse[0], max_iterations)
                else:
                    # This is an else block
                    self._visit_block(node.orelse, max_iterations)
                    
        elif isinstance(node, ast.For):
            # Record the for statement line
            self.execution_order.append(node.lineno)
            # Simulate loop iterations (simplified: 3 iterations)
            iterations = min(3, max_iterations)
            for _ in range(iterations):
                self._visit_block(node.body, max_iterations)
                # After each iteration, record returning to loop header
                if _ < iterations - 1:
                    self.execution_order.append(node.lineno)
            # Visit else clause if exists
            if node.orelse:
                self._visit_block(node.orelse, max_iterations)
                
        elif isinstance(node, ast.While):
            # Record the while statement line
            self.execution_order.append(node.lineno)
            # Simulate loop iterations (simplified: 3 iterations)
            iterations = min(3, max_iterations)
            for _ in range(iterations):
                self._visit_block(node.body, max_iterations)
                # After each iteration, record returning to loop header
                if _ < iterations - 1:
                    self.execution_order.append(node.lineno)
            # Visit else clause if exists
            if node.orelse:
                self._visit_block(node.orelse, max_iterations)
                
        elif isinstance(node, ast.With):
            # Record the with statement
            self.execution_order.append(node.lineno)
            # Visit the body
            self._visit_block(node.body, max_iterations)
            
        elif isinstance(node, ast.Try):
            # Record the try statement
            self.execution_order.append(node.lineno)
            # Visit try body
            self._visit_block(node.body, max_iterations)
            # For visualization, also show except blocks
            for handler in node.handlers:
                if hasattr(handler, 'lineno'):
                    self.execution_order.append(handler.lineno)
                self._visit_block(handler.body, max_iterations)
            # Visit else and finally
            if node.orelse:
                self._visit_block(node.orelse, max_iterations)
            if node.finalbody:
                self._visit_block(node.finalbody, max_iterations)
                
        else:
            # For all other executable statements
            if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign,
                               ast.Expr, ast.Return, ast.Raise, ast.Assert,
                               ast.Delete, ast.Pass, ast.Break, ast.Continue,
                               ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal)):
                self.execution_order.append(node.lineno)

class PythonCode(Code):
    def __init__(self, filename, **kwargs):
        kwargs["tab_width"] = kwargs.pop("tab_width", 4)
        kwargs["language"] = kwargs.pop("language", "python")
        kwargs["add_line_numbers"] = kwargs.pop("add_line_numbers", False)
        kwargs.pop("background", "window")
        paragraph_config = {
            "line_spacing": kwargs.pop("line_spacing", 1.0),
            "font": kwargs.pop("font", MONO_FONT)
        }
        super().__init__(filename, paragraph_config=paragraph_config, **kwargs)
        self.frame.set_opacity(0.3)
        with open(filename, "r") as f:
            self.code_string = f.read()
        self.indentation_chars = kwargs.get("indentation_chars", "    ")

        try:
            self.ast_tree = ast.parse(self.code_string, filename=filename)
        except SyntaxError as e:
            print(f"Warning: Could not parse {filename}: {e}")
            self.ast_tree = None
        self.filename = filename

    @property
    def frame(self):
        return self[:-1]
    
    @property
    def script(self):
        return self.code_lines
    
    @property
    def code(self):
        return self.code_lines
    
    def find_text(self, line_no:int, text:str, nth:int=1):
        lines = self.code_string.split("\n")
        line = lines[line_no-1]
        try:
            idx = _find_multiple(line, text)[nth-1]
        except IndexError:
            raise IndexError(f"Cannot find {nth}th {text} at line {line_no}: {line}")
        ver1, ver2, *_ = MANIM_VERSION.split(".")
        if int(ver1) < 1 and int(ver2) < 19:
            indentation_level = _count_indentation(line)
            idx -= (len(self.indentation_chars)-1) * indentation_level
        return idx, idx+len(text)
    
    def text_slice(self, line_no:int, text:str, nth:int=1, exclusive=False) -> Mobject:
        idx_start, idx_end = self.find_text(line_no, text, nth)
        if exclusive:
            return VGroup(self.code[line_no-1][:idx_start], self.code[line_no-1][idx_end:])
        else:
            return self.code[line_no-1][idx_start:idx_end]
    
    def highlight(self, line_no:int, text:str=None, nth:int=1, 
                  anim=Write, color="#FFFF00", anim_out=FadeOut):
        if text is None:
            target = self.code[line_no-1].copy().set_color(color)
        else:
            target = self.text_slice(line_no, text, nth).copy().set_color(color)
        return anim(target), anim_out(target)

    def _executing_generator(self, use_tracer=False, max_loop_iterations=3):
        """
        Generator that yields the next line number to be executed.
        
        Args:
            use_tracer: If True, actually execute the code with tracing (requires safe code)
            max_loop_iterations: Maximum number of iterations to simulate for loops
        """
        if self.ast_tree is None:
            # If AST parsing failed, just yield lines sequentially
            for i in range(1, len(self.code_lines) + 1):
                yield i
            return
        
        if use_tracer:
            # Use actual execution tracing (be careful with untrusted code!)
            tracer = ExecutionTracer(self.code_string, self.filename)
            execution_order = tracer.trace_execution()
        else:
            # Use AST-based simulation
            simulator = ASTExecutionSimulator(self.ast_tree, self.code_lines)
            execution_order = simulator.simulate(max_iterations=max_loop_iterations)
        
        # Yield line numbers in execution order
        for line_no in execution_order:
            if 1 <= line_no <= len(self.code_lines):
                yield line_no

    def exec(self, with_line_no=False, use_tracer=False):
        lines = list(self._executing_generator(use_tracer=use_tracer))
        anims = []
        for line in lines:
            box = SurroundingRect(stroke_width=0, color=GREEN, fill_color=GREEN, fill_opacity=0.8).set_z_index(1)
            real_code = VGroup(*[c for c in self.code[line-1] if isinstance(c, VMobjectFromSVGPath)])
            box.surround(real_code, buff_h=0.1, buff_w=0.1)

            if with_line_no:
                anims.append((FadeOut(box), line))
            else:
                anims.append(FadeOut(box))
        return anims


    def __call__(self, *line) -> VMobject:
        is_negative = lambda x: x < 0
        if len(line) == 1:
            return self.code[line[0]-1*is_negative(line[0])]
        elif len(line) == 2:
            return self.code[line[0]-1*is_negative(line[0]):line[1]]
        else:
            raise ValueError(f"The number of argument line should be 1 or 2, but {len(line)} given")


def _find_multiple(string, target):
    return [i for i in range(len(string)) if string.find(target, i) == i]

def _count_indentation(text):
    for i in range(len(text)):
        if text[i] == " ":
            continue
        else:
            return i // 4