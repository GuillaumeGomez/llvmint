# Once done, the code to update can be seen there:
# https://github.com/rust-lang/rustc_codegen_gcc/pull/129/files#diff-4fb378dd283a8400f8f8defde08413dc31a55b1a776c3fa2473e3f059061740cR10-R114
import os
import json


def append_translation(json_data, p, array):
  it = json_data["index"][p]
  content = it["docs"].split('`')
  if len(content) != 5:
    return
  array.append('"{}" => "{}",'.format(content[1], content[3]))


# First we generate the JSON version of the docs.
os.system("cargo rustdoc -- -Zunstable-options --output-format json")

# Then we extract the information we want.
with open('target/doc/llvmint.json', 'r', encoding='utf8') as f:
    content = f.read()
json_data = json.loads(content)
# doc for the json is here:
# https://doc.rust-lang.org/stable/nightly-rustc/rustdoc_json_types/index.html
outputs = {}
general = []
ARCHS = [
    "AMDGPU",
    "aarch64",
    "arm",
    "cuda",
    "hexagon",
    "mips",
    "nvvm",
    "ppc",
    "ptx",
    "x86",
    "xcore",
]
for p in json_data["paths"]:
  it = json_data["paths"][p]
  if it["crate_id"] != 0:
    # This is from an external crate.
    continue
  if it["kind"] != "function":
    # We're only looking for functions.
    continue
  # if len(it["path"]) == 2:
  #   # This is a "general" intrinsic, not bound to a specific arch.
  #   append_translation(json_data, p, general)
  #   continue
  if len(it["path"]) != 3 or it["path"][1] not in ARCHS:
    continue
  arch = it["path"][1]
  if arch not in outputs:
    outputs[arch] = []
  append_translation(json_data, p, outputs[arch])

# Just in case:
ARCHS.sort()

print('match name {')
for arch in ARCHS:
   if arch not in outputs or len(outputs[arch]) == 0:
     continue
   outputs[arch].sort()
   print('    // {}'.format(arch))
   print('\n'.join(['    {}'.format(x) for x in outputs[arch]]))
if len(general) > 0:
  general.sort()
  print('    // Intrinsics not bound to a specific arch')
  print('\n'.join(['    {}'.format(x) for x in general]))
print('    _ => unimplemented!("***** unsupported LLVM intrinsic {}", name),')
print('}')
