from app.ai.llm.client import OpenAIClient
from app.api.schemas.candidate import CandidateProfile


class CandidateExtractor:
    def __init__(self) -> None:
        self.client = OpenAIClient()

    def extract(
        self,
        resume_text: str,
    ) -> CandidateProfile:

        if not resume_text or not resume_text.strip():
            raise ValueError("Resume text cannot be empty.")

        system_prompt = """
You are an expert resume information extraction system.

Your task is to extract structured candidate information
from the provided resume.

IMPORTANT RULES:

1. Extract only information explicitly present in the resume.
2. Never invent, guess, or fabricate information.
3. If information is not available, return null for scalar fields.
4. For list fields, return an empty list when information is unavailable.
5. Preserve the candidate's actual information accurately.
6. Do not infer social media profiles from the candidate's name.
7. Do not generate URLs.

CONTACT INFORMATION:

Email:
- Extract the candidate's email address if present.

Phone:
- Extract the candidate's primary phone or mobile number if present.

WhatsApp:
- Extract a WhatsApp number ONLY when the resume explicitly
  identifies a number as WhatsApp.
- Do not assume that the normal phone number is a WhatsApp number.

LinkedIn:
- Extract the LinkedIn profile URL if explicitly present.

GitHub:
- Extract the GitHub profile URL if explicitly present.

Portfolio:
- Extract the candidate's personal website or portfolio URL
  if explicitly present.

URL RULES:

- Do not create URLs.
- Do not guess URLs.
- Do not construct LinkedIn URLs from the candidate's name.
- Do not construct GitHub URLs from the candidate's name.
- Do not construct portfolio URLs.
- Return the actual URL found in the resume.
- If a URL is not present, return null.

EXPERIENCE:

Extract the candidate's total professional experience
in years when it is explicitly available or can be reliably
calculated from the employment history.

SKILLS:

Extract technical and professional skills mentioned in the resume.

EDUCATION:

Extract degrees, institutions, and relevant education information.

PROJECTS:

Extract meaningful projects mentioned in the resume.

CERTIFICATIONS:

Extract certifications mentioned in the resume.
"""

        user_prompt = f"""
Extract the candidate profile from the following resume.

--- RESUME START ---

{resume_text}

--- RESUME END ---
"""

        return self.client.parse(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=CandidateProfile,
        )