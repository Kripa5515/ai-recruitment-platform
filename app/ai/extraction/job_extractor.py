from app.ai.llm.client import OpenAIClient
from app.api.schemas.job_requirements import JobRequirements


class JobExtractor:
    """
    Extract structured job requirements from an unstructured
    job description using an LLM.
    """

    def __init__(self):
        self.llm = OpenAIClient()

    def extract(
        self,
        job_description: str,
    ) -> JobRequirements:

        if not job_description or not job_description.strip():
            raise ValueError(
                "Job description cannot be empty."
            )

        response = self.llm.client.responses.parse(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert recruitment "
                        "job-description information extraction system. "

                        "Extract structured information "
                        "from the provided job description. "

                        "Do not invent, guess, or fabricate "
                        "any information. "

                        "Extract only information that is explicitly "
                        "present in the job description. "

                        "Extract the job title when explicitly "
                        "mentioned or clearly presented as the "
                        "job position/title. "

                        "Extract the company name only when it is "
                        "explicitly mentioned in the job description. "

                        "If the company name is not present, "
                        "return null for company. "

                        "If the job title is not present, "
                        "return null for title. "

                        "Extract the minimum required experience "
                        "in years when explicitly mentioned. "

                        "Examples: "
                        "'4+ years' means 4, "
                        "'minimum 5 years' means 5, "
                        "'3 years' means 3. "

                        "For technical skills, programming languages, "
                        "frameworks, databases, cloud platforms, "
                        "tools, libraries, and technologies: "

                        "If explicitly required, include them in "
                        "required_skills. "

                        "If explicitly marked as preferred, optional, "
                        "nice-to-have, good-to-have, bonus, or "
                        "desirable, include them in preferred_skills. "

                        "Do not put preferred skills into "
                        "required_skills. "

                        "For very short descriptions such as "
                        "'Python developer' or simply 'Python', "
                        "treat the explicitly mentioned technology "
                        "as a required skill. "

                        "Extract education requirements only when "
                        "explicitly mentioned. "

                        "Extract location and employment type only "
                        "when explicitly mentioned. "

                        "Put explicit non-skill requirements, "
                        "conditions, certifications, work "
                        "authorization requirements, travel "
                        "requirements, or similar requirements "
                        "into other_constraints. "

                        "If information is not present, return null "
                        "for optional scalar fields and an empty list "
                        "for list fields. "

                        "Do not make hiring decisions. "
                        "Your responsibility is only structured "
                        "information extraction."
                    ),
                },
                {
                    "role": "user",
                    "content": job_description,
                },
            ],
            text_format=JobRequirements,
        )

        if response.output_parsed is None:
            raise ValueError(
                "LLM failed to extract structured job requirements."
            )

        return response.output_parsed