"""Synthetic data generation via LLMs placeholder."""

def generate_synthetic(seed_prompts, n=10):
    """Generate synthetic examples from seed prompts using LLM (placeholder).

    Replace placeholder with real LLM calls (OpenAI, local LLM) and sampling controls.
    """
    synthetic = []
    for i, p in enumerate(seed_prompts):
        for j in range(n):
            synthetic.append({'id': f'syn-{i}-{j}', 'prompt': p, 'response': f'generated response for {p} #{j}'})
    return synthetic
