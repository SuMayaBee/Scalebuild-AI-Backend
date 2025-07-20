import requests
import os
from services.storage_service import upload_to_gcs
import io

REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY", "LFNiKM3HshXHUc5vcWccHpiL")

async def remove_background_from_url(image_url: str):
    """Remove background from an image using the remove.bg API and upload to GCS."""
    try:
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            data={
                'image_url': image_url,
                'size': 'auto'
            },
            headers={'X-Api-Key': REMOVE_BG_API_KEY},
        )

        if response.status_code == requests.codes.ok:
            # Create a filename
            file_name = f"no_bg_{os.path.basename(image_url)}.png"
            file_obj = io.BytesIO(response.content)

            bucket_name = os.getenv("GCS_BUCKET_NAME")
            if not bucket_name:
                raise Exception("GCS_BUCKET_NAME environment variable is not set")

            # Upload to Google Cloud Storage
            public_url = upload_to_gcs(file_obj, file_name, "image/png", bucket_name)
            return {"new_image_url": public_url}
        else:
            raise Exception(f"Error from remove.bg API: {response.status_code} {response.text}")

    except Exception as e:
        print(f"Error in background removal: {e}")
        raise e
