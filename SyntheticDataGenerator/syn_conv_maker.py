from prompts import system_prompt, user_prompt
import json, re, os
import ollama

def extract_json_blocks(text,batch):
    blocks = re.findall(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    parsed = []
    for block in blocks:
        try:
            parsed.append(json.loads(block))
        except json.JSONDecodeError as e:
            print(f"Error parsing the json block at batch-{batch}: ",e)
    return parsed

def append_to_json_file(new_data, batch, filename="SyntheticDataGenerator/conversations.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
    else:
        existing = []  
    if not isinstance(existing, list):
        existing = [existing]
    existing.append(new_data)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4, ensure_ascii=False)

num_batches = 100  
for i in range(num_batches):
    response = ollama.chat(
        model="deepseek-r1:latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    # print("Raw output:", response['message']['content'])
    raw_output = response['message']['content']
    parsed_output = extract_json_blocks(raw_output,i)
    # print("Parsed Output: ", parsed_output)
    append_to_json_file(parsed_output,i)
    print(f"Done with batch {i}")
    
    