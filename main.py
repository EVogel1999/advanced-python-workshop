import asyncio


async def main():
  print('Hello async world!')
  await asyncio.sleep(5)
  print('Finished sleeping...')


if __name__ == "__main__":
  asyncio.run(main())
  
