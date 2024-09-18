import os
from apify_client import ApifyClient
import pandas as pd
from config import settings
def send_requests_for_job_post(job_title,job_location,job_search_number):

    client = ApifyClient(settings.APIFY_API_TOKEN)

    run_input = {
        "query": job_title,
        "location": job_location,
        "delay": 200,
        "max_results": job_search_number,
        "remote": ["1"],
        "contract_type": ["F"],
        "time_interval": "ANY",
        "li_at_cookie": "",
        "proxyConfiguration": {
            "useApifyProxy": True,
            "apifyProxyCountry": "US",
        },
    }

    # Run the Actor and wait for it to finish
    run = client.actor(settings.ACTOR_TOKEN).call(run_input=run_input)

    jobs_list = list()
    count = 0
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        jobs_list.append(item)
        count += 1
        if count == int(job_search_number):
            break
    print(jobs_list)
    jobs_dataset = pd.DataFrame(jobs_list)
    print(jobs_dataset)
    jobs_dataset.to_csv(f'Sample_job_posts/{job_title}_{job_location}Jobs_posts.csv',index=False)
    return jobs_dataset

