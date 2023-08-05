from Dice import DiceModel
key_path, model, class_dict = "elite-striker-343511-2249c8c11f81.json", "monologg/koelectra-base-v3-discriminator", "dictionary.pickle"
model = DiceModel.TextModel(key_path, model, class_dict) 
data, K = "text", 5
category, prob = model.infer(data, K)
print(category)
print(prob)
