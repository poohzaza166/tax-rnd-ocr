from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForDocumentQuestionAnswering, TrainingArguments, Trainer, DefaultDataCollator, AutoTokenizer

class infrence:
    def __init__(self, model_name: str = "MariaK/layoutlmv2-base-uncased_finetuned_docvqa_v2", 
                        device: str = "cuda:0", language: str = "en"):
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForDocumentQuestionAnswering.from_pretrained(model_name)
        self.language = language



    def runinfrence (self, image, question) -> str:
        image = Image.open(image).convert("RGB")
        print("i been ran")
        with torch.no_grad():
            encoding = self.processor(image, question, return_tensors="pt",)
            outputs = self.model(**encoding)
            start_logits = outputs.start_logits
            end_logits = outputs.end_logits
            predicted_start_idx = start_logits.argmax(-1).item()
            predicted_end_idx = end_logits.argmax(-1).item()

        answer = self.processor.tokenizer.decode(encoding.input_ids.squeeze()[predicted_start_idx : predicted_end_idx + 1])

        if answer == "[CLS]":
            print("no good results found")
            return "idk"

        return answer


class trainLM():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("MariaK/layoutlmv2-base-uncased_finetuned_docvqa")
        self.processor = AutoProcessor.from_pretrained("MariaK/layoutlmv2-base-uncased_finetuned_docvqa")
        self.model = AutoModelForDocumentQuestionAnswering.from_pretrained("MariaK/layoutlmv2-base-uncased_finetuned_docvqa")

        self.data_collator = DefaultDataCollator()
        self.image_processor = self.processor.image_processor


        self.data = {}
        self.examples = {}
    # def get_document_answer(self, image, question):
    #     with torch.no_grad():
    #         encoding = self.processor(image.convert("RGB"), question, return_tensors="pt")
    #         outputs = self.model(**encoding)
    #         start_logits = outputs.start_logits
    #         end_logits = outputs.end_logits
    #         predicted_start_idx = start_logits.argmax(-1).item()
    #         predicted_end_idx = end_logits.argmax(-1).item()

    #     answer = self.processor.tokenizer.decode(encoding.input_ids.squeeze()[predicted_start_idx : predicted_end_idx + 1])
    #     return answer

    # # Load dataset
    # def load_iamge():
        
    #     feature = {}
    #     feature["image"] = Images("path/to/image")
    #     feature["query"] = {"en": "What is the name of the person in the image?"}
    #     feature["answer"] = {"en": "John Doe"}
    #     feature['bounding_boex'] = [[0, 0, 100, 100]]

    def processdata(self):
        # Initialize an empty list to hold lowered words
        words = []

        # Loop through the words in self.data["words"]
        for word in self.data["words"]:
        # Convert each word to lowercase
            lowered_word = word.lower() 
            
            # Print each lowered word
            print(lowered_word)

            # Append the lowered word to the words list
            words.append(lowered_word)

        # Call subfinder function, passing the lowered words list
        # and split answer converted to lowercase 
        match, word_idx_start, word_idx_end = self.subfinder(words, self.data["answer"].lower().split())        
        self.data['word_idx_start'] = word_idx_start
        self.data['end_index'] = word_idx_end

    def load_data(self, dataset_path, batch_size):
        image = Image.open(dataset_path)
        self.data["image"] = image

    def encode_dataset(self, max_length=512):
        questions = self.data["question"]
        words = self.data["words"]
        boxes = self.data["boxes"]
        answers = self.data["answer"]

        # encode the batch of examples and initialize the start_positions and end_positions
        encoding = self.tokenizer(questions, words, boxes, max_length=max_length, padding="max_length", truncation=True)
        start_positions = []
        end_positions = []

        # loop through the examples in the batch
        for i in range(len(questions)):
            cls_index = encoding["input_ids"][i].index(self.tokenizer.cls_token_id)

            # find the position of the answer in example's words
            words_example = [word.lower() for word in words[i]]
            answer = answers[i]
            match, word_idx_start, word_idx_end = self.subfinder(words_example, answer.lower().split())

            if match:
                # if match is found, use `token_type_ids` to find where words start in the encoding
                token_type_ids = encoding["token_type_ids"][i]
                token_start_index = 0
                while token_type_ids[token_start_index] != 1:
                    token_start_index += 1

                token_end_index = len(encoding["input_ids"][i]) - 1
                while token_type_ids[token_end_index] != 1:
                    token_end_index -= 1

                word_ids = encoding.word_ids(i)[token_start_index : token_end_index + 1]
                start_position = cls_index
                end_position = cls_index

                # loop over word_ids and increase `token_start_index` until it matches the answer position in words
                # once it matches, save the `token_start_index` as the `start_position` of the answer in the encoding
                for id in word_ids:
                    if id == word_idx_start:
                        start_position = token_start_index
                    else:
                        token_start_index += 1

                # similarly loop over `word_ids` starting from the end to find the `end_position` of the answer
                for id in word_ids[::-1]:
                    if id == word_idx_end:
                        end_position = token_end_index
                    else:
                        token_end_index -= 1

                start_positions.append(start_position)
                end_positions.append(end_position)

            else:
                start_positions.append(cls_index)
                end_positions.append(cls_index)

        encoding["image"] = self.data["image"]
        encoding["start_positions"] = start_positions
        encoding["end_positions"] = end_positions

        return encoding


    def get_ocr_words_and_boxes(self):
        images = self.data["image"].convert("RGB")
        encoded_inputs = self.image_processor(images)

        self.data["image"] = encoded_inputs.pixel_values
        self.data["words"] = encoded_inputs.words[0]
        self.data["boxes"] = encoded_inputs.boxes

        

    def subfinder(self, words_list, answer_list):
        matches = []
        start_indices = []
        end_indices = []
        for idx, i in enumerate(range(len(words_list))):
            if words_list[i] == answer_list[0] and words_list[i : i + len(answer_list)] == answer_list:
                matches.append(answer_list)
                start_indices.append(idx)
                end_indices.append(idx + len(answer_list) - 1)
        if matches:
            return matches[0], start_indices[0], end_indices[0]
        else:
            return None, 0, 0

        return encoding

    def train_model(self):
        training_args = TrainingArguments(
            per_device_train_batch_size=4,
            num_train_epochs=20,
            save_steps=200,
            logging_steps=50,
            evaluation_strategy="steps",
            learning_rate=5e-5,
            save_total_limit=2,
            remove_unused_columns=False,
            push_to_hub=True,
        )
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=encoded_train_dataset,
            eval_dataset=encoded_test_dataset,
            tokenizer=processor,
        )



    def save_model(model, save_path):
        # Save the model
        model.save_pretrained(save_path)



if __name__ == "__main__":
    # app = LMdata()
    # app.load_data("./img6.jpg", 4)
    # app.get_ocr_words_and_boxes()
    # app.processdata()
    # app.encode_dataset()
    # app.train_model()
    app = infrence()
    print(app.runinfrence("./img24.jpg", "what is the Account number?"))