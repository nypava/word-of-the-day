from moviepy.editor import TextClip, VideoFileClip, CompositeVideoClip, concatenate_videoclips
import os 
import re

class VideoEditor:
    captioned_videos = []
    
    def __init__(self) -> None:
        pass

    def add_subtitle(self, video_id: str, caption: str, dir: str, word: str) -> None:
        video_clip = VideoFileClip(os.path.join("./cache/", f"{video_id}.mp4"))

        regex_word = re.findall(r"\w*" + word + r"\w*", caption, re.IGNORECASE)[0]
        caption = caption.replace(".", " . ")
        caption = self._split_caption(caption, video_clip.size[0]) + "\n"
        caption = caption.replace(regex_word, f"<span foreground='#878584'>{regex_word}</span>")
        caption = f"<span background='black'> {caption} </span>"

        try: 
            caption_clip = TextClip(
                caption, 
                fontsize=13, 
                color="white", 
                bg_color="transparent",
                font="Noto-Sans-Regular",
                method="pango",
                stroke_color="black",
                stroke_width=2
            )
        except Exception:
            return
        
        caption_clip = caption_clip.set_position(("center", "bottom"), relative=True)
        
        captioned_video = CompositeVideoClip([video_clip, caption_clip])
        captioned_video.duration = video_clip.duration
        captioned_video_dir = os.path.join(dir, f"{video_id}-captioned.mp4")
        captioned_video.write_videofile(captioned_video_dir)

        self.captioned_videos.append(captioned_video_dir)

    def concatenate_videos(self, file_path):
        clips_list = []
        for video in self.captioned_videos:
            clips_list.append(VideoFileClip(video))

        concatenated_video =  concatenate_videoclips(clips_list, method="compose")
        concatenated_video.write_videofile(file_path)

        return
    
    def _split_caption(self, caption:str, width:int) -> str:
        splitted_str = ""        
        caption_length = 0
        max_length = int((width * 63) / 640)

        for word in caption.split():
            caption_length += len(word)
            if caption_length < max_length:
                splitted_str += word 
                splitted_str += " "
                continue
        
            caption_length = 0 
            splitted_str += "\n"

        return splitted_str
