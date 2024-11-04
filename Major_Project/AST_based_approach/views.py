from django.shortcuts import render
from django.http import JsonResponse
from pycparser import c_parser, c_ast
import hashlib

def parse_c_code(c_code):
    if not c_code:
        print("Empty code received")
        return None
        
    print("Original code received:", repr(c_code))
    
    # Add necessary typedefs and declarations
    fake_libc_include = """
    typedef void *__builtin_va_list;
    typedef int size_t;
    typedef int __builtin_va_list;
    typedef int __gnuc_va_list;
    typedef int __int32_t;
    typedef int __uint32_t;
    typedef int __int64_t;
    typedef int __uint64_t;
    typedef int __off_t;
    typedef int __pid_t;
    typedef int __clock_t;
    typedef int __time_t;
    typedef int __clockid_t;
    typedef int __timer_t;
    typedef int __locale_t;
    typedef int *__FILE;
    typedef int FILE;
    typedef int time_t;
    typedef int va_list;
    typedef int ptrdiff_t;
    typedef int wchar_t;
    """

    try:
        # Clean up the code
        c_code = c_code.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove any trailing semicolons after function closing brace
        c_code = c_code.strip()
        if c_code.endswith('};'):
            c_code = c_code[:-1]
        
        # Combine fake includes with cleaned code
        full_code = fake_libc_include + '\n' + c_code
        
        print("Code to parse:", repr(full_code))
        
        parser = c_parser.CParser()
        ast = parser.parse(full_code)
        
        # Find the first function definition
        for node in ast.ext:
            if isinstance(node, c_ast.FuncDef):
                return node
                
        print("No function definition found in the AST")
        return None

    except c_parser.ParseError as e:
        print(f"ParseError details: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

def hash_function_structure(node):
    if not isinstance(node, c_ast.FuncDef):
        print(f"Not a FuncDef node: {type(node)}")
        return None
        
    print(f"Processing function: {node.decl.name}")
    
    # Get function parameters
    params = node.decl.type.args.params if node.decl.type.args else []
    param_hash = hashlib.sha256()
    for param in params:
        print(f"Processing parameter: {param.name}")
        param_hash.update(param.type.type.names[0].encode())
        param_hash.update(param.name.encode())
    param_hash = param_hash.hexdigest()

    operation_sequence = []
    control_flow_elements = []

    def traverse_body(body):
        if isinstance(body, c_ast.Compound) and body.block_items:
            for stmt in body.block_items:
                if isinstance(stmt, c_ast.Decl) and stmt.init:
                    if isinstance(stmt.init, c_ast.BinaryOp):
                        print(f"Found operation: {stmt.init.op}")
                        operation_sequence.append(stmt.init.op)
                elif isinstance(stmt, c_ast.Assignment):
                    if isinstance(stmt.rvalue, c_ast.BinaryOp):
                        print(f"Found operation: {stmt.rvalue.op}")
                        operation_sequence.append(stmt.rvalue.op)
                elif isinstance(stmt, c_ast.If):
                    print("Found if statement")
                    control_flow_elements.append("if")
                    if stmt.iftrue:
                        traverse_body(stmt.iftrue)
                    if stmt.iffalse:
                        traverse_body(stmt.iffalse)

    traverse_body(node.body)
    print(f"Operations found: {operation_sequence}")
    print(f"Control flow elements found: {control_flow_elements}")

    operations_hash = hashlib.sha256("".join(operation_sequence).encode()).hexdigest()
    control_flow_hash = hashlib.sha256("".join(control_flow_elements).encode()).hexdigest()

    return param_hash, operations_hash, control_flow_hash

def calculate_similarity_score(hash1, hash2):
    if hash1 is None or hash2 is None:
        return None, None, None, None
        
    param_hash1, ops_hash1, cf_hash1 = hash1
    param_hash2, ops_hash2, cf_hash2 = hash2

    # Parameter similarity
    param_similarity = 1 if param_hash1 == param_hash2 else 0

    # Operations similarity
    ops_similarity = sum(a == b for a, b in zip(ops_hash1, ops_hash2)) / max(len(ops_hash1), len(ops_hash2))

    # Control flow similarity
    cf_similarity = sum(a == b for a, b in zip(cf_hash1, cf_hash2)) / max(len(cf_hash1), len(cf_hash2))

    # Calculate weighted average
    weights = {"param": 0.3, "ops": 0.4, "cf": 0.3}
    total_similarity = (
        param_similarity * weights["param"] +
        ops_similarity * weights["ops"] +
        cf_similarity * weights["cf"]
    )

    return total_similarity, param_similarity, ops_similarity, cf_similarity

def get_similarity_category(similarity_score):
    if similarity_score > 0.5:
        return "Similar"
    elif similarity_score < 0.5:
        return "Not Similar"
    else:
        return "Somewhat Similar"

def compare_code(request):
    if request.method == "POST":
        code1 = request.POST.get("code1", "").strip()
        code2 = request.POST.get("code2", "").strip()

        print("Processing Code 1:", repr(code1))
        print("Processing Code 2:", repr(code2))

        if not code1 or not code2:
            return JsonResponse({"error": "Both code samples are required"}, status=400)

        # Parse both code samples
        ast1 = parse_c_code(code1)
        ast2 = parse_c_code(code2)

        # Check if parsing was successful
        if ast1 is None:
            return JsonResponse({"error": "Error parsing code sample 1. Please check the syntax."}, status=400)
        if ast2 is None:
            return JsonResponse({"error": "Error parsing code sample 2. Please check the syntax."}, status=400)

        # Get function hashes directly since parse_c_code now returns FuncDef
        hash1 = hash_function_structure(ast1)
        hash2 = hash_function_structure(ast2)

        if hash1 is None:
            return JsonResponse({"error": "No valid function found in code sample 1"}, status=400)
        if hash2 is None:
            return JsonResponse({"error": "No valid function found in code sample 2"}, status=400)

        total_similarity, param_similarity, ops_similarity, cf_similarity = calculate_similarity_score(hash1, hash2)
        
        if total_similarity is None:
            return JsonResponse({"error": "Error calculating similarity"}, status=400)

        similarity_category = get_similarity_category(total_similarity)

        result = {
            "total_similarity": round(total_similarity, 2),
            "similarity_category": similarity_category,
            "param_similarity": round(param_similarity, 2),
            "ops_similarity": round(ops_similarity, 2),
            "cf_similarity": round(cf_similarity, 2)
        }

        return JsonResponse(result)

    return JsonResponse({"error": "Invalid request method"}, status=405)
    
def home(request):
    return render(request, 'AST_based_approach/home.html')