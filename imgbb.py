from time import time
from typing import Any

from aiohttp import ClientSession, FormData
from pydantic import BaseModel


class Image(BaseModel):
    name: str
    extension: str
    width: int
    height: int
    size: int
    time: int
    size_formatted: str
    delete_url: str
    url_viewer: str
    url: str


async def upload_image(file: Any, delete_after: int | None = None) -> Image:
    async with ClientSession() as session:
        form_data = FormData(
            [
                ("action","upload"),
                ("type", "file"),
                ("source", file),
                ("timestamp", str(int(time()))),
            ]
        )
        if delete_after:
            form_data.add_field("expiration", str(delete_after))

        response = await session.post(
            url="https://imgbb.com/json",
            data=form_data
        )
        json: dict = await response.json()

    if json.get("status_code", None) != 200:
        raise Exception(json)

    image = Image(**json.get("image"))
    return image

async def delete_image(image: Image | str) -> bool:
    delete_url: str = image.delete_url if isinstance(image, Image) else image
    # example https://ibb.co/cwVnNz9/6c57d2eb6619897d2931fa7cef9c9e71

    async with ClientSession() as session:
        form_data = FormData(
            [
                ("action", "delete"),
                ("delete", "image"),
                ("deleting[id]", delete_url.split("/")[3])
            ]
        )

        response = await session.post(
            url="https://imgbb.com/json",
            data=form_data
        )
        json: dict = await response.json()

        print(json)

    return json.get("status_code", None) == 200

