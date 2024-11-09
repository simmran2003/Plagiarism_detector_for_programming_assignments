from django.shortcuts import render
import json
import re
from django.http import JsonResponse
from pycparser import c_parser, c_ast
from django.views.decorators.csrf import csrf_exempt
import numpy as np

# Function to extract function names from the AST
def extract_functions_from_ast(ast_tree):
    functions = []
    # Loop through 'ext' of the FileAST object, which contains the declarations and functions
    for node in ast_tree.ext:
        if isinstance(node, c_ast.FuncDef):  # Ensure it's a function definition node
            functions.append(node.decl.name)  # Add the function name
    return functions

# # Function to compare functions (You can expand this function as per your requirements)
# def compare_functions(functions1, functions2):
#     # Simple example comparison: Count matching functions (This can be customized to compare structure, arguments, etc.)
#     matching_functions = set(functions1).intersection(set(functions2))
#     similarity_score = len(matching_functions) / max(len(functions1), len(functions2))  # Simple similarity calculation
#     return similarity_score

# Define your view to compare the two code samples
@csrf_exempt
def compare_code(request):
    if request.method == "POST":
        try:
            # Check if request has content
            if not request.body:
                return JsonResponse({"error": "Empty request body"}, status=400)
            
            # Try to parse JSON data
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)

            # Extract the code1 and code2 from the request data
            code1 = data.get('code1')
            code2 = data.get('code2')
            print("Code1",code1)
            print("Code2",code2)
            # Check if both codes are provided
            if not code1 or not code2:
                return JsonResponse({"error": "Both code samples must be provided"}, status=400)

            # Preprocess the C code samples
            preprocessed_code1 = preprocess_c_code(code1)
            preprocessed_code2 = preprocess_c_code(code2)
            print("PP1",preprocessed_code1)
            print("PP2",preprocessed_code2)
            if preprocessed_code1 is None or preprocessed_code2 is None:
                return JsonResponse({"error": "Error in preprocessing the code"}, status=400)

            # Parse the preprocessed C code into ASTs
            ast1 = parse_c_code(preprocessed_code1)
            ast2 = parse_c_code(preprocessed_code2)

            # print("Ast1",ast1)
            # print("Ast2",ast2)
            if ast1 is None or ast2 is None:
                return JsonResponse({"error": "Error in parsing the code"}, status=400)

            # Extract functions from the ASTs
            functions1 = extract_functions_from_ast(ast1)
            functions2 = extract_functions_from_ast(ast2)

            # Check if valid functions were found
            if not functions1 or not functions2:
                return JsonResponse({"error": "No valid functions found in one or both code samples"}, status=400)
            print("func1:",functions1)
            print("func2:",functions2)
            list1 = []
            list2 = []
            for func in ast1:
                if type(func).__name__ == "FuncDef":
                    list1.append(func)
            for func in ast2:
                if type(func).__name__ == "FuncDef":
                    list2.append(func)

            # Analyze functions to extract their characteristics
            analyzed_functions1 = [analyze_function(item) for item in list1]
            analyzed_functions2 = [analyze_function(item) for item in list2]
            print("Analyzed 1:",analyzed_functions1)
            print("Analyzed 2:",analyzed_functions2)
            # Calculate the similarity between the functions
            similarity_scores = []
            for func1, func2 in zip(analyzed_functions1, analyzed_functions2):
                similarity = calculate_similarity(func1, func2)
                similarity_scores.append(similarity)

            # Average the similarity scores to get a total similarity score
            total_similarity = sum([score['total'] for score in similarity_scores]) / len(similarity_scores) if similarity_scores else 0

            # Categorize the total similarity score
            similarity_category = get_similarity_category(total_similarity)

            # Return the results
            return JsonResponse({
                "total_similarity": total_similarity,
                "similarity_category": similarity_category,
                "function_similarity_details": similarity_scores
            }, status=200)

        except Exception as e:
            # Handle any unexpected errors
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def preprocess_c_code(c_code):
    """
    Preprocesses C code by removing preprocessor directives and comments
    while preserving the actual code structure.
    """
    try:
        # Remove comments (single-line and multi-line)
        c_code = re.sub(r'//.*?$', '', c_code, flags=re.MULTILINE)
        c_code = re.sub(r'/\.?\*/', '', c_code, flags=re.DOTALL)

        # Remove #include directives
        c_code = re.sub(r'#include.*?\n', '', c_code)
        
        # Replace bool with int and true/false with 1/0 directly
        c_code = """
typedef int bool;
""" + c_code.replace('true', '1').replace('false', '0')

        # Normalize whitespace while preserving newlines
        c_code = re.sub(r'[ \t]+', ' ', c_code)
        c_code = re.sub(r'\n\s*\n', '\n', c_code)

        return c_code.strip()
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return None

def parse_c_code(c_code):
    """
    Parse C code into AST using pycparser.
    """
    parser = c_parser.CParser()
    try:
        # Add fake headers to help with parsing
        fake_headers = """
typedef int __builtin_va_list;
typedef int __gnuc_va_list;
typedef int __int8_t;
typedef int __uint8_t;
typedef int __int16_t;
typedef int __uint16_t;
typedef int __int_least16_t;
typedef int __uint_least16_t;
typedef int __int32_t;
typedef int __uint32_t;
typedef int __int64_t;
typedef int __uint64_t;
typedef int __int_least32_t;
typedef int __uint_least32_t;
typedef int _LOCK_T;
typedef int _LOCK_RECURSIVE_T;
typedef int _off_t;
typedef int __dev_t;
typedef int __uid_t;
typedef int __gid_t;
"""
        # Combine headers with preprocessed code
        full_code = fake_headers + c_code
        
        # Parse the combined code
        ast = parser.parse(full_code)
        
        if ast is None:
            print("Failed to generate AST")
            return None
            
        return ast
        
    except c_parser.ParseError as e:
        print(f"Parse error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during parsing: {e}")
        return None


def analyze_function(func_def):
    """
    Analyzes a FuncDef node to extract characteristics for similarity analysis.
    """
    # Initialize analysis result
    analysis = {
        'parameters': set(),
        'operations': [],
        'control_flow': [],
        'function_calls': set(),
        'return_statements': [],
        'variables': set(),
        'constants': set()
    }
    print(type(func_def))
    # Extract parameters
    if func_def.decl and isinstance(func_def.decl.type, c_ast.FuncDecl) and func_def.decl.type.args:
        for param in func_def.decl.type.args.params:
            if isinstance(param, c_ast.Decl) and param.name:
                analysis['parameters'].add(param.name)
                if isinstance(param.type, c_ast.TypeDecl) and isinstance(param.type.type, c_ast.IdentifierType):
                    analysis['variables'].add(param.name)

    # Recursive helper function to traverse nodes
    def visit(node):
        if isinstance(node, c_ast.BinaryOp):
            # Capture binary operations
            analysis['operations'].append(f"BINOP_{node.op}")
            visit(node.left)
            visit(node.right)
            
        elif isinstance(node, c_ast.Assignment):
            # Capture assignment operations
            analysis['operations'].append(f"ASSIGN_{node.op}")
            visit(node.rvalue)
            visit(node.lvalue)
            
        elif isinstance(node, c_ast.If):
            # Capture control flow (If statements)
            analysis['control_flow'].append("IF")
            visit(node.cond)
            if node.iftrue:
                visit(node.iftrue)
            if node.iffalse:
                analysis['control_flow'].append("ELSE")
                visit(node.iffalse)
                
        elif isinstance(node, c_ast.Return):
            # Capture return statements
            analysis['return_statements'].append("RETURN")
            if node.expr:
                visit(node.expr)
                
        elif isinstance(node, c_ast.ID):
            # Capture variable usage
            analysis['variables'].add(node.name)
            
        elif isinstance(node, c_ast.Constant):
            # Capture constants
            analysis['constants'].add(node.value)
            
        elif isinstance(node, c_ast.FuncCall):
            # Capture function calls
            if isinstance(node.name, c_ast.ID):
                analysis['function_calls'].add(node.name.name)
            if node.args:
                for arg in node.args.exprs:
                    visit(arg)
                    
        elif isinstance(node, c_ast.Compound):
            # Process each statement in a compound block
            if node.block_items:
                for stmt in node.block_items:
                    visit(stmt)
                    
        # Add more node types if needed for other cases

    # Start traversal on the function body
    if func_def.body:
        visit(func_def.body)
    
    return analysis

def sequence_similarity(seq1, seq2):
    """
    Computes Levenshtein similarity between two sequences.
    """
    try:
        if not seq1 and not seq2:
            return 1.0
        if not seq1 or not seq2:
            return 0.0
        
        # Initialize matrix for Levenshtein distance
        len1, len2 = len(seq1), len(seq2)
        matrix = np.zeros((len1 + 1, len2 + 1))

        for i in range(len1 + 1):
            matrix[i][0] = i
        for j in range(len2 + 1):
            matrix[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if seq1[i - 1] == seq2[j - 1] else 1
                matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)

        # Return normalized similarity score
        return 1 - matrix[len1][len2] / max(len1, len2)
    except Exception as e:
        print(f"Error calculating Levenshtein similarity: {e}")
        return 0.0


def calculate_similarity(analysis1, analysis2):
    """
    Calculates similarity between two analyzed functions.
    """
    try:
        # Convert sets to sorted lists for Levenshtein similarity calculation
        parameters_similarity = sequence_similarity(sorted(analysis1['parameters']), sorted(analysis2['parameters']))
        operations_similarity = sequence_similarity(analysis1['operations'], analysis2['operations'])
        control_flow_similarity = sequence_similarity(analysis1['control_flow'], analysis2['control_flow'])

        return {
            'total': (parameters_similarity + operations_similarity + control_flow_similarity) / 3,
            'parameters': parameters_similarity,
            'operations': operations_similarity,
            'control_flow': control_flow_similarity
        }
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return {
            'total': 0.0,
            'parameters': 0.0,
            'operations': 0.0,
            'control_flow': 0.0
        }


def get_similarity_category(similarity_score):
    """
    Categorizes the similarity score.
    """
    if similarity_score >= 0.6:
        return "Highly Similar"
    # elif similarity_score >= 0.5:
    #     return "Moderately Similar"
    else:
        return "Low Similarity"

def home(request):
    return render(request, 'AST_based_approach/home.html')