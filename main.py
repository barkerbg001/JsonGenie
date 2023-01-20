import json
import re

def json_to_csharp_class(json_str):
    json_obj = json.loads(json_str)
    class_str = json_obj_to_csharp_class_str(json_obj, "RootObject")
    return class_str

def json_obj_to_csharp_class_str(json_obj, class_name):
    class_str = "public class " + class_name + "{\n"
    for key, value in json_obj.items():
        if isinstance(value, dict):
            inner_class_str = json_obj_to_csharp_class_str(value, key.title())
            class_str += inner_class_str
            class_str += "    public " + key.title() + " " + key + " { get; set; }\n"
        elif isinstance(value, list):
            list_str = json_list_to_csharp_class_str(value, key.title())
            class_str += list_str
            class_str += "    public List<" + key.title() + "> " + key + " { get; set; }\n"
        else:
            class_str += "    public " + type_str(value) + " " + key + " { get; set; }\n"
    class_str += "}\n"
    return class_str

def json_list_to_csharp_class_str(json_list, class_name):
    list_str = ""
    for json_obj in json_list:
        if isinstance(json_obj, dict):
            list_str += json_obj_to_csharp_class_str(json_obj, class_name)
    return list_str

def type_str(value):
    if isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, bool):
        return "bool"
    else:
        return "string"

if __name__ == "__main__":
    json_file = open("data.json")
    json_str = json_file.read()
    json_file.close()

    csharp_class_str = json_to_csharp_class(json_str)
    csharp_class_str = re.sub(r'(?<=\n)\s+', '', csharp_class_str)
    csharp_class_file = open("Data.cs", "w")
    csharp_class_file.write(csharp_class_str)
    csharp_class_file.close()