import re
import random
from pydantic.dataclasses import dataclass
from typing import List, Optional, Mapping, Any
from pydantic import BaseModel, ConfigDict
from stoping_utils import _SentinelTokenStoppingCriteria
import torch
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer,
    StoppingCriteriaList,
)

from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun

@dataclass
class LLMConfig:
    max_length: int = 100
    do_sample: bool = False
    top_p: float = 0.9
    top_k: int = 50 
    temperature: float = 0.7
    repetition_penalty: float = 1.0
    early_stopping: bool = True
    
class GpuLLM(LLM):
    model: AutoModelForCausalLM
    device: str
    config: LLMConfig
    stop_msgs: Any
    seed: int
    
    def __init__(
        self,
        model_name: str,
        device: str,
        config: LLMConfig,
        stop_msgs: List[str] = None,
        seed: int = 0,
        **kwargs
    ):
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map=device, **kwargs)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.config = config
        self.stop_msgs = stop_msgs or []
        self.seed = seed
        self.stop_regex = self._build_stop_regex(stop_msgs)
        self.model_name = model_name
        self.device  = device

    @property
    def _llm_type(self) -> str:
        return f"Custom_llm_infrence for {self.model_name}"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None, 
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        tokenized_prompt = self.tokenizer.encode(
            prompt, 
            return_tensors='pt'
        ).to(self.model.device)
        
        torch.manual_seed(self.seed)
        
        if stop != None:
            stop_token_list = [
                _SentinelTokenStoppingCriteria(
                sentinel_token_ids=self.tokenizer(
                    stop_msg, 
                    add_special_tokens=False, 
                    return_tensors="pt"
                ).input_ids.to(self.model.device),
                starting_idx=tokenized_prompt.shape[-1],
                stop_string=stop_msg, 
                tokenizer=self.tokenizer
            ) 
            for stop_msg in self.stop_msgs
            ]
        
        else:

            stop_token_list = [
                _SentinelTokenStoppingCriteria(
                    sentinel_token_ids=self.tokenizer(
                        stop_msg, 
                        add_special_tokens=False, 
                        return_tensors="pt"
                    ).input_ids.to(self.model.device),
                    starting_idx=tokenized_prompt.shape[-1],
                    stop_string=stop_msg, 
                    tokenizer=self.tokenizer
                ) 
                for stop_msg in self.stop_msgs
            ]
        
        stopping_criteria = StoppingCriteriaList(stop_token_list)
        
        output = self.model.generate(
            inputs=tokenized_prompt,
            max_length=self.config.max_length,
            do_sample=self.config.do_sample,
            top_p=self.config.top_p,
            top_k=self.config.top_k,
            temperature=self.config.temperature,
            repetition_penalty=self.config.repetition_penalty,
            stopping_criteria=stopping_criteria,
            early_stopping=self.config.early_stopping
        )
        
        responses = self.tokenizer.decode(output, skip_special_tokens=True)
        response = responses[0]
        
        final_response = re.sub(
            self.stop_regex,
            '',
            response
        )
        
        return re.sub(r"(##.*)\n?",'', final_response)
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {
            "stop": self.stop_msgs,
            "config": self.config
        }
    
    def _build_stop_regex(self, stop_msgs: List[str]) -> str:
        stop_patterns = []
        for msg in stop_msgs:
            pattern = re.escape(msg)
            stop_patterns.append(pattern)
        return f"({'|'.join(stop_patterns)})"

        
# if __name__ == "__main__":

    # model_name = "Monero/Manticore-13b-Chat-Pyg-Guanaco"
    # device = "cuda"
    
    # tokenizer = LlamaTokenizer.from_pretrained(model_name)
    # config = LLMConfig()
    # stop_msgs = ["Human:", "AI:"]
    
    # llm = CustomLLM(
    #     model_name, 
    #     device, 
    #     tokenizer,
    #     config,
    #     stop_msgs
    # )
    
    # response = llm("Hello, how are you today?")
    # print(response)