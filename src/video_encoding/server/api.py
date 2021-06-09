from fastapi import FastAPI

router = FastAPI()


@router.get("/video/{resolution}/{path}")
async def process(resolution, path):
    raise NotImplementedError
