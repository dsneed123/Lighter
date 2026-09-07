from ollama import chat
import ollama


def order_models():
    models = []

    for model in ollama.list().models:
        info = ollama.show(model.model)

        parameters = float(info.details.parameter_size.replace("B", ""))
        context = info.modelinfo.get("llama.context_length", 0)

        models.append({
            "name": model.model,
            "parameters": parameters,
            "context": context
        })

    models.sort(key=lambda model: model["parameters"])

    return models  

"""Estimates tokens using roughly 4 characters per token and ensures the result is at least 1."""
def calc_token_cost(query):
    words = len(query.split())  # Counts the whitespace-separated words in the query.
    characters = len(query)  # Counts every character in the query.
    return round((words * 1.3) + (characters / 10))  # Combines word and character estimates to produce a rough token baseline.
        
def required_context(tokens):
    if tokens <= 500:
        return 4_000
    if tokens <= 2_000:
        return 8_000
    if tokens <= 8_000:
        return 16_000
    return 32_000


def select_model(models, required_context):
    compatible = [
        model for model in models
        if model["context"] >= required_context
    ]

    return compatible[0] if compatible else None

def get_model(query):
    estimate_token_cost = calc_token_cost(query)

    context_estimate = required_context(estimate_token_cost)

    model_list = order_models()
    return select_model(model_list, context_estimate)

def run_query(query):
    selected_model = get_model(query)
    response = ollama.chat(
        model=selected_model["name"],
        messages=[{"role": "user", "content": query}]
    )

    return response.message.content