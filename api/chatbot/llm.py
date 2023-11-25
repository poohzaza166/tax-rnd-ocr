from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import StoppingCriteriaList
import torch
import re
from stoping_utils import _SentinelTokenStoppingCriteria
from typing import Union, Optional

class llm:
    def __init__(self, model: str) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForCausalLM.from_pretrained(model, device="auto")

        self.temperature = 0.9
        self.top_k = 0
        self.top_p = 0.9
        self.dosample = True
        self.greedy = False
        self.beam = 0
        self.no_repat_ngram_size = 3
        self.stop_token = None

        self.stopping_criteria = _SentinelTokenStoppingCriteria(self.stop_token)
        self.max_length = 1000    

from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Union

class LLM:
    def __init__(self, model: str) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForCausalLM.from_pretrained(model)

        self.temperature = 0.9
        self.top_k = 40
        self.top_p = 0.9
        self.dosample = True
        self.greedy = False
        self.beam = 0
        self.no_repeat_ngram_size = 0
        self.stop_token = None
        self.repetition_penalty = 1.0
        self.stopping_criteria = _SentinelTokenStoppingCriteria(self.stop_token)
        self.max_length = 1000

    def inference(self, query: str):
        if self.stop_token == None:
            try:
                inputs = self.tokenizer.encode(query, return_tensors="pt")
                outputs = self.model.generate(
                    inputs,
                    max_length=self.max_length,
                    temperature=self.temperature,
                    top_k=self.top_k,
                    top_p=self.top_p,
                    do_sample=self.dosample,
                    greedy=self.greedy,
                    num_beams=self.beam,
                    repetition_penalty = self.repetition_penalty,
                    no_repeat_ngram_size=self.no_repeat_ngram_size,
                )

                
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            stop_list = []
            for i in self.stop_token:
                self.stopping_criteria = _SentinelTokenStoppingCriteria(i)
                self.stop_token.append(self.stopping_criteria)

            self.stopping_criteria = StoppingCriteriaList(stop_list)

            inputs = self.tokenizer.encode(query, return_tensors="pt")
            outputs = self.model.generate(
                inputs,
                max_length=self.max_length,
                temperature=self.temperature,
                top_k=self.top_k,
                top_p=self.top_p,
                do_sample=self.dosample,
                greedy=self.greedy,
                num_beams=self.beam,
                repetition_penalty = self.repetition_penalty,
                no_repeat_ngram_size=self.no_repeat_ngram_size,
                stopping_criteria=self.stopping_criteria
            )

            generated_text = self.tokenizer.decode(outputs[0][inputs:], skip_special_tokens=True)
            return generated_text
        

    def parse_output(self, query: str):
        self.inference(query)


if __name__ == "__main__":
    lm = LLM("/lustre/scratch/public/Yi-34B")
    print(lm.inference("ello"))