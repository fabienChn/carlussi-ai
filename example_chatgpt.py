import sys
import chatgpt

query = sys.argv[1]

response = chatgpt.transcript_to_answer(query)

print(response)