from youtube_transcript_api import NoTranscriptFound, TranscriptsDisabled, YouTubeTranscriptApi
from langchain.document_loaders import YoutubeLoader
from langchain.docstore.document import Document
from typing import List, Any
import re

class CustomYoutubeLoader(YoutubeLoader):

    def load(self) -> List[Document]:
        """Load documents."""
        metadata = {"source": self.video_id}

        if self.add_video_info:
            video_info = self._get_video_info()
            metadata.update(video_info)

        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(self.video_id)
        except TranscriptsDisabled:
            return []

        transcript = None
        try:
            transcript = transcript_list.find_transcript([self.language])

        except NoTranscriptFound:
            try:
                transcript = transcript_list.find_generated_transcript([self.language])
            except NoTranscriptFound:
                uk_transcript = transcript_list.find_generated_transcript(["uk"])
                transcript = uk_transcript.translate(self.language)

        transcript_pieces = transcript.fetch()
        transcript_text = " ".join([t["text"].strip(" ") for t in transcript_pieces])

        return [Document(page_content=transcript_text, metadata=metadata)]

    @staticmethod
    def extract_video_id(youtube_url: str) -> str:
        """Extract video id from common YT urls."""
        match = re.search(r"(?:youtube\.com/.*v=|youtu\.be/)([^&]+)", youtube_url)
        if not match:
            raise ValueError(f"Could not determine the video ID for the URL {youtube_url}")
        return match.group(1)

    @classmethod
    def from_youtube_url(cls, youtube_url: str, **kwargs: Any) -> YoutubeLoader:
        """Given youtube URL, load video."""
        video_id = cls.extract_video_id(youtube_url)
        return cls(video_id, **kwargs)
