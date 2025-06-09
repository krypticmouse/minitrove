from time import time
from tqdm import tqdm
from loguru import logger


def hf_sourcing():
    from datasets import load_dataset

    start_time = time()
    ds = load_dataset(
        "microsoft/mediflow",
        split="mediflow",
        streaming=True,
    )

    for i, row in tqdm(enumerate(ds)):
        pass
    end_time = time()
    logger.info(f"Time taken: {end_time - start_time} seconds")


def fsspec_glob(file_path):
    import fsspec
    import braceexpand

    """
    Get a list of files in a fsspec filesystem that match a pattern.

    We extend fsspec glob to also work with braces, using braceexpand.

    Args:
        file_path (str): a file path or pattern, possibly with *, **, ?, or {}'s

    Returns:
        list: A list of files that match the pattern. returned files have the protocol prepended to them.
    """

    # Use fsspec to get a list of files
    fs = fsspec.core.url_to_fs(file_path)[0]
    protocol = fsspec.core.split_protocol(file_path)[0]

    def join_protocol(file):
        if protocol:
            return f"{protocol}://{file}"
        return file

    out = []

    # glob has to come after braceexpand
    for file in braceexpand.braceexpand(file_path):
        out.extend(join_protocol(file) for file in fs.glob(file))

    return out


def fsspec_sourcing():
    import fsspec

    hf_path = "hf://datasets/microsoft/mediflow/data/mediflow-*"
    files = fsspec_glob(hf_path)
    logger.info(f"Found {len(files)} files, {files[0]}")

    start_time = time()
    for file in files:
        with fsspec.open(file) as f:
            for i, line in tqdm(enumerate(f)):
                pass
    end_time = time()

    logger.info(f"Time taken: {end_time - start_time} seconds")


def datatrove_sourcing():
    from datatrove.pipeline.readers import JsonlReader
    from datatrove.executor import LocalPipelineExecutor

    dist_executor = LocalPipelineExecutor(
        tasks=5,
        workers=-1,
        pipeline=[
            JsonlReader(
                "hf://datasets/microsoft/mediflow/data/",
                glob_pattern="mediflow-*",
                text_key="instruction",
                file_progress=True,
                doc_progress=True,
            ),
        ],
    )
    start_time = time()
    dist_executor.run()
    end_time = time()
    logger.info(f"Time taken: {end_time - start_time} seconds")


def minitrove_sourcing():
    from databrix.sourcer.sourcers import JSONSourcer

    sourcer = JSONSourcer(
        id_key="instruction_id",
        text_key="instruction",
    )
    start_time = time()
    files = fsspec_glob("hf://datasets/microsoft/mediflow/data/mediflow-*")
    sources = sourcer.source(files, num_processes=5, num_threads=64)
    for source in tqdm(sources, desc="Processing sources"):
        for i, doc in tqdm(source, desc="Processing documents"):
            pass
    end_time = time()
    logger.info(f"Time taken: {end_time - start_time} seconds")


if __name__ == "__main__":
    # hf_sourcing()               # 200.5s
    # fsspec_sourcing()           # 940s
    # datatrove_sourcing()        # 77s
    minitrove_sourcing()        # 77s