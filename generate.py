
amount_of_structs = 2000

def write_file(string, path):
    text_file = open(path, "w+")
    text_file.write(string)
    text_file.close()

code = ""
code += "extern crate libloading_mini;\r\n"
code += "\r\n"
code += "use libloading_mini::Library;\r\n"
code += "use std::mem;\r\n"
code += "use std::ffi::c_void;\r\n"
code += "\r\n"

for i in range(0, amount_of_structs):
    code += "#[repr(C)] pub struct _" + str(i) + " { }\r\n"

code += "\r\n"
code += "\r\n"

code += "#[repr(C)]\r\n"
code += "pub struct BigDll {\r\n"
code += "    lib: Library,\r\n"
code += "    ptrs: [*mut c_void;" + str(amount_of_structs - 1) + "],\r\n"
code += "}\r\n"

code += "\r\n"
code += "\r\n"
code += "impl BigDll {\r\n"
for i in range(0, amount_of_structs - 1):
    code += "    pub fn function_" + str(i) + "(&self) -> fn(_:  _" + str(i) + ") -> _" + str(i + 1) + " { unsafe { mem::transmute(self.ptrs[" + str(i) + "]) } } \r\n"
code += "}\r\n"

code += "pub fn load_big_dll(path: &str) -> Option<BigDll> {\r\n"
code += "        let lib = Library::new(path)?;\r\n"
code += "        let ptrs = [\r\n"
for i in range(0, amount_of_structs - 1):
    code += "        lib.get(b\"function_" + str(i) + "\")?,\r\n"
code += "    ];\r\n"
code += "\r\n"
code += "        Some(BigDll {\r\n"
code += "            lib,\r\n"
code += "            ptrs,\r\n"
code += "        })\r\n"
code += "}\r\n"


write_file(code, './src/lib.rs')