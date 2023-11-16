
import multiprocessing as mp
from PIL import Image, ImageSequence
import rembg


def getFrames(im_path: str):
    with Image.open(im_path) as im:
        frames = []
        for frame in ImageSequence.Iterator(im):
            frame = frame.convert('RGBA')
            frames.append(frame)
    print(f"number frames: {len(frames)}")
    return frames, im


def edit_images(frame):
    rem_frame = rembg.remove(frame)
    print(f"bg removed")
    return rem_frame


def main(my_path: str):
    """
    This is the main entry point for the program
    """

    print(f"number of cpus: {mp.cpu_count()}")

    frames, im = getFrames(my_path)
    
    duration = im.info['duration']

    frames = frames[:10]

    print(f"no. frames: {len(frames)}")

    with mp.Pool(4) as p:
        q = p.map(edit_images, [frame for frame in frames])

    print(f"processes complete")

    edited_frames = []

    # Get the results from the queues
    for frame in q:
        edited_frames.append(frame)

    # Save the edited frames as a GIF file

    edited_frames[0].save('edited.gif',
                          save_all=True,
                          append_images=edited_frames[1:],
                          duration=duration,
                          disposal=2,
                          loop=0)

    print("Done!")
