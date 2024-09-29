from google import generativeai
question_model =  """
1, What is a synonym for 'decent'?
A, acceptable
B, terrible
C, bad
D, awful

2, What is an antonym for 'decent'?
A, good
B, improper
C, nice
D, excellent

3, Which sentence uses 'decent' correctly?
A, The restaurant had a very decent menu.
B, The weather was decent today.
C, He is a decent man.
D, The price was decent.

Answer 1: A
Answer 2: B
Answer 3: C
""" 

def question_generator(api_key: str, word:str) -> dict:
    success = False

    generativeai.configure(api_key=api_key)
    model = generativeai.GenerativeModel('gemini-pro')

    prompt = str(f"""
    Can you make a synonym, antonym and usage in context question for a word '{word}'. I want you to make them all choice.
    
    And use this format when you answer, with no markdown \n {str(question_model)} 
        
    """)

    result = {}    

    while not success:
        try:
            response = model.generate_content(prompt)
            questions = str(response.text).split("\n\n")[:3]
            answers = str(response.text).split("\n\n")[-1]
            answers_splitted = answers.split("\n")
            choices_index = {"A": 0, "B":1, "C":2, "D": 3}
             
            for i in range(3):
                quesions_splitted = questions[i].split("\n")
                question = quesions_splitted[0] 
             
                result[question] = {"choices": quesions_splitted[1:], "answer": choices_index[answers_splitted[i][-1]]}
        except Exception:
            pass

        else: 
            success = True
        
    return result
