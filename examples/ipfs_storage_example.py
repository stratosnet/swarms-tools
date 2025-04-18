import io
import os
import asyncio

from swarms_tools.storage.ipfs import IPFSStorageClient


def _generate_in_memory_file(size_in_mb: int) -> io.BytesIO:
    mega_byte = 1_000_000
    file_io = io.BytesIO(os.urandom(size_in_mb * mega_byte))
    return file_io


def base_example():
    print("ipfs storage sync base example")
    client = IPFSStorageClient(timeout=None)

    key = "hello"
    value = b"world"

    cid = client.put(key, value)
    print("Got cid:", cid)
    value_from_ipfs = client.get(key=cid)

    assert value == value_from_ipfs
    print("Value match")

    # or through contextmanager
    with IPFSStorageClient(timeout=None) as client:
        cid = client.put(key, value)
        print("Got cid:", cid)
        value_from_ipfs = client.get(key=cid)

        assert value == value_from_ipfs
        print("Value match")
    print("")


async def base_async_example():
    print("ipfs storage async base example")
    client = IPFSStorageClient(timeout=None)

    key = "ahello"
    value = b"aworld"

    cid = await client.aput(key, value)
    print("Got cid:", cid)
    value_from_ipfs = await client.aget(key=cid)

    assert value == value_from_ipfs
    print("Value match")

    await client.close()

    # or through contextmanager
    with IPFSStorageClient(timeout=None) as client:
        cid = await client.aput(key, value)
        print("Got cid:", cid)
        value_from_ipfs = await client.aget(key=cid)

        assert value == value_from_ipfs
        print("Value match")
    print("")


async def example_with_big_file():
    print("ipfs storage async big file example")
    client = IPFSStorageClient(timeout=None)

    key = "bigfile"
    file_ = _generate_in_memory_file(100)

    cid = await client.aput(key, file_)
    print("Got cid from big:", cid)
    value_from_ipfs = await client.aget(key=cid)

    original = file_.getvalue()
    retrieved = value_from_ipfs

    print("Data matches:", original == retrieved)
    assert original == retrieved
    print("Value match")

    await client.close()


def main():
    base_example()
    asyncio.run(base_async_example())
    asyncio.run(example_with_big_file())


if __name__ == "__main__":
    main()
