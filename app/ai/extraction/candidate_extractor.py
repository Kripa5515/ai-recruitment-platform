from app.ai.llm.client import OpenAIClient
from app.api.schemas.candidate import CandidateProfile


class CandidateExtractor:
    def __init__(self):
        self.llm = OpenAIClient()

    def extract(self, resume_text: str) -> CandidateProfile:
        if not resume_text.strip():
            raise ValueError("Resume text cannot be empty.")

        response = self.llm.client.responses.parse(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a resume information extraction system. "
                        "Extract candidate information from the provided "
                        "resume text. "
                        "Do not invent information. "
                        "If information is not present, return null for "
                        "optional scalar fields and an empty list for "
                        "list fields."
                    ),
                },
                {
                    "role": "user",
                    "content": resume_text,
                },
            ],
            text_format=CandidateProfile,
        )

        return response.output_parsed