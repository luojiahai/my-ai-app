import torch
import transformers

class Generator(object):
    def __init__(self, pretrained_model_name_or_path, *args, **kwargs):
        if torch.cuda.is_available():
            self._device = torch.device('cuda')
        elif torch.backends.mps.is_available():
            self._device = torch.device('mps')
        else:
            self._device = torch.device('cpu')

        self._model = transformers.AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=pretrained_model_name_or_path,
            *args,
            **kwargs,
        )

        self._tokenizer = transformers.AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=pretrained_model_name_or_path,
            *args,
            **kwargs,
        )

        self._pipeline = transformers.pipeline(
            task='text-generation',
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device,
        )

    @property
    def device(self):
        return self._device

    @property
    def model(self):
        return self._model

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def pipeline(self):
        return self._pipeline

    def generate(self, prompt: str, *args, **kwargs):
        text_inputs = [{'role': 'user', 'content': prompt}]
        text_outputs = self.pipeline(
            text_inputs=text_inputs,
            *args,
            **kwargs,
        )
        return text_outputs
