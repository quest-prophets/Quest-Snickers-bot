import markovify
import sys

print("Reading from stdin...")

text = sys.stdin.read()

print("Generating the model...")

text_model = markovify.Text(text)

starting_words_count = len([key for key in text_model.chain.model.keys() if "___BEGIN__" in key])
print(f"Model generated. # of starting words: {starting_words_count}")

print("Exporting the model to JSON...")

model_json = text_model.to_json()

with open("texts/model.json", "w") as f:
    f.write(model_json)

print("model.json written successfully")
