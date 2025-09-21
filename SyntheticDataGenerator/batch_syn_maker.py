from concurrent.futures import ThreadPoolExecutor, as_completed
import json, re, os
import ollama

from SyntheticDataGenerator.creative_prompts import system_prompt, user_prompt

def extract_json_blocks(text, batch):
    blocks = re.findall(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    parsed = []
    for block in blocks:
        try:
            parsed.append(json.loads(block))
        except json.JSONDecodeError as e:
            print(f'Error parsing JSON at batch-{batch}: {e}')
    return parsed

def run_batch(batch):
    response = ollama.chat(
        model='deepseek-r1:latest',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
    )
    raw_output = response['message']['content']
    return extract_json_blocks(raw_output, batch)

def save_all(results, filename='SyntheticDataGenerator/conversations_D44.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
    else:
        existing = []
    if not isinstance(existing, list):
        existing = [existing]
    
    # Flatten results
    for res in results:
        existing.extend(res)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=4, ensure_ascii=False)

num_batches = 10
max_workers = 10 # no. of parallel requests

results = []
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = {executor.submit(run_batch, i): i for i in range(num_batches)}
    for future in as_completed(futures):
        batch_id = futures[future]
        try:
            parsed = future.result()
            results.append(parsed)
            print(f'Done with batch {batch_id}')
        except Exception as e:
            print(f'Batch {batch_id} failed: {e}')

save_all(results)
