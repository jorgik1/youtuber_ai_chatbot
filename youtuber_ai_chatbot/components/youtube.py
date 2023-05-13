from youtube_transcript_api import NoTranscriptFound, TranscriptsDisabled, YouTubeTranscriptApi
from langchain.document_loaders import YoutubeLoader
from langchain.docstore.document import Document
from typing import List

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
