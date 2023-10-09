import asyncio
import httpx
import pprint

from time import perf_counter


BASE_URL = "https://jsonplaceholder.typicode.com"


class PostIterator:
  def __init__(self, url: str, *, post_per_next: int = 5):
    self._url = f'{url}/posts'
    self._post_per_next = post_per_next
  
  def __iter__(self):
    self._index = 1
    return self

  def __next__(self):
    # Check if the index is greater then the max
    if self._index > 100:
      raise StopIteration

    # Make the requests in parallel
    co = []
    for i in range(self._post_per_next):
      index = self._index + i
      if index > 100:
        raise StopIteration

      co.append(httpx.get(f'{self._url}/{index}'))
      
    # Adjust the current index and return the responses
    self._index += self._post_per_next
    
    return [resp.json() for resp in co]



def main():
  for post_group in PostIterator(BASE_URL):
    print('\n\n\n\n')
    pprint.pprint(post_group)


if __name__ == "__main__":
  start = perf_counter() 
  main()
  stop = perf_counter()

  print(f'\n\n\n\nTotal Elapsed Time: {stop-start}')
