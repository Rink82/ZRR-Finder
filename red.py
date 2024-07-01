import asyncio
import aiohttp
from aiofiles import open as aopen

async def get_final_url(session, url):
    try:
        async with session.get(url, allow_redirects=True, timeout=10) as response:
            return url, str(response.url)
    except Exception as e:
        return url, f"Error: {str(e)}"

async def process_links(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [get_final_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    async with aopen('red.log', 'w') as f:
        for original_url, final_url in results:
            await f.write(f"{original_url} -> {final_url}\n")

async def main():
    with open('link.log', 'r') as file:
        urls = [line.strip() for line in file]
    
    await process_links(urls)

if __name__ == "__main__":
    asyncio.run(main())