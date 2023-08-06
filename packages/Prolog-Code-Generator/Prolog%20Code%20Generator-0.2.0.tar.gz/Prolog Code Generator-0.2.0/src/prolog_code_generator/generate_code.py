import argparse
from excel_template import get_template
import CodeGenerator

def main() -> None:
    """Main function to run code generator from console by prolog_code_generator.py -f {filename} -d {delimiter} -o {output_file}"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="Pass path to file", required=True)
    parser.add_argument("-d", "--delimiter", help="Pass delimiter [optional]")
    parser.add_argument("-o", "--output", help="Pass path to output and file name [optional]")
    args = parser.parse_args()
    data = get_template(*[arg for arg in [args.filename,args.delimiter] if arg])
    kupsko = CodeGenerator(data)
    kupsko1 = kupsko.generate_code()
    kupsko.code_to_file(*[arg for arg in [kupsko1,args.output] if arg])
    filename = args.filename
    delimiter = args.delimiter
    output_file = args.output
    

if __name__ == "__main__":
    main()
    