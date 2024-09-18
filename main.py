from fastapi import FastAPI, HTTPException
import scrap_linkedin_jobs
import calculate_similarity_score
from pydantic import BaseModel

app = FastAPI()

class PredictRequest(BaseModel):
    job_title: str
    job_location: str
    job_search_number: float
    resume: str

@app.post("/predict")
async def predict(request: PredictRequest):
    
    try:
        job_title = request.job_title
        job_location = request.job_location
        job_search_number = request.job_search_number
        resume = request.resume

        # Scrap Linkedin job post with ApifyClient
        job_descriptions = scrap_linkedin_jobs.send_requests_for_job_post(job_title, job_location,job_search_number)
        print(job_descriptions)
        # Calculate the most similar results
        score = calculate_similarity_score.match_results(resume, job_descriptions)

        # API Response
        return {"score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
