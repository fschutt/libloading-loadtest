
amount_of_structs = 2000

def write_file(string, path):
    text_file = open(path, "w+")
    text_file.write(string)
    text_file.close()

code = ""
code += "extern crate libloading;\r\n"

code += "\r\n"
code += "\r\n"

code += "#[cfg(unix)]\r\n"
code += "use libloading::os::unix::{Library, Symbol};\r\n"
code += "#[cfg(windows)]\r\n"
code += "use libloading::os::windows::{Library, Symbol};\r\n"

code += "\r\n"
code += "\r\n"

for i in range(0, amount_of_structs):
    code += "#[repr(C)] pub struct _" + str(i) + " { }\r\n"

code += "\r\n"
code += "\r\n"

code += "#[repr(C)]\r\n"
code += "pub struct BigDll {\r\n"
code += "    lib: Library,\r\n"
for i in range(0, amount_of_structs - 1):
    code += "    function_" + str(i) + ": Symbol<extern fn(_:  _" + str(i) + ") -> _" + str(i + 1) + ">,\r\n"
code += "}\r\n"

code += "\r\n"
code += "\r\n"

code += "pub fn load_big_dll(path: &str) -> Result<BigDll, &'static str> {\r\n"
code += "    let lib = Library::new(path).map_err(|_| \"library is not a DLL file (?!)\")?;\r\n"
for i in range(0, amount_of_structs - 1):
    code += "    let function_" + str(i) + " = unsafe { lib.get::<extern fn(_: _" + str(i) + ") -> _" + str(i + 1) + ">(b\"function_" + str(i) + "\").map_err(|_| \"could not load fn function_" + str(i) + "\")? };\r\n"
code += "    Ok(BigDll {\r\n"
code += "        lib,\r\n"
for i in range(0, amount_of_structs - 1):
    code += "        function_" + str(i) + ",\r\n"
code += "    })\r\n"
code += "}\r\n"

write_file(code, './src/lib.rs')