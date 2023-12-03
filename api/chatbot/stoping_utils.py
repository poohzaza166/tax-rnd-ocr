from typing import Optional
import transformers
import torch
import re
import time

class _SentinelTokenStoppingCriteria(transformers.StoppingCriteria):

    def __init__(self, sentinel_token_ids: torch.LongTensor,
                 starting_idx: int, tokenizer, stop_string: str):
        transformers.StoppingCriteria.__init__(self)
        self.sentinel_token_ids = sentinel_token_ids
        self.starting_idx = starting_idx
        self.stopstring = stop_string
        self.tokenizer = tokenizer
        self.count = 0

    def __call__(self, input_ids: torch.LongTensor,
                 _scores: torch.FloatTensor) -> bool:
        for sample in input_ids:
            trimmed_sample = sample[self.starting_idx:]
            # Can't unfold, output is still too tiny. Skip.
            if trimmed_sample.shape[-1] < self.sentinel_token_ids.shape[-1]:
                continue

            for window in trimmed_sample.unfold(dimension=0, size=self.sentinel_token_ids.shape[-1], step=1):
                chunk  = self.tokenizer.decode(window)
                # print(chunk)
                if self.stopstring in chunk:
                    # if self.count >=1:
                        # print("++++++++++++++")
                        # print(chunk)
                        # print(self.stopstring)
                        # print('stop reason token hit')
                        # print('=======================')
                        # self.count = 0
                    return True
                    # print(self.count)
                    # self.count += 1
                    # return False
                if torch.all(torch.eq(self.sentinel_token_ids, window)):
                    return True
                
        return False

class MaxTimeCriteria(transformers.StoppingCriteria):
    """
    This class can be used to stop generation whenever the full generation exceeds some amount of time. By default, the
    time will start being counted when you initialize this function. You can override this by passing an
    `initial_time`.

    Args:
        max_time (`float`):
            The maximum allowed time in seconds for the generation.
        initial_time (`float`, *optional*, defaults to `time.time()`):
            The start of the generation allowed time.
    """

    def __init__(self, max_time: float, initial_timestamp: Optional[float] = None):
        self.max_time = max_time
        self.initial_timestamp = time.time() if initial_timestamp is None else initial_timestamp

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        var = time.time() - self.initial_timestamp > self.max_time
        if var:
            print('stopreason time out')
            return True