import CodeGenerator
from excel_template import get_template

if __name__ == "__main__":
    filename = input("Pass filename")
    delimiter = input("Pass delimiter [optiona]")
    output_file = input("Pass output file name]")
    if delimiter:
        data = get_template(filename,delimiter)
    else:
        data = get_template(filename)
    kupsko = CodeGenerator(data)
    kupsko1 = kupsko.generate_code()
    if output_file:
         kupsko.code_to_file(kupsko1,output_file)
    else:
         kupsko.code_to_file(kupsko1)
    input('Press ENTER to exit')
