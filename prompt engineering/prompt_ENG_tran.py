from click import prompt
from transformers import AutoTokenizer , AutoModelForSeq2SeqLM
from datasets import load_dataset

dataset_name = "opus_books"
data_set = load_dataset(dataset_name , "en-fr")
print(data_set)

#print example for clearfication
print(f'''the sentence is : {data_set["train"][0]["translation"]["fr"]} \n 
the translation is : {data_set["train"][0]["translation"]["en"]}''')


#load model and tokenizer 
model_name= "google/flan-t5-base"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name,special_tokens=True)

#without prompt engineering
examples_index = [30,1200]

for i,index in enumerate(examples_index) :
    print(f"example number {i+1} : \n")
    print(f"the sentence is : {data_set['train'][index]['translation']['fr']} \n")
    print(f"the human translation to English is : {data_set['train'][index]['translation']['en']} \n")

    example_encoded =tokenizer(data_set['train'][index]['translation']['en'],return_tensors="pt")
    trans_generated  = model.generate(example_encoded["input_ids"],max_new_tokens=100)[0]
    translated_text = tokenizer.decode(trans_generated, skip_special_tokens=True)
    print(f"the model translation to english is : {translated_text} \n")


#with prompt engineering 
def generating_prompt(included_examples,example_to_apply):
    prompt = ''
    for index in included_examples:
        prompt += f'''translate the following sentence from French to English : 
        sentense : {data_set['train'][index]['translation']['fr']}
        translation : {data_set["train"][index]["translation"]["en"]} \n\n'''
    prompt += f'''translate the following sentence from French to English :
    sentense : {data_set['train'][example_to_apply]['translation']['fr']}''' 
    return prompt



def apply_translation(shot_prompt,example_to_apply):
    input = tokenizer(shot_prompt,return_tensors="pt")
    generated_text = model.generate(input["input_ids"],max_new_tokens=100)[0]
    output = tokenizer.decode(generated_text, skip_special_tokens=True)
    print(f"the prompt is : {shot_prompt} \n")
    print (f"the model translation to english is : {output} \n")
    print(f"the human translation to English is : {data_set['train'][example_to_apply]['translation']['en']} \n")


zero_shot_prompt = generating_prompt([],340)
apply_translation(zero_shot_prompt, 340)

one_shot = generating_prompt([30],340)
apply_translation(one_shot, 340)

few_shot = generating_prompt([30,1200], 340)
apply_translation(few_shot, 340)
