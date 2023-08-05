# BIPF-Python
A Python library for BIPF (Binary In-Place Format)

See [https://github.com/ssbc/bipf](https://github.com/ssbc/bipf)
for the origin of BIPF and a description of the format. A condensed
writeup is at the end of this document.

Quick start (the interface is the same as in json and cbor2):

- install the library: ```python3 -m pip install bipf```
- in your code: ```from bipf import dumps, loads```
- ```dumps(<your_python_data>)``` serializes the object to bytes
- ```loads(<some_bipf_bytes>)``` restores a BIPF-serialized object

A rich demo in ```tests/demo.py``` also generates a testvector. The output is:

```
# encoded 80 bytes: f50418666f6f8c02127fff0a800a810aff0a000a010a7f12800012007f1a0080000e002179656168061862616695014046726564686f6c6d4305413da6832fbc3f186261722868656c6c6f1862617a06

# generator demo:
> 18666f6f 8c02127fff0a800a810aff0a000a010a7f12800012007f1a0080000e00217965616806
  > 0 127fff
  > 1 0a80
  > 2 0a81
  > 3 0aff
  > 4 0a00
  > 5 0a01
  > 6 0a7f
  > 7 128000
  > 8 12007f
  > 9 1a008000
  > 10 0e00
  > 11 2179656168
  > 12 06
> 18626166 95014046726564686f6c6d4305413da6832fbc3f
  > 4046726564686f6c6d 4305413da6832fbc3f
> 18626172 2868656c6c6f
> 1862617a 06

# parse entire object and read a single value
{'foo': [-129, -128, -127, -1, 0, 1, 127, 128, 32512, 32768, False, b'yeah', None], 'baf': {'Fredholm': 0.1101000100000001}, 'bar': 'hello', 'baz': None}
hello

# seek and decode a single value
key pos 69 --> hello
path pos 56 --> 0.1101000100000001

# keys can be bytes, int, double, bool and None:
# input:
 {b'\x00\x01': 'ah', 99: 'eh', 4.3: 'ih', True: 'oh', None: 'uh'}
# encoded 34 bytes: 85021100011061680a631065684333333333333311401069680e01106f6806107568
# parse entire serialization
 {b'\x00\x01': 'ah', 99: 'eh', 4.3: 'ih', True: 'oh', None: 'uh'}
```

---

## BIPF format

BIPF uses type-length-value (TLV) encoding for atomic types
as well as for lists and dictionaries. This allows to skip entries
without having to hunt for an end-of-list or end-of-dict marker.

- ```TLV``` := concatenation of ```tag_bytes``` and ```value_bytes```
- ```tag_bytes``` := varint_encoding( len(```value_bytes```) << 3 | ```type_bits``` )
- ```type_bits``` :=
```
                        value bytes:
   TYPE_STRING   # 000  utf-8 encoded string
   TYPE_BYTES    # 001  raw
   TYPE_INT      # 010  signed little endian, 1 to 8 bytes, minimal size
   TYPE_DOUBLE   # 011  64bit IEEE-754 float, little endian
   TYPE_LIST     # 100  sequence of BIPF-encoded elements
   TYPE_DICT     # 101  sequence with alternating BIPF-encoded key and val
   TYPE_BOOLNONE # 110  length==0 -> None, else one byte with 0 or 1 for F/T
   TYPE_RESERVED # 111
```
- varint_encoding is ```unsigned LEB128``` as used in WebAssembly
- keys for dictionaries can have any type except list or dict (and reserved)

---
