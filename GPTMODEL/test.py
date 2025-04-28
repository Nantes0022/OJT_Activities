import inspect
from transformers import TrainingArguments

print(inspect.signature(TrainingArguments.__init__))