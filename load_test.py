import asyncio
import time
import httpx

URL = "http://localhost:8000/api/v1/predict"

API_KEY = "your-existing-api-key"

payload = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}


async def send_request(client):
    start = time.perf_counter()

    try:
        response = await client.post(
            URL,
            headers={
                "X-API-Key": API_KEY,
                "Content-Type": "application/json"
            },
            json=payload
        )

        duration = time.perf_counter() - start

        return response.status_code, duration

    except Exception:
        return 0, 0


async def main():

    total_requests = 50

    async with httpx.AsyncClient() as client:

        tasks = [
            send_request(client)
            for _ in range(total_requests)
        ]

        results = await asyncio.gather(*tasks)

    successful = sum(
        1 for status, _ in results
        if status == 200
    )

    failed = total_requests - successful

    times = [
        duration
        for _, duration in results
        if duration > 0
    ]

    average_time = sum(times) / len(times)

    print("----- LOAD TEST RESULTS -----")
    print(f"Total Requests : {total_requests}")
    print(f"Successful     : {successful}")
    print(f"Failed         : {failed}")
    print(f"Average Time   : {average_time:.4f} seconds")
    print(f"Maximum Time   : {max(times):.4f} seconds")


asyncio.run(main())