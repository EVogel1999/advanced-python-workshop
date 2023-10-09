import asyncio
import httpx
import pprint

from time import perf_counter


BASE_URL = "https://jsonplaceholder.typicode.com"


class PostIterator:
  def __init__(self, url: str, *, post_per_next: int = 5):
    self._url = f'{url}/posts'
    self._post_per_next = post_per_next
  
  def __aiter__(self):
    self._index = 1
    return self

  async def __anext__(self):
    # Check if the index is greater then the max
    if self._index > 100:
      raise StopAsyncIteration

    # Make the requests in parallel
    async with httpx.AsyncClient() as client:
      co = []
      for i in range(self._post_per_next):
        index = self._index + i
        if index > 100:
          raise StopAsyncIteration

        co.append(client.get(f'{self._url}/{index}'))
      
      # Adjust the current index and return the responses
      self._index += self._post_per_next
      resps = await asyncio.gather(*co)
    
    return [resp.json() for resp in resps]



async def main():
  async for post_group in PostIterator(BASE_URL):
    print('\n\n\n\n')
    pprint.pprint(post_group)


if __name__ == "__main__":
  start = perf_counter() 
  asyncio.run(main())
  stop = perf_counter()

  print(f'\n\n\n\nTotal Elapsed Time: {stop-start}')
