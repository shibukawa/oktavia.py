"""
Test data generator script to test compatibility with binary-io.jsx
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import oktavia

output = oktavia.binaryio.BinaryOutput()

output.dump_16bit_number(0)
output.dump_16bit_number(65535)
output.dump_32bit_number(0)
output.dump_32bit_number(4294967295)
output.dump_string("hello world")
output.dump_string_list(['hello', 'world'])
output.dump_string_list_map({'hello': ['HELLO'], 'world': ['WORLD']})
output.dump_32bit_number_list([0, 0, 0, 0, 0])

out = open('testdata.bin', 'bw')
out.write(output.result())
out.close()
