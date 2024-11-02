from fastapi import APIRouter
from ..models.chat import AutoCompleteModel, ChatModel, ChatResponseModel
from transformers import pipeline
import torch

router = APIRouter()

def generate_response(message: str) -> dict:
    generator = pipeline("text-generation", model="gpt2-large")
    return generator(message)


@router.post("/autocomplete/")
async def autocomplete(body: AutoCompleteModel) -> ChatResponseModel:
    response = generate_response(body.phrase)
    return ChatResponseModel(assistant=response[0]['generated_text'])


def format_response(response: dict) -> str:
    return ''.join(response.split("\n<|assistant|>\n")[1:]).strip()

@router.post("/chat/")
async def chat(body: ChatModel) -> ChatResponseModel:
    
    #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    
    pipe = pipeline("text-generation",
                    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                    torch_dtype=torch.bfloat16,
                    device=device)


    message = [
        {"role": "system",
         "content": "You are a friendly chatbot that responds to technical questions."},
        {"role": "user",
         "content": body.message}
    ]
    prompt = pipe.tokenizer.apply_chat_template(
        message,
        tokenize=False,
        add_generation_prompt=True
    )
    
    prediction = pipe(prompt,
                   max_new_tokens=256,
                   do_sample=True,
                   temperature=0.7, top_k=50, top_p=0.95)

    response = prediction[0]['generated_text']
    return ChatResponseModel(assistant=format_response(response))
    