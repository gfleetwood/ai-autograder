import pandas as pd

def create_kb(collection, marked_responses, marking_scheme_row):

    file_name = "question_{}_kb.txt".format(marking_scheme_row["question_number"])
    q_num = marking_scheme_row['question_number']
    
    examples = (
        marked_responses
        .query("question_number == @q_num")
        .to_dict(orient = "records")
    )

    examples_str = "\n\n".join([
        "student answer: {} \n\n student answer score: {}"
        .format(x["student_answer"], int(x["score"]))
        for x in examples
    ])
    
    payload = "\n\n".join(["{}: \n\n {}".format(x,y) for x,y in marked_responses_row.items()])
    payload = payload + "\n\n" + examples_str
    
    #with open(file_name, "w") as f: f.write(payload)
    
    collection.add(
    documents = [payload],
    metadatas = [{"source": "marking_scheme"}],
    ids = ["question_{}_kb".format(q_num)]
    )

    return(True)
    
def mark_questions(collection, row):

    content = """
    You are an expert on grading IGCSE business papers. In your knowledge base you have a document for each of 15 questions. Each document has:

    * the question number

    * the question

    * the maximum number of marks to award for the question

    * a marking scheme determining how many an answer should get

    * a set of possible answers

    * A set of reference student answers and the marks the student got for that answer.

    You will be given a student's answer to a question, which knowledge base file to use to score the student's answer, and the max score for the question. Your answer should be 
    a single number between 0 and that max score, and your reason for deducting marks if you did. If you didn't deduct marks then return "Perfect answer" for the result. Return 
    your answer as a json with keys "gpt_score", and "reason_for_gpt_grade". Do not say anything else besides the json.

    Use the file question_{}_kb.txt to mark this student's response out of {} points:
    
    {}
    """.format(
        str(q_num),
        questions_info.query("question_number == @q_num").marks.values[0],
        row['student_answer']
    )
    
    messages = [{"role": "system", "content": content}]
    
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo", messages = messages, max_tokens = 1000, temperature = 0
    )  
    
    prompt_output = response.choices[0].message.content
    
    return(prompt_output)

