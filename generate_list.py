# Once done, the code to update can be seen there:
# https://github.com/rust-lang/rustc_codegen_gcc/pull/129/files#diff-4fb378dd283a8400f8f8defde08413dc31a55b1a776c3fa2473e3f059061740cR10-R114
import os

# First we generate the JSON version of the docs.
os.system("cargo rustdoc -- -Zunstable-options --output-format json")

# Then we extract the information we want.
with open('target/doc/llvmint.json', 'r', encoding='utf8') as f:
    content = f.read()
json_data = json.loads(content)
# doc for the json is here:
# https://doc.rust-lang.org/stable/nightly-rustc/rustdoc_json_types/index.html
for p in json_data["paths"]:
  it = json_data["paths"][p]
  # If we want, we can switch "x86" with another arch without problem.
  if len(it["path"]) != 3 or it["path"][1] != "x86":
    continue
  it = json_data["index"][p]
  content = it["docs"].split('`')
  if len(content) != 5:
    continue
  print('"{}" => "{}"'.format(it["name"], content[1], content[3]))
