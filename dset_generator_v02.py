import csv
import os
import json
import time
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# Read q.csv with bookmark tracking
try:
    with open('q.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        rows = list(reader)
        
    # Find first bookmarked question
    start_index = 0
    for i, row in enumerate(rows):
        if len(row) >= 2 and row[1].strip() == "ERROR":
            start_index = i
            break
    total_questions = len(rows) - start_index

except FileNotFoundError:
    print("Error: q.csv file not found")
    exit()

# Create output directory
output_dir = 'dset_generator'
os.makedirs(output_dir, exist_ok=True)

def save_to_files(data_row):
    # Save to CSV
    csv_path = os.path.join(output_dir, 'output.csv')
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['timestamp', 'question', 'thoughts', 'final_answer'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data_row)
    
    # Save to TXT
    txt_path = os.path.join(output_dir, 'output.txt')
    with open(txt_path, 'a', encoding='utf-8') as txtfile:
        txtfile.write(f"Timestamp: {data_row['timestamp']}\n")
        txtfile.write(f"Question: {data_row['question']}\n")
        txtfile.write(f"Thought Process: {data_row['thoughts']}\n")
        txtfile.write(f"Final Answer: {data_row['final_answer']}\n")
        txtfile.write("-" * 50 + "\n\n")
    
    # Save to JSON
    json_path = os.path.join(output_dir, 'output.json')
    with open(json_path, 'a', encoding='utf-8') as jsonfile:
        json_record = {
            "metadata": {
                "timestamp": data_row['timestamp'],
                "question": data_row['question']
            },
            "response": {
                "reasoning": data_row['thoughts'],
                "answer": data_row['final_answer']
            }
        }
        jsonfile.write(json.dumps(json_record, ensure_ascii=False) + '\n')

# Process questions with retry logic
for i in range(start_index, len(rows)):
    current_row = rows[i]
    question = current_row[0].strip()
    if not question:
        continue

    retry_count = 0
    max_retries = 3
    processed = False
    
    while retry_count <= max_retries:
        try:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Processing question {i-start_index+1}/{total_questions}: {question[:50]}...")
            
            # API Request
            response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[{"role": "user", "content": f"answer this question: {question}"}]
            )
            
            # Process response
            data_row = {
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "question": question,
                "thoughts": response.choices[0].message.reasoning_content,
                "final_answer": response.choices[0].message.content
            }
            
            save_to_files(data_row)
            print(f"Successfully processed question {i-start_index+1}/{total_questions}")
            
            # Clear bookmark if exists
            if len(current_row) >= 2 and current_row[1] == "ERROR":
                current_row[1] = ""
                with open('q.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(header)
                    writer.writerows(rows)
            
            processed = True
            break

        except Exception as e:
            print(f"Error: {str(e)}")
            if retry_count < max_retries:
                wait_time = 60 * (2 ** retry_count)
                print(f"Retrying in {wait_time//60} minutes...")
                time.sleep(wait_time)
                retry_count += 1
            else:
                # Set error bookmark
                if len(current_row) < 2:
                    current_row.append("ERROR")
                else:
                    current_row[1] = "ERROR"
                
                # Update q.csv
                with open('q.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(header)
                    writer.writerows(rows)
                
                print(f"Persistent error. Bookmarked question at row {i+2}. Resume later.")
                exit()

    if not processed:
        exit()

print(f"\nAll {total_questions} questions processed successfully!")
print(f"Output files located in: {os.path.abspath(output_dir)}")