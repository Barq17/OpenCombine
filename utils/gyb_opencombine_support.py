def suffix_variadic(name, index, arity):
    return name + ('' if arity == 1 else str(index))

def list_with_suffix_variadic(name, arity):
    return [suffix_variadic(name, i, arity) for i in range(arity)]

def if_canimport_combine(framework):
    return '#if canImport(Combine)' if framework == 'Combine' else ''

def endif_canimport_combine(framework):
    return '#endif' if framework == 'Combine' else ''

frameworks_under_test = ['OpenCombine', 'CombineX', 'Combine']

def benchmark_name_swift_identifier(benchmark_name):
    return benchmark_name.replace(".", "_")

def benchmark_function(benchmark_name, framework_under_test):
    return "run_{}_{}".format(benchmark_name_swift_identifier(benchmark_name),
                              framework_under_test)

def benchmark_preamble(benchmark_name):
    result = """
import OpenCombine
import CombineX

#if canImport(Combine)
import Combine
#endif

import TestsUtils
"""
    for framework_under_test in frameworks_under_test:
        result += if_canimport_combine(framework_under_test)
        identifier = benchmark_name_swift_identifier(benchmark_name)
        result += """
private let {0}_{2} =
    BenchmarkInfo(name: "{1}.{2}",
                  runFunction: {3},
                  tags: [.validation, .api])
""".format(identifier,
           benchmark_name,
           framework_under_test,
           benchmark_function(benchmark_name, framework_under_test))
        
        result += endif_canimport_combine(framework_under_test)

    result += """
public var {}: [BenchmarkInfo] {{
    var tests = [BenchmarkInfo]()
""".format(identifier)
    
    for framework_under_test in frameworks_under_test:
        result += if_canimport_combine(framework_under_test)

        result += """
    tests.append({}_{})
""".format(identifier, framework_under_test)
        
        result += endif_canimport_combine(framework_under_test)

    result += """
    return tests
}
"""
    return result
