from youtube_transcript_api import NoTranscriptFound, TranscriptsDisabled, YouTubeTranscriptApi
from langchain.document_loaders import YoutubeLoader
from langchain.docstore.document import Document
from typing import List, Any
import re

YT_URL_RE = re.compile(r"""(?x)^
    (
        (?:https?://|//)                                    # http(s):// or protocol-independent URL
        (?:(?:(?:(?:\w+\.)?[yY][oO][uU][tT][uU][bB][eE](?:-nocookie|kids)?\.com|
        youtube\.googleapis\.com)/                        # the various hostnames, with wildcard subdomains
        (?:.*?\#/)?                                          # handle anchor (#/) redirect urls
        (?:                                                  # the various things that can precede the ID:
            (?:(?:v|embed|e)/(?!videoseries))                # v/ or embed/ or e/
            |shorts/
            |(?:                                             # or the v= param in all its forms
                (?:(?:watch|movie)(?:_popup)?(?:\.php)?/?)?  # preceding watch(_popup|.php) or nothing (like /?v=xxxx)
                (?:\?|\#!?)                                  # the params delimiter ? or # or #!
                (?:.*?[&;])??                                # any other preceding param (like /?s=tuff&v=xxxx or ?s=tuff&amp;v=V36LpHqtcDY)
                v=
            )
        ))
        |(?:
        youtu\.be|                                        # just youtu.be/xxxx
        vid\.plus|                                        # or vid.plus/xxxx
        )/
        )
    )?                                                       # all until now is optional -> you can pass the naked ID
    (?P<id>[0-9A-Za-z_-]{11})                                # here is it! the YouTube video ID
    (?(1).+)?                                                # if we found the ID, everything can follow
    $"""
    )

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
        match = YT_URL_RE.match(youtube_url)
        if not match:
            raise ValueError(f"Could not determine the video ID for the URL {youtube_url}")
        return match.group("id")

    @classmethod
    def from_youtube_url(cls, youtube_url: str, **kwargs: Any) -> YoutubeLoader:
        """Given youtube URL, load video."""
        video_id = cls.extract_video_id(youtube_url)
        return cls(video_id, **kwargs)
