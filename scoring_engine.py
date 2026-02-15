def calculate_clarity_score(ai_score, ambiguity_count):

    penalty = ambiguity_count * 3
    final_score = ai_score - penalty

    if final_score < 0:
        final_score = 0
    if final_score > 100:
        final_score = 100

    return final_score
