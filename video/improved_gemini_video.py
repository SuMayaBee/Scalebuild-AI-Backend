#!/usr/bin/env python3
"""
Gemini Video Generation Script
This script uses Google's Gemini API with Veo 3.0 to generate videos from text prompts
"""
import os
import time
import json
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiVideoGenerator:
    def __init__(self):
        """Initialize the Gemini video generator with Veo 3.0"""
        self.setup_gemini()
        print("✅ Gemini Video Generator with Veo 3.0 initialized")
    
    def setup_gemini(self):
        """Setup Gemini API client"""
        try:
            # Initialize the Gemini client
            self.client = genai.Client()
            print("✅ Gemini client configured successfully")
            
        except Exception as e:
            print(f"❌ Error setting up Gemini: {e}")
            print("💡 Make sure your Google credentials are properly configured")
            raise
    
    def generate_video(
        self, 
        prompt: str, 
        output_filename: str = None, 
        negative_prompt: str = None,
        aspect_ratio: str = "16:9",
        person_generation: str = "allow_all",
        max_wait_time: int = 600
    ):
        """
        Generate a video from a text prompt using Gemini with Veo 3.0
        
        Args:
            prompt (str): Text description of the video to generate
            output_filename (str): Name of the output video file (optional)
            negative_prompt (str): What NOT to include in the video (optional)
            aspect_ratio (str): Video aspect ratio - "16:9", "9:16", or "1:1"
            person_generation (str): For text-to-video: "allow_all" only
            max_wait_time (int): Maximum time to wait for generation in seconds
        
        Returns:
            str: Path to the generated video file or None if failed
        """
        try:
            print(f"🎬 Starting video generation with Veo 3.0...")
            print(f"📝 Prompt: {prompt}")
            if negative_prompt:
                print(f"🚫 Negative prompt: {negative_prompt}")
            print(f"📐 Aspect ratio: {aspect_ratio}")
            print(f"👥 Person generation: {person_generation}")
            
            start_time = time.time()
            
            # Prepare video generation parameters
            video_params = {
                "model": "veo-3.0-generate-preview",
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "person_generation": person_generation,
            }
            
            # Add negative prompt if provided
            if negative_prompt:
                video_params["negative_prompt"] = negative_prompt
            
            # Generate video using Veo 3.0 model
            print("🔄 Sending request to Veo 3.0...")
            operation = self.client.models.generate_videos(**video_params)
            
            print(f"🔄 Video generation started. Operation ID: {operation.name}")
            
            # Poll the operation status until the video is ready
            while not operation.done:
                elapsed_time = time.time() - start_time
                
                if elapsed_time > max_wait_time:
                    print(f"⏰ Timeout: Video generation took longer than {max_wait_time} seconds")
                    return None
                
                print(f"⏳ Waiting for video generation... ({elapsed_time:.0f}s elapsed)")
                time.sleep(10)
                operation = self.client.operations.get(operation)
            
            # Check if generation was successful
            if not hasattr(operation.response, 'generated_videos') or not operation.response.generated_videos:
                print("❌ Video generation failed - no videos in response")
                return None
            
            # Download the generated video
            generated_video = operation.response.generated_videos[0]
            
            # Generate output filename if not provided
            if not output_filename:
                timestamp = int(time.time())
                safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_prompt = safe_prompt.replace(' ', '_')[:30]
                aspect_suffix = aspect_ratio.replace(":", "x")
                output_filename = f"veo_{aspect_suffix}_{safe_prompt}_{timestamp}.mp4"
            
            # Ensure the filename has .mp4 extension
            if not output_filename.endswith('.mp4'):
                output_filename += '.mp4'
            
            # Create output directory if it doesn't exist
            output_path = Path("video/generated") / output_filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download and save the video
            print(f"💾 Downloading video...")
            self.client.files.download(file=generated_video.video)
            generated_video.video.save(str(output_path))
            
            print(f"✅ Video generated successfully!")
            print(f"📁 Saved to: {output_path}")
            print(f"⏱️ Total generation time: {time.time() - start_time:.1f} seconds")
            
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Error generating video: {e}")
            return None
    
    def generate_video_script(self, prompt: str):
        """
        Generate a detailed video script/storyboard using Gemini
        
        Args:
            prompt (str): Basic video description
            
        Returns:
            str: Detailed video script
        """
        try:
            script_prompt = f"""
            Create a detailed video script and storyboard for this concept:
            {prompt}
            
            Please provide:
            1. Scene breakdown (shot by shot)
            2. Camera movements and angles
            3. Lighting suggestions
            4. Audio/music recommendations
            5. Duration for each scene
            6. Visual effects or transitions
            7. Color palette suggestions
            
            Format this as a professional video production script.
            """
            
            print("🎭 Generating video script with Gemini...")
            # Note: For script generation, we'll use a simple text response
            # since the client is focused on video generation
            return f"Video Script for: {prompt}\n\nThis would be a detailed script generated by Gemini's text capabilities.\nFor actual video generation, use the generate_video() method."
            
            if response and response.text:
                return response.text
            else:
                return "Failed to generate script"
                
        except Exception as e:
            print(f"❌ Error generating script: {e}")
            return f"Error: {str(e)}"
    
    def analyze_video_concept(self, prompt: str):
        """
        Analyze a video concept and provide production insights
        
        Args:
            prompt (str): Video concept description
            
        Returns:
            dict: Analysis results
        """
        try:
            analysis_prompt = f"""
            Analyze this video concept and provide production insights:
            {prompt}
            
            Please analyze:
            1. Technical feasibility (1-10 scale)
            2. Estimated production complexity
            3. Required equipment/resources
            4. Potential challenges
            5. Budget estimation (low/medium/high)
            6. Target audience
            7. Similar reference videos or styles
            8. Improvement suggestions
            
            Provide a structured analysis.
            """
            
            print("🔍 Analyzing video concept...")
            # Note: Analysis would require text generation capabilities
            # For now, return a placeholder analysis
            return {
                "success": True,
                "analysis": f"Video Concept Analysis for: {prompt}\n\nThis is a placeholder analysis. The Gemini client is optimized for video generation with Veo 3.0.\nFor detailed analysis, you would need to integrate with Gemini's text generation capabilities.",
                "prompt": prompt
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_multiple_concepts(self, base_prompt: str, variations: int = 3):
        """
        Generate multiple video concept variations
        
        Args:
            base_prompt (str): Base video concept
            variations (int): Number of variations to generate
        
        Returns:
            list: List of video concept variations
        """
        try:
            variation_prompt = f"""
            Based on this video concept: {base_prompt}
            
            Generate {variations} creative variations of this concept.
            Each variation should:
            1. Maintain the core theme
            2. Offer a unique perspective or approach
            3. Be feasible to produce
            4. Have distinct visual style
            
            Format each variation as:
            Variation X: [Title]
            Description: [Detailed description]
            Style: [Visual style]
            Mood: [Emotional tone]
            ---
            """
            
            print(f"🎨 Generating {variations} concept variations...")
            # Note: This would require text generation capabilities
            # For now, return placeholder variations
            variations_list = []
            for i in range(variations):
                variations_list.append(f"Variation {i+1}: Alternative approach to '{base_prompt}'\nDescription: This would be a creative variation generated by Gemini's text capabilities.\nStyle: Cinematic\nMood: Engaging")
            
            return variations_list
                
        except Exception as e:
            print(f"❌ Error generating variations: {e}")
            return [f"Error: {str(e)}"]

def main():
    """Main function to demonstrate video generation"""
    print("🎬 GEMINI VIDEO GENERATION DEMO")
    print("=" * 60)
    
    try:
        # Initialize the video generator
        generator = GeminiVideoGenerator()
        
        # Example prompts for different types of videos
        example_prompts = [
            {
                "name": "Dialogue Scene",
                "prompt": "A close up of two people staring at a cryptic drawing on a wall, torchlight flickering. A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"
            },
            {
                "name": "Nature Scene",
                "prompt": "A serene mountain lake at sunrise with mist rising from the water, birds flying overhead, and gentle ripples on the surface reflecting the golden sky."
            },
            {
                "name": "Urban Scene",
                "prompt": "A bustling city street at night with neon lights reflecting on wet pavement, people walking with umbrellas, and cars passing by with their headlights creating light trails."
            },
            {
                "name": "Abstract Art",
                "prompt": "Colorful paint drops falling into clear water in slow motion, creating beautiful swirling patterns and mixing colors in an artistic display."
            }
        ]
        
        print("Available example prompts:")
        for i, example in enumerate(example_prompts, 1):
            print(f"{i}. {example['name']}")
            print(f"   {example['prompt'][:80]}...")
        
        print("\nOptions:")
        print("1. Generate video concept analysis")
        print("2. Generate detailed video script")
        print("3. Generate concept variations")
        print("4. 🎬 Generate ACTUAL VIDEO with Veo 3.0 (from examples)")
        print("5. 🎬 Generate CUSTOM VIDEO with Veo 3.0")
        print("6. Custom video concept analysis")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            # Video concept analysis
            example_choice = input(f"Choose example (1-{len(example_prompts)}): ").strip()
            try:
                example_index = int(example_choice) - 1
                if 0 <= example_index < len(example_prompts):
                    selected_example = example_prompts[example_index]
                    print(f"\n🎯 Analyzing: {selected_example['name']}")
                    
                    analysis = generator.analyze_video_concept(selected_example['prompt'])
                    
                    if analysis["success"]:
                        print(f"\n📊 Analysis Results:")
                        print("=" * 50)
                        print(analysis["analysis"])
                        
                        # Save analysis to file
                        timestamp = int(time.time())
                        filename = f"analysis_{selected_example['name'].lower().replace(' ', '_')}_{timestamp}.txt"
                        output_path = Path("video/generated") / filename
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(f"Video Concept Analysis\n")
                            f.write(f"=====================\n\n")
                            f.write(f"Concept: {selected_example['name']}\n")
                            f.write(f"Prompt: {selected_example['prompt']}\n\n")
                            f.write(f"Analysis:\n")
                            f.write(f"=========\n")
                            f.write(analysis["analysis"])
                        
                        print(f"\n💾 Analysis saved to: {output_path}")
                    else:
                        print(f"\n❌ Analysis failed: {analysis['error']}")
                else:
                    print("❌ Invalid example choice")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == "2":
            # Generate video script
            example_choice = input(f"Choose example (1-{len(example_prompts)}): ").strip()
            try:
                example_index = int(example_choice) - 1
                if 0 <= example_index < len(example_prompts):
                    selected_example = example_prompts[example_index]
                    print(f"\n🎭 Generating script for: {selected_example['name']}")
                    
                    script = generator.generate_video_script(selected_example['prompt'])
                    
                    print(f"\n📝 Generated Script:")
                    print("=" * 50)
                    print(script[:500] + "..." if len(script) > 500 else script)
                    
                    # Save script to file
                    timestamp = int(time.time())
                    filename = f"script_{selected_example['name'].lower().replace(' ', '_')}_{timestamp}.txt"
                    output_path = Path("video/generated") / filename
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(f"Video Script\n")
                        f.write(f"============\n\n")
                        f.write(f"Concept: {selected_example['name']}\n")
                        f.write(f"Prompt: {selected_example['prompt']}\n\n")
                        f.write(f"Script:\n")
                        f.write(f"=======\n")
                        f.write(script)
                    
                    print(f"\n💾 Script saved to: {output_path}")
                else:
                    print("❌ Invalid example choice")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == "3":
            # Generate concept variations
            example_choice = input(f"Choose example (1-{len(example_prompts)}): ").strip()
            try:
                example_index = int(example_choice) - 1
                if 0 <= example_index < len(example_prompts):
                    selected_example = example_prompts[example_index]
                    print(f"\n🎨 Generating variations for: {selected_example['name']}")
                    
                    variations = generator.generate_multiple_concepts(selected_example['prompt'], 3)
                    
                    print(f"\n🎭 Generated Variations:")
                    print("=" * 50)
                    for i, variation in enumerate(variations, 1):
                        if variation.strip():
                            print(f"\n{variation.strip()}")
                    
                    # Save variations to file
                    timestamp = int(time.time())
                    filename = f"variations_{selected_example['name'].lower().replace(' ', '_')}_{timestamp}.txt"
                    output_path = Path("video/generated") / filename
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(f"Video Concept Variations\n")
                        f.write(f"========================\n\n")
                        f.write(f"Base Concept: {selected_example['name']}\n")
                        f.write(f"Base Prompt: {selected_example['prompt']}\n\n")
                        f.write(f"Variations:\n")
                        f.write(f"===========\n")
                        for variation in variations:
                            if variation.strip():
                                f.write(f"\n{variation.strip()}\n")
                    
                    print(f"\n💾 Variations saved to: {output_path}")
                else:
                    print("❌ Invalid example choice")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == "4":
            # Generate actual video with Veo 3.0
            example_choice = input(f"Choose example (1-{len(example_prompts)}): ").strip()
            try:
                example_index = int(example_choice) - 1
                if 0 <= example_index < len(example_prompts):
                    selected_example = example_prompts[example_index]
                    print(f"\n🎬 Generating video for: {selected_example['name']}")
                    
                    # Ask for video configuration
                    print("\n📐 Choose aspect ratio:")
                    print("1. 16:9 (Landscape/YouTube)")
                    print("2. 9:16 (Portrait/TikTok/Instagram)")
                    print("3. 1:1 (Square/Instagram)")
                    
                    aspect_choice = input("Enter choice (1-3, default 1): ").strip() or "1"
                    aspect_ratios = {"1": "16:9", "2": "9:16", "3": "1:1"}
                    aspect_ratio = aspect_ratios.get(aspect_choice, "16:9")
                    
                    # Ask for negative prompt
                    negative_prompt = input("\n🚫 Enter negative prompt (what to avoid, optional): ").strip()
                    if not negative_prompt:
                        negative_prompt = "blurry, low quality, distorted faces, bad lighting, shaky camera"
                    
                    print(f"\n🎬 Starting video generation...")
                    print(f"📐 Aspect ratio: {aspect_ratio}")
                    print(f"🚫 Negative prompt: {negative_prompt}")
                    
                    result = generator.generate_video(
                        prompt=selected_example['prompt'],
                        negative_prompt=negative_prompt,
                        aspect_ratio=aspect_ratio,
                        person_generation="allow_all"
                    )
                    
                    if result:
                        print(f"\n🎉 Video generated successfully!")
                        print(f"📁 Saved to: {result}")
                        print(f"💡 You can now play the video file!")
                    else:
                        print("\n❌ Video generation failed")
                else:
                    print("❌ Invalid example choice")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == "5":
            # Generate custom video with Veo 3.0
            custom_prompt = input("\nEnter your custom video prompt: ").strip()
            if custom_prompt:
                print(f"\n🎬 Generating custom video...")
                
                # Ask for video configuration
                print("\n📐 Choose aspect ratio:")
                print("1. 16:9 (Landscape/YouTube)")
                print("2. 9:16 (Portrait/TikTok/Instagram)")
                print("3. 1:1 (Square/Instagram)")
                
                aspect_choice = input("Enter choice (1-3, default 1): ").strip() or "1"
                aspect_ratios = {"1": "16:9", "2": "9:16", "3": "1:1"}
                aspect_ratio = aspect_ratios.get(aspect_choice, "16:9")
                
                # Ask for negative prompt
                negative_prompt = input("\n🚫 Enter negative prompt (what to avoid, optional): ").strip()
                if not negative_prompt:
                    negative_prompt = "blurry, low quality, distorted faces, bad lighting, shaky camera"
                
                print(f"\n🎬 Starting custom video generation...")
                print(f"📝 Prompt: {custom_prompt}")
                print(f"📐 Aspect ratio: {aspect_ratio}")
                print(f"🚫 Negative prompt: {negative_prompt}")
                
                result = generator.generate_video(
                    prompt=custom_prompt,
                    negative_prompt=negative_prompt,
                    aspect_ratio=aspect_ratio,
                    person_generation="allow_all"
                )
                
                if result:
                    print(f"\n🎉 Custom video generated successfully!")
                    print(f"📁 Saved to: {result}")
                    print(f"💡 You can now play the video file!")
                else:
                    print("\n❌ Custom video generation failed")
            else:
                print("❌ Empty prompt")
        
        elif choice == "6":
            # Custom concept analysis
            custom_prompt = input("\nEnter your video concept: ").strip()
            if custom_prompt:
                analysis = generator.analyze_video_concept(custom_prompt)
                
                if analysis["success"]:
                    print(f"\n📊 Analysis Results:")
                    print("=" * 50)
                    print(analysis["analysis"])
                else:
                    print(f"\n❌ Analysis failed: {analysis['error']}")
            else:
                print("❌ Empty prompt")
        
        elif choice == "7":
            print("👋 Goodbye!")
        
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Generation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()