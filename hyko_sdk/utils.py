from typing import AsyncIterator
import httpx
import asyncio
import tqdm
import math


async def download_file(url: str) -> bytearray:
    async with httpx.AsyncClient(verify=False, http2=True) as client:
        head_res = await client.head(url=url)
        if not head_res.is_success:
            raise Exception("Could not read HEAD")
        file_size = int(head_res.headers["Content-Length"])
        with tqdm.tqdm(total=file_size, unit_scale=True, unit_divisor=1024, unit="B", desc=f"Downloading {url}") as progress:
            step = math.ceil(file_size / 16)
            ranges = []
            for s in range(0, file_size, step):
                e = s + step
                if e > file_size:
                    e = file_size
                ranges.append((s, e, bytearray()))
            def update_progress(delta_n: int):
                progress.update(delta_n)
            tasks = [download_range(url=url, client=client, start=start, end=end, data=data, update_progress=update_progress) for start, end, data in ranges]
            await asyncio.wait(tasks)
            out = bytearray()
            total_downloaded = 0
            for _, _, data in ranges:
                total_downloaded += len(data)
                out += data
            return out

async def download_range(url: str, client: httpx.AsyncClient, start: int, end: int, data: bytearray, update_progress) -> bytearray:
    async with client.stream("GET", url, headers={"Range": f"bytes={start}-{end-1}"}) as response:
        async for chunk in response.aiter_bytes():
            data += chunk
            update_progress(len(chunk))
    return data

async def bytearray_aiter(data: bytearray, update_progress) -> AsyncIterator[bytearray]:
    step_size = int(len(data) / 100)
    if not step_size: step_size = 1
    for start in range(0, len(data), step_size):
        end = start + step_size
        if end > len(data):
            end = len(data)
        yield data[start:end]
        update_progress(end-start)

async def upload_file(url: str, data: bytearray) -> None:
    async with httpx.AsyncClient(verify=False, http2=True) as client:
        file_size = len(data)
        with tqdm.tqdm(total=file_size, unit_scale=True, unit_divisor=1024, unit="B", desc=f"Uploading {url}") as progress:
            res = await client.put(
                url=url,
                headers={"Content-Length": str(file_size)},
                content=bytearray_aiter(data=data, update_progress=progress.update),
            )
            if not res.is_success:
                raise Exception(f"Error while uploading, {res.text}")