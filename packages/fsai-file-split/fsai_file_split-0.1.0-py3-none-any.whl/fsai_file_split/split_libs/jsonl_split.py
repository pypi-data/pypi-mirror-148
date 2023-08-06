from loguru import logger
import glob, subprocess, os

def json_split(split_by, chunk_size, input_file_path, output_file_path, start=0):

    num_lines = open(input_file_path).read().count("\n")

    # number_of_buckets
    if split_by == "number_of_buckets":
        lines_per_file = int(num_lines / chunk_size)
    else: # size_of_buckets
        lines_per_file = chunk_size

    if lines_per_file < chunk_size:
        logger.warning("There are less lines than the chunk size. Setting the lines per file to {}".format(num_lines))
        lines_per_file = num_lines

    # Execute the split as a subprocess and ait
    p = subprocess.Popen(
        ["split", "-l", str(lines_per_file), input_file_path, "{}.".format(output_file_path)]
    )
    p.wait()

    output_file_dir = os.path.dirname(os.path.abspath(output_file_path))

    # Get all files in the output directory
    files = glob.glob(os.path.join(output_file_dir, "*.jsonl.*"))

    saved = []

    # For each file
    for counter, file in enumerate(files, start=start):

        # Get the full file path
        path = os.path.dirname(os.path.abspath(file))

        new_file_path = "{}/{}.jsonl".format(path, counter)
        
        # Rename the file
        os.rename(file, new_file_path)

        saved.append(new_file_path)

    return saved