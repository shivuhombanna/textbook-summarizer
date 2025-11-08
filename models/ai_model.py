from transformers import pipeline

# Use smaller models if needed:
SUMMARIZER_MODEL = "sshleifer/distilbart-cnn-12-6"  # faster & lighter
QG_MODEL = "valhalla/t5-small-qg-hl"

print("Loading summarizer model...")
summarizer = pipeline("summarization", model=SUMMARIZER_MODEL, device=-1)

print("Loading question generation model...")
qg = pipeline("text2text-generation", model=QG_MODEL, device=-1)

def chunk_text(text, chunk_size=3000):
    for i in range(0, len(text), chunk_size):
        yield text[i:i+chunk_size]

def generate_summary(text, max_length=150, min_length=40):
    try:
        # If text is very long, only summarize first chunk
        to_summarize = text[:3500]
        result = summarizer(to_summarize, max_length=max_length, min_length=min_length, do_sample=False)
        return result[0]['summary_text']
    except Exception as e:
        return "Error during summarization: " + str(e)

def generate_questions(text, number_of_questions=7):
    try:
        questions = []
        chunks = list(chunk_text(text))

        for chunk in chunks:
            prompt = "generate multiple questions: " + chunk
            out = qg(prompt, max_length=256, num_return_sequences=1)
            generated = out[0]['generated_text']

            # Split on question marks to separate questions
            for q in generated.split("?"):
                q = q.strip()
                if q:
                    questions.append(q + "?")

            if len(questions) >= number_of_questions:
                break

        # Cut to requested number
        return questions[:number_of_questions]
    except Exception as e:
        return ["Error during question generation: " + str(e)]
