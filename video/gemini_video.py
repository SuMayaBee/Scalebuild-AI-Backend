import time
from google import genai
from google.genai import types

client = genai.Client(api_key='AIzaSyAUwpCrOLA0YmnMJZ79CJEO-NrlFtWdpxY')

# Text-to-video prompt
prompt = """A close up of two cat staring at a cryptic drawing on a wall, torchlight flickering.
A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"""

# Optional: Negative prompt (what NOT to include)
negative_prompt = """blurry, low quality, distorted faces, bad lighting, shaky camera, poor audio"""

print("🎬 Starting Veo 3.0 text-to-video generation...")
print(f"📝 Prompt: {prompt}")
print(f"🚫 Negative prompt: {negative_prompt}")

# Generate video with all available parameters for text-to-video
operation = client.models.generate_videos(
    model="veo-3.0-generate-preview",
    prompt=prompt,
    #negative_prompt=negative_prompt,  # What to avoid in the video
    #aspect_ratio="16:9",  # Video aspect ratio (16:9, 9:16, 1:1)
    #person_generation="allow_all",  # For text-to-video: "allow_all" only
    # Note: 'image' parameter is not used for text-to-video generation
)

print(f"🔄 Video generation started. Operation: {operation.name}")

# Poll the operation status until the video is ready.
while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(10)
    operation = client.operations.get(operation)

# Download the generated video.
generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)
generated_video.video.save("dialogue_example.mp4")
print("Generated video saved to dialogue_example.mp4")