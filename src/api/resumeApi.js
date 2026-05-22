import { resumeData } from "../data/resumeData";

export async function fetchResumeProfile() {
  await new Promise((resolve) => setTimeout(resolve, 180));
  return structuredClone(resumeData);
}
