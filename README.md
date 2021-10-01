![](https://repository-images.githubusercontent.com/412517075/d07cae05-6d5e-4f70-9fa0-4ced237ac1ec)


# Swift Codable Model Generator
A simple script to generate swift model file from a json file.

# Usage Example

1. Run the terminal
2. Go to the folder where you want to save the generated swift model file
3. run the following command:

```
python3 swiftModeler.py products.json Product

```

# Requirements:

[x] The json file must contains a list of objects of size 1 or more.
[x] The json file name and the model name are required in the command.
[x]	The json file should NOT contains nested objects.
[x] The supported types String, Int, Double and their arrays types.

# Roadmap:

[] The json file can be eitehr an object or list of objects
[] Default model name if it's not provided in the command
[] The json file can have nested objects