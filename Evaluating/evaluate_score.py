from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from pathlib import Path
import sys
import json

def calculate_scores(reference_folder, inference_json):
    evaluate_data_folder = Path(reference_folder)
    pdf_reference = []
    for txt_file in evaluate_data_folder.rglob("*.txt"):  # Get all .txt files in the folder
        with open(txt_file, "r",encoding="utf-8") as f:
            tup = tuple([str(txt_file.name),f.read()])
            pdf_reference.append(tup)
    pdf_reference.sort(key=lambda x: x[0])
    pdf_inference = []
    with open(inference_json, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            pdf_inference.append((data["file_name"], data["summary"]))
    pdf_inference.sort(key=lambda x: x[0])
    #print("inferences",pdf_inference)
    #print("references", pdf_reference)
    rouges = []
    bleus = []
    for (r_name, r_txt) in (pdf_reference):
        for (i_name, i_txt) in (pdf_inference):
            if r_name == i_name:
                print(f"Getting score of:{r_name}")
                rouges.append(rouge_score(i_txt, r_txt))
                bleus.append(bleu_socre(i_txt, r_txt))
    #print("bleus",bleus)
    #print("rouges", rouges)
    avg_rouge = {
        'rouge1': sum(d['rouge1'] for d in rouges) / len(rouges),
        'rouge2': sum(d['rouge2'] for d in rouges) / len(rouges),
        'rougeL': sum(d['rougeL'] for d in rouges) / len(rouges)
    }
    avg_bleu = sum(bleus) / len(bleus)
    print(f"Among{len(rouges)} files ,avg_rouge:{avg_rouge}, avg_bleu: {avg_bleu}")
    return avg_rouge, avg_bleu

def rouge_score(inference, ref):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(ref[1], inference[1])  # ref[1] and inference[1] are the texts
    return {k: v.fmeasure for k, v in scores.items()}
def bleu_socre(inference, ref):
    reference_tokens = [ref[1].split()]  # list of list of tokens
    candidate_tokens = inference[1].split()
    score = sentence_bleu(reference_tokens, candidate_tokens, 
                          smoothing_function=SmoothingFunction().method1)
    return score



if __name__ == "__main__":
    arguments = sys.argv
    # The first element of sys.argv is the script name itself
    # Subsequent elements are the command-line arguments
    if len(arguments) != 3:
        print("[folder that store references] [inference json file]")
    else:
        calculate_scores(arguments[1], arguments[2])

