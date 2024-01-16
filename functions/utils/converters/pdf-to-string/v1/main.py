import asyncio
import multiprocessing
from io import BytesIO

from metadata import Inputs, Outputs, Params, func
from PyPDF2 import PageObject, PdfReader


def extract_text_multi(content: bytearray):
    reader = PdfReader(BytesIO(content))

    texts = multiprocessing.Manager().list(["" for _ in range(len(reader.pages))])

    processes: list[multiprocessing.Process] = []

    def extract_text(page: PageObject, i: int):
        texts[i] = page.extract_text()
        print(f"{i} -> {len(texts[i])}")

    for i, page in enumerate(reader.pages):
        p = multiprocessing.Process(target=extract_text, args=[page, i])
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    return "".join(texts)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    text = await asyncio.to_thread(extract_text_multi, inputs.pdf_file.get_data())
    return Outputs(text=text)
