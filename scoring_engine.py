def calculate_clarity_score(result):

    ai_score = result["ai_clarity_score"]
    ambiguity_list = result.get("ambiguities", [])

    ambiguity_count = len(ambiguity_list)

    penalty = ambiguity_count * 3
    final_score = ai_score - penalty

    if final_score < 0:
        final_score = 0
    if final_score > 100:
        final_score = 100

    return final_score