import ast

class BinOpFinder(ast.NodeVisitor):

    def visit_BinOp(self, node):
        print(f"found BinOp at line: {node.lineno}")
        self.generic_visit(node)

class RedundancyReducer(ast.NodeTransformer):

    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.Add):
            if isinstance(node.left, ast.Constant) and node.left.value == 0:
                return node.right
            elif isinstance(node.right, ast.Constant) and node.right.value == 0:
                return node.left
        if isinstance(node.op, ast.Mult):
            if isinstance(node.left, ast.Constant) and node.left.value == 1:
                return node.right
            elif isinstance(node.right, ast.Constant) and node.right.value == 1:
                return node.left
        return node

def main():
    with open("program.py", "r") as source:
        tree = ast.parse(source.read())

    print('##### OUTPUT #####')
    exec(compile(tree, filename="", mode="exec"))

    print('\n##### AST #####')
    print(ast.dump(tree, indent=4))

    print('\n##### VISIT #####')
    binOpFinder = BinOpFinder()
    binOpFinder.visit(tree)

    print('\n##### TRANSFORM #####')
    redundancyReducer = RedundancyReducer()
    redundancyReducer.visit(tree)
    print(ast.dump(tree, indent=4))

    print('\nCODE:')
    print(ast.unparse(tree))

    print('\nRESULT:')
    exec(compile(tree, filename="", mode="exec"))
    


if __name__ == "__main__":
    main()